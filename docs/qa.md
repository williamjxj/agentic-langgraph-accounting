# Query Guide & FAQ

## 📊 Dataset Overview

Before asking queries, understand what data is available:

### Invoice Database (SQL)
- **250 invoices** spanning 2022-2026
- **50 unique vendors** across various industries
- **12 categories**: IT, Legal, Marketing, Operations, HR, Finance, Facilities, Consulting, R&D, Compliance, Travel, Supplies
- **11 departments**: Engineering, Sales, Finance, Marketing, HR, Operations, Legal, IT, Executive, Customer Service, R&D
- **7 statuses**: Pending (20), Paid (154), Overdue (76), Approved, Rejected, On Hold, Cancelled
- **Payment terms**: Net 30, Net 45, Net 60, Net 90, Due on Receipt
- **Amount range**: $100 - $76,000 (realistic distribution)

### Document Store (RAG)
- **20+ audit reports** in Markdown format
- **Quarterly reports**: Q1-Q4 2024 financial summaries
- **Vendor analysis**: Top vendor spending patterns
- **Compliance reports**: GAAP compliance reviews
- **Category reports**: IT, Legal, Marketing, HR spending breakdowns

---

## 🎯 Query Categories & Examples

### Category 1: SQL-Routed Queries (Structured Data)

These queries trigger the **SQL node** and query the invoice database directly.

**Route Display:** `🔍 Route: route → query_sql → generate`

#### Count & Aggregate Queries

```
✅ "How many invoices are pending?"
   Expected: "20 pending invoices (Total: $XXX,XXX.XX)"
   
✅ "How many invoices are overdue?"
   Expected: "76 overdue invoices (Total: $XXX,XXX.XX)"
   
✅ "How many invoices are paid?"
   Expected: "154 paid invoices (Total: $XXX,XXX.XX)"
   
✅ "What's the total number of invoices?"
   Expected: "Total number of invoices: 250"
```

#### Vendor Analysis

```
✅ "Show me total spending by vendor"
   Expected: List of all 50 vendors with totals
   
✅ "What's the total amount for Tech Solutions LLC?"
   Expected: Vendor-specific spending total
   
✅ "Which vendors have the highest invoices?"
   Expected: Top vendors ranked by spending
```

#### Category Breakdown

```
✅ "Show me spending by category"
   Expected: IT, Legal, Marketing, etc. with totals
   
✅ "How much did we spend on IT?"
   Expected: Total IT category spending
   
✅ "What are our Marketing expenses?"
   Expected: Marketing category breakdown
   
✅ "Show me all Legal spending"
   Expected: Legal category total and details
```

#### Department Analysis

```
✅ "Show spending by department"
   Expected: Engineering, Sales, Finance, etc. with totals
   
✅ "What did Engineering spend?"
   Expected: Engineering department total
   
✅ "How much did the Sales department spend?"
   Expected: Sales department spending
   
✅ "Show me HR department invoices"
   Expected: HR-related invoice details
```

#### Status-Based Queries

```
✅ "Show me pending invoices"
   Expected: List of 20 pending invoices with details
   
✅ "List all overdue invoices"
   Expected: 76 overdue invoices with due dates
   
✅ "Which invoices are paid?"
   Expected: List of 154 paid invoices
   
✅ "Show me cancelled invoices"
   Expected: Cancelled invoice details
```

#### Time-Based Queries (Note: May need enhancement)

```
⚠️ "Show me invoices from 2024"
   Current: May return recent invoices (limited date filtering)
   
⚠️ "What were our expenses in Q4?"
   Current: May need to check both SQL and reports
```

---

### Category 2: RAG-Routed Queries (Document Search)

These queries trigger the **RAG node** and search through audit reports and documents.

**Route Display:** `🔍 Route: route → query_rag → generate`

#### Audit Report Queries

