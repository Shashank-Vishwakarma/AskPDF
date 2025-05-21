from supabase import Client
from fastapi import UploadFile, HTTPException, status
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents.base import Document
from groq import Groq

from src.config import Config
from src.utils import generate_file_path


class SupabaseService:
    client: Client

    def __init__(self, supabase_url: str, supabase_key: str):
        self.client = Client(
            supabase_url=supabase_url,
            supabase_key=supabase_key
        )

    def upload_file(self, file: UploadFile):
        try:
            response = self.client.storage.from_("docs").upload(
                path=generate_file_path(file.filename),
                file=file.file.read(),
                file_options={
                    "content-type": file.content_type,
                }
            )

            return f"{Config.SUPABASE_URL}/storage/v1/object/public/{response.full_path}"
        except Exception as e:
            print("upload_file: Error: ", str(e))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong!")


class QdrantService:
    client: QdrantClient
    model: SentenceTransformer

    def __init__(self, qdrant_host: str, qdrant_port: str, transformer_model: str):
        self.client = QdrantClient(host=qdrant_host, port=qdrant_port)
        self.model = SentenceTransformer(transformer_model)

    def extract_text_from_pdf(self, pdf_path: str, chunk_size: int=300, chunk_overlap: int=50) -> list[Document]:
        try:
            # Load the pdf
            loader = PyPDFLoader(pdf_path)
            docs = loader.load()

            # Split into chunks
            text_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
            docs = text_splitter.split_documents(docs)

            return docs
        except Exception as e:
            print("extract_text_from_pdf: Error: ", str(e))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong!")

    def create_collection(self, collection_name: str):
        try:
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE)
            )
        except Exception as e:
            print("create_collection: Error: ", str(e))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong!")

    def ingest_documents(self, collection_name: str, pdf_path: str):
        try:
            if not self.client.collection_exists(collection_name):
                self.create_collection(collection_name)

            docs = self.extract_text_from_pdf(pdf_path, chunk_size=300, chunk_overlap=50)

            # create points for ingestion into qdrant
            points: list[PointStruct] = []
            for idx, doc in enumerate(docs):
                point = PointStruct(
                    id=idx,
                    vector=self.model.encode(doc.page_content).tolist(),
                    payload={
                        "text": doc.page_content,
                        **doc.metadata
                    }
                )
                points.append(point)

            self.client.upsert(
                collection_name=collection_name,
                points=points
            )
        except Exception as e:
            print("ingest_documents: Error: ", str(e))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong!")

    def retrieve_documents(self, collection_name: str, query: str, limit: int = 5):
        try:
            response = self.client.search(
                collection_name=collection_name,
                limit=limit,
                query_vector=self.model.encode(query).tolist(),
            )
            
            # Extract only text field
            results = []
            for result in response:
                results.append(result.payload["text"])

            return results
        except Exception as e:
            print("retrieve_documents: Error: ", str(e))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong!")


supabase_service = SupabaseService(
    supabase_key=Config.SUPABASE_KEY,
    supabase_url=Config.SUPABASE_URL
)

qdrant_service = QdrantService(
    qdrant_host=Config.QDRANT_HOST,
    qdrant_port=Config.QDRANT_PORT, 
    transformer_model=Config.TRANSFORMER_MODEL
)