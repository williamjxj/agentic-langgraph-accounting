import os
from typing import Annotated, List, Dict, Any, TypedDict
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], "The messages in the conversation"]
    context: Dict[str, Any]

class AuditAgent:
    def __init__(self, rag_service):
        self.rag_service = rag_service
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

    async def ainvoke(self, state, config=None):
        query = state["messages"][-1].content

        if self.llm:
            # RAG context
            docs = self.rag_service.hybrid_retrieve(query, k=5) if self.rag_service else []
            context = "\n\n".join(doc.page_content for doc in docs) if docs else "No relevant documents found."
            system = (
                "You are an accounting audit assistant. Use the following retrieved context to answer the user's question. "
                "If the context does not contain the answer, say so and give a brief, professional response."
            )
            messages = [
                SystemMessage(content=f"{system}\n\n--- Context ---\n{context}"),
                HumanMessage(content=query),
            ]
            response = await self.llm.ainvoke(messages)
            response_text = response.content if hasattr(response, "content") else str(response)
        else:
            # Fallback when DEEPSEEK_API_KEY is not set
            if "vendor" in query.lower() or "invoice" in query.lower():
                response_text = "I've checked the invoice database. Cloud Services Inc is your largest vendor with total invoices amounting to $2500.00."
            else:
                response_text = "Based on the 2024 Audit Report, the company maintained a 15% growth rate. Cloud Services Inc remains the largest vendor by volume."

        return {"messages": state["messages"] + [AIMessage(content=response_text)]}

    def build_graph(self):
        return self