```
✅ "Show me the Q4 2024 audit report"
   Expected: Q4 quarterly report summary (24 invoices, $412,289.20)
   
✅ "What does the Q1 audit report say?"
   Expected: Q1 quarterly financial summary
   
✅ "Show me the Q2 2024 report"
   Expected: Q2 report details with metrics
   
✅ "What were Q3 revenues?"
   Expected: Q3 revenue data from report
```

#### Compliance & Standards

```
✅ "Is the company GAAP compliant?"
   Expected: Compliance status from reports
   
✅ "Show me compliance findings"
   Expected: Compliance report summary
   
✅ "What does the compliance report say?"
   Expected: GAAP compliance review details
   
✅ "Are we following purchasing policies?"
   Expected: Policy compliance information
```

#### Growth & Trends

```
✅ "What does the audit report say about growth?"
   Expected: Revenue growth analysis from reports
   
✅ "Show me revenue trends"
   Expected: Trend data from quarterly reports
   
✅ "What are the key financial metrics?"
   Expected: Metrics from audit summaries
```

#### Vendor Analysis (from Reports)

```
✅ "What does the vendor analysis report say?"
   Expected: Vendor performance review
   
✅ "Show me vendor performance reviews"
   Expected: Vendor analysis findings
   
✅ "What are the top vendor recommendations?"
   Expected: Vendor-related insights from reports
```

#### Category-Specific Reports

```
✅ "Show me the IT spending report"
   Expected: IT category audit report
   
✅ "What does the Marketing report say?"
   Expected: Marketing spending analysis
   
✅ "Show me Legal expenses analysis"
   Expected: Legal category report
   
✅ "What about HR spending trends?"
   Expected: HR category insights
```

---

### Category 3: Hybrid Queries (Both SQL + RAG)

These queries trigger **both nodes** for comprehensive answers combining database and documents.

**Route Display:** `🔍 Route: route → query_both → query_sql → query_rag → generate`

#### Combined Analysis

```
✅ "Which vendor has the highest invoices and what does the audit say about them?"
   Expected: SQL data + vendor analysis report insights
   
✅ "Show me invoice totals and the audit report's compliance findings"
   Expected: SQL totals + compliance report summary
   
✅ "What's our IT spending and what does the quarterly report say about tech?"
   Expected: SQL IT totals + report analysis
   
✅ "vendor compliance status"
   Expected: SQL vendor data + compliance documents
```

#### Generic/Exploratory Queries

```
✅ "hello" or "hi"
   Expected: Introductory response with sample data from both SQL and RAG
   
✅ "What can you tell me about our finances?"
   Expected: Overview using both database and reports
   
✅ "Give me a financial summary"
   Expected: Combined SQL metrics + report insights
   
✅ "What's the overall spending picture?"
   Expected: Hybrid analysis from both sources
```

---

## 💡 Tips & Best Practices

### 1. Understanding Route Visibility

**Every response shows the execution path:**
- **🔍 Route:** Shows which nodes were executed
- **Icons indicate source:**
  - 🗄️ = Direct SQL database query
  - 📄 = Document semantic search  
  - 📊 = Hybrid search (both SQL + RAG)

**Example:**
```
Query: "how many invoices are pending"
Response starts with:
  🔍 Route: route → query_sql → generate
  🗄️ Direct SQL database query
```

### 2. Keyword-Based Routing

**SQL Keywords** (trigger database queries):
- invoice, vendor, amount, total, sum, count
- how many, list all, show me
- paid, pending, overdue, status
- category, department

**RAG Keywords** (trigger document search):
- report, audit, analysis, summary
- growth, compliance, revenue, expense
- GAAP, quarter, Q1, Q2, Q3, Q4
- trend, findings, recommendations

**Pro Tip:** Mix keywords to trigger hybrid routing for comprehensive answers!

### 3. Be Specific for Better Results

❌ Vague: "Tell me about invoices"
✅ Better: "How many invoices are pending?"

❌ Vague: "What about reports?"
✅ Better: "Show me the Q4 2024 audit report"

