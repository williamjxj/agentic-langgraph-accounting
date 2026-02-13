# 技术实现：评估与分析

对**会计 AI 审计**应用技术实现的研究和分析，包含各组件及整体的优缺点评估。

---

## 1. 架构概览

| 层级        | 技术              | 职责 |
|-------------|--------------------------|------|
| **API**     | FastAPI + Uvicorn        | REST 后端，异步请求处理 |
| **编排** | LangGraph (最小化) | Agent 状态管理；无实际图拓扑 |
| **RAG**     | LangChain + ChromaDB + BM25 | 文档加载、分块、嵌入、混合检索 |
| **LLM**     | DeepSeek (OpenAI 兼容 API) | 基于 RAG 上下文生成答案 |
| **向量数据库** | ChromaDB (本地)      | 持久化嵌入；内存 BM25 |
| **结构化数据库** | SQLAlchemy + SQLite (异步) | 发票表，启动时从 CSV 加载种子数据 |
| **ETL**     | PyPDF, pdf2image, pytesseract | PDF/MD 加载，OCR 备用方案，分块 |
| **前端**| Streamlit               | 聊天 UI，文件上传，调用后端 HTTP |

数据流：**用户查询 → FastAPI `/query` → AuditAgent 检索 RAG 文档 → DeepSeek LLM → 响应**。上传通过 `/upload`，ETL 在后台运行，RAG 存储随之更新。

---

## 2. 组件分析

### 2.1 后端 (FastAPI)

| 方面 | 实现 |
|--------|----------------|
| 应用入口 | `backend/main.py`；从项目根目录加载 `.env` |
| 启动 | `init_db()`，对 `data/` 完整 ETL，RAG 初始化，DB 为空时加载 CSV 种子数据，构建 agent |
| 端点 | `POST /query` (agent)，`POST /upload` (文件 + 后台 ETL) |
| 状态 | 全局单例：`etl_service`, `rag_service`, `audit_agent_graph` |

**优点**

- 异步端点和异步 agent/LLM 调用适合 I/O 密集型工作负载。
- 路径基于 `_PROJECT_ROOT` 派生，无论当前工作目录在哪都能正常工作。
- 上传使用后台任务避免阻塞请求。
- Pydantic 模型用于请求/响应；全面的类型提示。

**缺点**

- 无依赖注入：服务是全局变量，难以测试和替换（例如 RAG/DB）。
- 每次进程启动都运行完整 ETL；无增量或延迟加载。
- 无身份验证、速率限制或除 Pydantic 外的请求验证。
- `/query` 中的 `thread_id` 虽然被接受但未使用（无对话或数据库持久化）。

---

### 2.2 RAG 服务

| 方面 | 实现 |
|--------|----------------|
| 嵌入 | `FakeEmbeddings(size=1536)` — 确定性，无 API |
| 向量存储 | ChromaDB，`persist_directory="chroma_db"` |
| 关键词 | 内存文档列表上的 BM25Okapi |
| 检索 | `hybrid_retrieve`：向量 top-k + BM25 top-k，按内容去重，返回最多 k 个 |

**优点**

- 混合检索（向量 + BM25）提高了对精确术语和同义词的鲁棒性。
- ChromaDB 持久化在重启后保留。
- 简单易读的 API：`initialize_vector_store`，`hybrid_retrieve`，`add_documents`。
- 默认设置无嵌入 API 成本或密钥（FakeEmbeddings）。

**缺点**

- **FakeEmbeddings**：无真正的语义相似性；向量搜索对语义实际上是随机的。
- BM25 语料库保存在内存中并在每次 `add_documents` 时**重建** — O(n) 且无增量索引。
- Chroma `persist_directory` 相对于 CWD；可能因运行上下文不同而异（见 run_server）。
- 无元数据过滤（例如按来源或日期）或重排序。
- 固定块大小 (1000) 和重叠 (100)；无多向量或句子窗口策略。

