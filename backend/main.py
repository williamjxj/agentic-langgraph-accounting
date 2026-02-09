import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root (parent of backend/)
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(_PROJECT_ROOT / ".env")

from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional
from ..models.database import init_db, async_session, Invoice
from ..services.etl_service import ETLService
from ..services.rag_service import RAGService
from ..agents.audit_agent import AuditAgent
from langchain_core.messages import HumanMessage

app = FastAPI(title="Accounting AI Auditor API")

# Global instances
etl_service = ETLService()
rag_service = RAGService()
audit_agent_graph = None

class QueryRequest(BaseModel):
    query: str
    thread_id: str = "default"

@app.on_event("startup")
async def startup():
    await init_db()
    # Initial data processing
    data_dir = str(_PROJECT_ROOT / "data")
    chunks = await etl_service.run_pipeline(data_dir)
    if chunks:
        rag_service.initialize_vector_store(chunks)
    
    # Sync SQL DB with mock data if empty
    async with async_session() as session:
        from sqlalchemy import select, func
        result = await session.execute(select(func.count()).select_from(Invoice))
        count = result.scalar()
        if count == 0:
            import pandas as pd
            csv_path = _PROJECT_ROOT / "data" / "invoice_summary.csv"
            if csv_path.exists():
                df = pd.read_csv(str(csv_path))
                for _, row in df.iterrows():
                    inv = Invoice(
                        invoice_id=row['invoice_id'],
                        vendor=row['vendor'],
                        amount=row['amount'],
                        date=row['date'],
                        status=row['status']
                    )
                    session.add(inv)
                await session.commit()
            
    global audit_agent_graph
    agent_instance = AuditAgent(rag_service)
    audit_agent_graph = agent_instance.build_graph()

@app.post("/query")
async def query_agent(request: QueryRequest):
    initial_state = {
        "messages": [HumanMessage(content=request.query)],
        "context": {}
    }
    
    # Run the agent (which is now a mock bypass)
    result = await audit_agent_graph.ainvoke(initial_state)
    
    # Return the last message from the agent
    return {"response": result["messages"][-1].content}

@app.post("/upload")
async def upload_document(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    # Save file
    uploads_dir = _PROJECT_ROOT / "data" / "uploads"
    uploads_dir.mkdir(parents=True, exist_ok=True)
    file_path = uploads_dir / file.filename
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    
    # Background processing
    background_tasks.add_task(process_new_file, str(file_path))
    return {"message": f"File {file.filename} uploaded and processing started."}

async def process_new_file(file_path: str):
    if file_path.endswith(".pdf"):
        chunks = await etl_service.process_pdf(file_path)
    elif file_path.endswith(".md"):
        chunks = await etl_service.process_markdown(file_path)
    else:
        return
        
    if chunks:
        await rag_service.add_documents(chunks)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
