import os
from typing import List
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

class IngestionManager:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", " ", ""]
        )

    def load_document(self, file_path: str) -> List[Document]:
        """
        Load a document based on file extension.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext == ".pdf":
            loader = PyPDFLoader(file_path)
        elif file_ext == ".txt":
            loader = TextLoader(file_path, encoding="utf-8")
        else:
            raise ValueError(f"Unsupported file type: {file_ext}")
            
        return loader.load()

    def process_and_split(self, file_path: str) -> List[Document]:
        """
        Load a document and split it into chunks.
        """
        documents = self.load_document(file_path)
        return self.text_splitter.split_documents(documents)