---

### 2.3 审计 Agent

| 方面 | 实现 |
|--------|----------------|
| 框架 | LangChain 消息；带 DeepSeek base URL 和 API key 的 `ChatOpenAI` |
| 图 | `build_graph()` 返回 `self`；无 LangGraph 节点/边，单步执行 |
| 流程 | 获取最后一条用户消息 → RAG 检索 (k=5) → 构建系统 + 用户消息 → LLM → 追加 AIMessage |
| 降级方案 | 如果无 `DEEPSEEK_API_KEY`：按关键词硬编码模拟答案 |

**优点**

- 通过 OpenAI 兼容客户端使用 DeepSeek：一个客户端，可配置 base URL 和 key。
- 密钥缺失时优雅降级（演示模式）。
- RAG 上下文通过系统消息注入；上下文与用户查询清晰分离。
- 在 FastAPI 中正确使用异步 `ainvoke`。

**缺点**

- **无真正的 agentic 行为**：无工具，无 SQL，无路由；单次 RAG + LLM 调用（不是 README 中所说的"在 SQL 和文档间选择的 agent"）。
- **SQL DB 未使用**：Invoice 表和 CSV 种子数据从未被 agent 查询。
- LangGraph 只是名义上的；无图结构、循环或工具节点。
- 无对话历史：每个请求都是无状态的；`thread_id` 被忽略。
- 无流式传输；响应仅在完整生成后返回。

---

### 2.4 ETL 服务

| 方面 | 实现 |
|--------|----------------|
| PDF | PyPDFLoader；如果提取文本长度 < 50，切换到 OCR |
| OCR | pdf2image → 每页 pytesseract |
| Markdown | TextLoader + 相同分割器 |
| 分块 | RecursiveCharacterTextSplitter (1000 字符，100 重叠，标准分隔符) |
| 流水线 | `run_pipeline(data_dir)`：遍历树，按扩展名分发 |

**优点**

- 扫描/图像 PDF 的 OCR 备用方案。
- 异步接口（`process_pdf`，`process_markdown`，`run_pipeline`）。
- 所有文档类型使用单一分割器配置；RAG 的块格式一致。

**缺点**

- 文档加载器（PyPDF，TextLoader）是**同步的**；异步方法仍然阻塞 I/O。
- 无重试，无大小限制；大型或格式错误的 PDF 可能减慢或崩溃进程。
- OCR 在进程中运行；CPU 密集且可能阻塞事件循环。
- 仅支持 `.pdf` 和 `.md`；无 Excel、HTML 或其他办公格式。
- 错误仅记录（例如 `print`）；无结构化日志或指标。

---

### 2.5 数据库 (SQLite + SQLAlchemy)

| 方面 | 实现 |
|--------|----------------|
| 引擎 | `sqlite+aiosqlite:///./accounting.db` (相对路径) |
| 模型 | `Invoice`：id, invoice_id, vendor, amount, date, status, created_at |
| 启动 | 创建表；如果发票计数为 0，从 `data/invoice_summary.csv` 加载种子数据 |

**优点**

- 异步引擎和会话；适配 FastAPI 异步风格。
- 简单模式；Pydantic 模式供 API 使用。
- CSV 种子数据提供可重复的演示数据，无需手动 DB 设置。

**缺点**

- **agent 未使用**：无从 agent 到 DB 的工具或查询路径。
- 单一文件路径 `./accounting.db`；位置取决于 CWD（与 Chroma 相同问题）。
- 无迁移（例如 Alembic）；模式更改需手动操作。
- 仅 SQLite；扩展到 Postgres 需要配置，可能还需要连接池。

---

### 2.6 前端 (Streamlit)

| 方面 | 实现 |
|--------|----------------|
| UI | 会话状态中的聊天消息；侧边栏文件上传 |
| 后端 | 使用 `requests.post` 调用 `http://localhost:8000` 的 `/query` 和 `/upload` |

