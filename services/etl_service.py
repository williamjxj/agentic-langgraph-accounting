import os
import asyncio
from typing import List, Dict, Any
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import pytesseract
from pdf2image import convert_from_path
from PIL import Image

class ETLService:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100,
            separators=["\n\n", "\n", " ", ""]
        )

    async def process_pdf(self, file_path: str) -> List[Dict[str, Any]]:
        """Process PDF using standard loader, fallback to OCR if needed."""
        try:
            loader = PyPDFLoader(file_path)
            documents = loader.load()
            
            # If text is too short, it might be a scanned image, try OCR
            total_text = "".join([doc.page_content for doc in documents])
            if len(total_text.strip()) < 50:
                return await self.process_ocr(file_path)
            
            chunks = self.text_splitter.split_documents(documents)
            return [{"content": chunk.page_content, "metadata": chunk.metadata} for chunk in chunks]
        except Exception as e:
            print(f"Error processing PDF {file_path}: {e}")
            return await self.process_ocr(file_path)

    async def process_ocr(self, file_path: str) -> List[Dict[str, Any]]:
        """Perform OCR on PDF pages."""
        try:
            images = convert_from_path(file_path)
            ocr_text = ""
            for img in images:
                ocr_text += pytesseract.image_to_string(img) + "\n"
            
            # Create a single document-like structure
            chunks = self.text_splitter.split_text(ocr_text)
            return [{"content": chunk, "metadata": {"source": file_path, "type": "ocr"}} for chunk in chunks]
        except Exception as e:
            print(f"OCR Error for {file_path}: {e}")
            return []

    async def process_markdown(self, file_path: str) -> List[Dict[str, Any]]:
        """Process markdown reports."""
        loader = TextLoader(file_path)
        documents = loader.load()
        chunks = self.text_splitter.split_documents(documents)
        return [{"content": chunk.page_content, "metadata": chunk.metadata} for chunk in chunks]

    async def run_pipeline(self, data_dir: str):
        """Walk through data directory and process all files."""
        all_chunks = []
        for root, _, files in os.walk(data_dir):
            for file in files:
                file_path = os.path.join(root, file)
                if file.endswith(".pdf"):
                    chunks = await self.process_pdf(file_path)
                    all_chunks.extend(chunks)
                elif file.endswith(".md"):
                    chunks = await self.process_markdown(file_path)
                    all_chunks.extend(chunks)
        return all_chunks

# For testing
if __name__ == "__main__":
    from pathlib import Path
    etl = ETLService()
    # Example: Run from project root
    # project_root = Path(__file__).parent.parent
    # asyncio.run(etl.run_pipeline(str(project_root / "data")))