❌ Vague: "Vendor stuff"
✅ Better: "Show me total spending by vendor"

### 4. Use Natural Language

The agent understands conversational queries:

```
✅ "How much did we spend on IT this year?"
✅ "Are there any overdue invoices I should worry about?"
✅ "What's the deal with our Q4 numbers?"
✅ "Which vendors are costing us the most?"
```

### 5. Explore Different Perspectives

**Same data, different questions:**
```
"Show me pending invoices"          → List view
"How many invoices are pending?"    → Count only
"What's the total amount pending?"  → Sum aggregation
"Which vendors have pending items?" → Vendor grouping
```

### 6. Leverage the Rich Metadata

The 250 invoices include 16 fields - ask about them!

```
✅ "Show me invoices with Net 30 payment terms"
✅ "Which invoices have PO numbers?"
✅ "What are the tax rates on our invoices?"
✅ "Show me invoices by department"
✅ "What's the subtotal vs total breakdown?"
```

### 7. Test the Routing Logic

**Force specific routes by using keywords:**

```
# Force SQL route
"Count invoices"
"Show vendor amounts"
"List pending status"

# Force RAG route
"Quarterly audit"
"Compliance report findings"
"Revenue growth analysis"

# Force hybrid route
"hello"
"general overview"
"vendor compliance"
```

### 8. Multi-Turn Conversations

While the current version doesn't have conversation memory, you can:
- Ask follow-up questions with full context
- Reference previous answers explicitly

```
First: "How many invoices are pending?"
Then:  "Show me the pending invoices from Tech Solutions LLC"
```

---

## 🐛 Troubleshooting & FAQs

### Q1: "I asked about pending invoices but got a generic count"

**A:** Make sure to include status keywords. Try:
- ✅ "How many invoices are **pending**?"
- ✅ "Show me **pending** invoices"
- ❌ "How many invoices?" (too generic)

### Q2: "The route shows query_both but I wanted just SQL"

**A:** Your query likely had both SQL and RAG keywords. Be more specific:
- For SQL only: Use "count", "total", "list", "show me"
- For RAG only: Use "report", "audit", "compliance", "analysis"

### Q3: "I don't see any actual invoice amounts in the response"

**A:** The demo might be running without the DEEPSEEK_API_KEY. Check:
```bash
echo $DEEPSEEK_API_KEY
# If empty, set it:
export DEEPSEEK_API_KEY="your-key-here"
```

Then restart the server:
```bash
python run_server.py
```

### Q4: "Can I ask about specific invoice IDs?"

**A:** Yes! Try:
```
"Show me invoice INV-2024-0045"
"What's the status of INV-2023-0123?"
```

Note: Current SQL query logic may need enhancement for ID-specific queries.

### Q5: "Debug logging shows in terminal but not UI"

**A:** That's intentional! Debug logs (`[DEBUG]`, `[ERROR]`) appear in:
- Backend terminal (where `python run_server.py` runs)
- Not in Streamlit UI (keeps it clean)

To see what's happening:
1. Check the backend terminal
2. Look for `[DEBUG] SQL Query for: ...`
3. See SQL results length

### Q6: "How do I know if the database has all 250 invoices?"

**A:** Ask: "What's the total number of invoices?"

Expected: `Total number of invoices: 250`

If you see `5`, the database needs reloading:
```bash
rm accounting.db
python run_server.py  # Reloads from CSV
```

### Q7: "Can I upload my own invoices?"

**A:** Yes! Use the Streamlit sidebar:
1. Click "Upload an invoice or report (PDF/MD)"
2. Select your file
3. Click "Process Document"
4. Wait for background processing
5. Query the new data!

### Q8: "How does hybrid retrieval work?"

**A:** The RAG system uses **two strategies**:
1. **Semantic Search**: Vector similarity (Sentence Transformers)
2. **Keyword Search**: BM25 algorithm

Both results are combined for better accuracy!

---

## 🚀 Advanced Usage