**优点**

- 构建快速；聊天和上传在一个文件中。
- 会话状态在该会话的内存中保留对话。
- 文件上传触发后端处理并提供反馈。

**缺点**

- **硬编码 `localhost:8000`**：当后端在其他位置或 Docker 中时失败。
- 无基于环境变量的 API URL 或配置。
- CSV 路径假设 CWD；从其他目录运行时中断。
- 无身份验证；任何有访问权限的人都可以查询和上传。
- 同步 `requests`；对长答案无流式传输或进度。

---

### 2.7 运行 / 打包

| 方面 | 实现 |
|--------|----------------|
| 服务器 | `run_server.py` 将父目录添加到 `sys.path`，使用模块字符串运行 uvicorn |
| 路径 | 后端使用 `_PROJECT_ROOT`；RAG/DB 仍使用相对路径 `chroma_db` 和 `./accounting.db` |

**优点**

- 从项目根目录运行，无需 `cd` 到父目录；本地开发更简单。
- 单条命令：`python run_server.py`。

**缺点**

- `run_server.py` 中的路径操作较脆弱；依赖于仓库布局。
- 启动器中无 `reload`；代码更改需要手动重启。
- requirements.txt 没有版本固定；构建可能随时间漂移。

---

## 3. 总结：优点与缺点

### 总体优势

- **技术栈现代且连贯**：FastAPI、异步 SQLAlchemy、LangChain、ChromaDB、DeepSeek。
- **混合 RAG 设计**（向量 + BM25）合理；实现清晰。
- **DeepSeek 集成**简单基于密钥；缺少密钥时有降级方案。
- **ETL** 支持 PDF + OCR 和 markdown；适合内部文档和报告。
- **项目布局**（backend、agents、services、models、frontend）清晰易维护。

### 主要缺陷和风险

| 领域 | 问题 | 影响 |
|------|--------|--------|
| RAG | FakeEmbeddings | 无真正的语义搜索；检索质量弱。 |
| RAG | 内存 BM25，添加时完全重建索引 | 不可扩展；大型文档集慢。 |
| Agent | 无工具，无 SQL | README 承诺"查询 SQL 或文档"但仅使用 RAG。 |
| Agent | 无对话记忆 | 无多轮或线程使用。 |
| 数据 | SQL DB 未使用 | 结构化发票数据从不影响答案。 |
| 运维 | 路径（Chroma、DB）相对于 CWD | 不同运行上下文行为不同。 |
| 前端 | 硬编码 API URL | 无法部署而不修改代码。 |
| 运维 | 每次启动完整 ETL | 对大型数据目录缓慢且冗余。 |
| 部署 | 无版本固定 | 可重现性和供应链风险。 |

---

## 4. 建议（优先级排序）

1. **替换 FakeEmbeddings** 为真实嵌入模型（例如 DeepSeek 嵌入如果可用，或小型开源模型），使混合检索有意义。
2. **将 agent 连接到 SQL DB**，通过只读工具（例如"按供应商/日期查询发票"）并添加简单路由器或工具调用步骤，使 agent 能在 RAG 和 SQL 间选择。
3. **使 API URL 可配置**，在前端（环境变量或配置）并修复数据路径以使用项目根或配置。
4. **从 `_PROJECT_ROOT` 解析 RAG/DB 路径**（或单一配置），使 Chroma 和 SQLite 路径在不同运行中保持一致。
5. **添加可选的对话持久化**，使用 `thread_id`（例如内存或 DB），使 agent 能使用最近历史。
6. **固定依赖版本**，在 `requirements.txt`（或使用锁文件）以实现可重现构建。
7. **延迟启动时的完整 ETL**：仅从现有 Chroma 加载，或在单独的作业/脚本中运行 ETL，保持 API 启动轻量。

本文档反映了当前代码库的实现，可随应用演进而更新。
