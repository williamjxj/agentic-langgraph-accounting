import os
from typing import Annotated, List, Dict, Any, TypedDict, Literal
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], "The messages in the conversation"]
    context: str
    next_action: str
    sql_results: str

class AuditAgent:
    def __init__(self, rag_service, async_session_maker=None):
        self.rag_service = rag_service
        self.async_session_maker = async_session_maker
        api_key = os.getenv("DEEPSEEK_API_KEY")
        self.llm = (
            ChatOpenAI(
                model="deepseek-chat",
                openai_api_key=api_key,
                openai_api_base="https://api.deepseek.com",
            )
            if api_key
            else None
        )
        self.graph = None

    async def route_query(self, state: AgentState) -> AgentState:
        """Determine if the query needs SQL, RAG, or both."""
        query = state["messages"][-1].content.lower()
        
        # Keywords that suggest SQL database queries
        sql_keywords = ["invoice", "vendor", "amount", "total", "sum", "count", "average", 
                       "how many", "list all", "show me", "paid", "pending", "status"]
        
        # Keywords that suggest document/report retrieval
        rag_keywords = ["report", "audit", "analysis", "summary", "growth", "compliance",
                       "revenue", "expense", "gaap", "quarter", "q1", "q2", "q3", "q4"]
        
        sql_score = sum(1 for kw in sql_keywords if kw in query)
        rag_score = sum(1 for kw in rag_keywords if kw in query)
        
        if sql_score > rag_score:
            state["next_action"] = "query_sql"
        elif rag_score > sql_score:
            state["next_action"] = "query_rag"
        else:
            # Default to both for comprehensive answers
            state["next_action"] = "query_both"
        
        return state

    async def query_sql(self, state: AgentState) -> AgentState:
        """Query the SQL database for invoice data."""
        if not self.async_session_maker:
            state["sql_results"] = "SQL database not available."
            return state
        
        try:
            from ..models.database import Invoice
            async with self.async_session_maker() as session:
                query_text = state["messages"][-1].content.lower()
                
                # Enhanced query interpretation with new fields
                if "category" in query_text or "spending by" in query_text:
                    # Category breakdown
                    result = await session.execute(
                        select(Invoice.category, func.sum(Invoice.amount).label('total'))
                        .group_by(Invoice.category)
                        .order_by(func.sum(Invoice.amount).desc())
                    )
                    rows = result.fetchall()
                    sql_results = "Spending by category:\n" + "\n".join(
                        f"- {row.category}: ${row.total:.2f}" for row in rows if row.category
                    )
                elif "department" in query_text:
                    # Department breakdown
                    result = await session.execute(
                        select(Invoice.department, func.sum(Invoice.amount).label('total'))
                        .group_by(Invoice.department)
                        .order_by(func.sum(Invoice.amount).desc())
                    )
                    rows = result.fetchall()
                    sql_results = "Spending by department:\n" + "\n".join(
                        f"- {row.department}: ${row.total:.2f}" for row in rows if row.department
                    )
                elif "overdue" in query_text:
                    # Get overdue invoices
                    result = await session.execute(
                        select(Invoice).where(Invoice.approval_status == "Overdue")
                    )
                    invoices = result.scalars().all()
                    sql_results = f"Overdue invoices ({len(invoices)}):\n" + "\n".join(
                        f"- {inv.invoice_id}: {inv.vendor} - ${inv.amount:.2f} (Due: {inv.due_date})" 
                        for inv in invoices[:10]
                    )
                elif "total" in query_text or "sum" in query_text:
                    # Get total amounts by vendor
                    result = await session.execute(
                        select(Invoice.vendor, func.sum(Invoice.amount).label('total'))
                        .group_by(Invoice.vendor)
                        .order_by(func.sum(Invoice.amount).desc())
                    )
                    rows = result.fetchall()
                    sql_results = "Invoice totals by vendor:\n" + "\n".join(
                        f"- {row.vendor}: ${row.total:.2f}" for row in rows
                    )
                elif "count" in query_text or "how many" in query_text:
                    # Count invoices
                    result = await session.execute(select(func.count()).select_from(Invoice))
                    count = result.scalar()
                    sql_results = f"Total number of invoices: {count}"
                elif "pending" in query_text:
                    # Get pending invoices
                    result = await session.execute(
                        select(Invoice).where(Invoice.status == "Pending")
                    )
                    invoices = result.scalars().all()
                    sql_results = f"Pending invoices ({len(invoices)}):\n" + "\n".join(
                        f"- {inv.invoice_id}: {inv.vendor} - ${inv.amount:.2f}" 
                        for inv in invoices[:10]
                    )
                else:
                    # Default: show all invoices summary
                    result = await session.execute(select(Invoice).limit(10))
                    invoices = result.scalars().all()
                    sql_results = "Recent invoices:\n" + "\n".join(
                        f"- {inv.invoice_id}: {inv.vendor} - ${inv.amount:.2f} ({inv.status})"
                        for inv in invoices
                    )
                
                state["sql_results"] = sql_results
        except Exception as e:
            state["sql_results"] = f"Error querying database: {str(e)}"
        
        return state

    async def query_rag(self, state: AgentState) -> AgentState:
        """Retrieve relevant documents from the RAG store."""
        query = state["messages"][-1].content
        
        if self.rag_service:
            docs = self.rag_service.hybrid_retrieve(query, k=5)
            context = "\n\n".join(doc.page_content for doc in docs) if docs else "No relevant documents found."
        else:
            context = "RAG service not available."
        
        state["context"] = context
        return state

    async def generate_answer(self, state: AgentState) -> AgentState:
        """Generate final answer using LLM with context from SQL and/or RAG."""
        query = state["messages"][-1].content
        
        if self.llm:
            # Build context from available sources
            context_parts = []
            
            if state.get("sql_results"):
                context_parts.append(f"=== Database Query Results ===\n{state['sql_results']}")
            
            if state.get("context"):
                context_parts.append(f"=== Retrieved Documents ===\n{state['context']}")
            
            full_context = "\n\n".join(context_parts) if context_parts else "No context available."
            
            system = (
                "You are an accounting audit assistant with access to both structured invoice data "
                "and audit reports/documents. Use the provided context to answer the user's question accurately. "
                "If the context doesn't contain the answer, say so and provide a brief, professional response."
            )
            
            messages = [
                SystemMessage(content=f"{system}\n\n{full_context}"),
                HumanMessage(content=query),
            ]
            
            response = await self.llm.ainvoke(messages)
            response_text = response.content if hasattr(response, "content") else str(response)
        else:
            # Fallback when DEEPSEEK_API_KEY is not set
            if state.get("sql_results"):
                response_text = f"Based on the database:\n{state['sql_results']}"
            elif state.get("context"):
                response_text = f"Based on the documents:\n{state['context'][:500]}..."
            else:
                response_text = "I don't have enough information to answer that question."
        
        state["messages"] = state["messages"] + [AIMessage(content=response_text)]
        return state

    def route_next_action(self, state: AgentState) -> Literal["query_sql", "query_rag", "query_both"]:
        """Router function for conditional edges."""
        return state.get("next_action", "query_rag")

    async def query_both(self, state: AgentState) -> AgentState:
        """Query both SQL and RAG."""
        state = await self.query_sql(state)
        state = await self.query_rag(state)
        return state

    def build_graph(self):
        """Build the LangGraph workflow with proper StateGraph."""
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("route", self.route_query)
        workflow.add_node("query_sql", self.query_sql)
        workflow.add_node("query_rag", self.query_rag)
        workflow.add_node("query_both", self.query_both)
        workflow.add_node("generate", self.generate_answer)
        
        # Set entry point
        workflow.set_entry_point("route")
        
        # Add conditional edges based on routing decision
        workflow.add_conditional_edges(
            "route",
            self.route_next_action,
            {
                "query_sql": "query_sql",
                "query_rag": "query_rag",
                "query_both": "query_both"
            }
        )
        
        # All query nodes lead to answer generation
        workflow.add_edge("query_sql", "generate")
        workflow.add_edge("query_rag", "generate")
        workflow.add_edge("query_both", "generate")
        workflow.add_edge("generate", END)
        
        # Compile the graph
        self.graph = workflow.compile()
        return self.graph

    async def ainvoke(self, state, config=None):
        """Invoke the compiled graph."""
        if not self.graph:
            self.build_graph()
        
        # Initialize state fields if not present
        if "context" not in state:
            state["context"] = ""
        if "sql_results" not in state:
            state["sql_results"] = ""
        if "next_action" not in state:
            state["next_action"] = ""
        
        result = await self.graph.ainvoke(state, config)
        return result