### Testing Route Visibility

Create a test script to see all route types:

```python
import requests

queries = {
    "SQL": "how many invoices are pending",
    "RAG": "show me the Q4 audit report", 
    "Hybrid": "hello"
}

for route_type, query in queries.items():
    response = requests.post(
        "http://localhost:8000/query",
        json={"query": query, "thread_id": "test"}
    )
    print(f"\n{route_type} Query: {query}")
    print(f"Response: {response.json()['response'][:200]}")
```

### Benchmarking Performance

Time your queries:

```bash
time curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "how many invoices are pending"}'
```

Expected: 1.5-4 seconds end-to-end

### API Direct Usage

Skip Streamlit and use the API directly:

```bash
# Count query
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "how many invoices are pending", "thread_id": "api-user"}'

# Report query  
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "show Q4 audit report", "thread_id": "api-user"}'
```

### Batch Queries (Coming Soon)

Currently single queries only. Future enhancement:
```python
# Future API
POST /batch_query
{
  "queries": [
    "how many pending?",
    "show Q4 report",
    "vendor totals"
  ]
}
```

---

## 📝 Query Templates

### Copy-Paste Ready Queries

**Financial Overview:**
```
How many invoices are pending?
What's the total amount by vendor?
Show me spending by category
Which invoices are overdue?
```

**Compliance Check:**
```
Is the company GAAP compliant?
Show me compliance findings
What does the audit report say about compliance?
```

**Vendor Analysis:**
```
Which vendor has the highest spending?
Show me total amounts by vendor
What does the vendor analysis report say?
```

**Quarterly Review:**
```
Show me the Q4 2024 audit report
What were Q3 revenues?
Give me Q1 financial summary
```

**Department Tracking:**
```
Show spending by department
What did Engineering spend?
How much did Sales spend?
```

**Status Monitoring:**
```
How many invoices are overdue?
Show me all pending invoices
Which invoices are paid?
```

---

## 🎓 Learning Exercises

### Exercise 1: Route Exploration
Ask the same question with different phrasings and observe routing:

1. "invoices pending" → Should route to SQL
2. "pending report" → Might route to RAG
3. "pending analysis" → Might route to hybrid

### Exercise 2: Data Coverage
Find the boundaries of the dataset:

1. "What's the oldest invoice?" → Should find 2022 data
2. "What's the newest invoice?" → Should find 2026 data
3. "How many vendors do we have?" → Should say 50

### Exercise 3: Hybrid Triggering
Try to force a hybrid query:

1. "vendor" (SQL keyword) + "compliance" (RAG keyword)
2. "invoice" (SQL) + "report" (RAG)
3. Generic greeting: "hello" or "hi"

### Exercise 4: Metadata Exploration
Discover all the rich metadata:

1. "What payment terms do we use?"
2. "Show me invoices with PO numbers"
3. "What tax rates appear in our invoices?"

---

## 🔗 Related Documentation

- [README.md](../README.md) - Main project documentation
- [improvement-1.md](improvement-1.md) - Phase 1: Real embeddings & agentic workflow
- [improvement-2.md](improvement-2.md) - Phase 2: Rich dataset & HuggingFace integration
- [improvement-3.md](improvement-3.md) - Phase 3: Cross-platform compatibility
- [data-management.md](data-management.md) - Data architecture & storage

---

## 💭 Community Queries

Share your interesting queries! Some creative examples:

```
"What's the most expensive invoice we have?"
"Which department spends the most?"
"Are we paying vendors on time?"
"What's our average invoice amount?"
"Which vendors have the most invoices?"
"What's the compliance rate in Q4?"
"Show me all IT vendors"
"What are the top 5 spending categories?"
```

---

**Last Updated:** February 2026  
**Dataset Version:** 250 invoices, 20+ reports  
**Route Visibility:** ✅ Enabled  
**Supported Query Types:** SQL, RAG, Hybrid

**Happy Querying! 🚀**
