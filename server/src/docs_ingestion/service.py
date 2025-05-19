from supabase import Client
from src.config import Config
from src.utils import generate_file_path
from fastapi import UploadFile, HTTPException, status

class SupabaseService:
    client: Client
    
    def __init__(self):
        self.client = Client(
            supabase_url=Config.SUPABASE_URL,
            supabase_key=Config.SUPABASE_KEY
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

            return f"{Config.SUPABASE_URL}/storage/v1/object/public/docs/{response.full_path}"
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        
supabase_service = SupabaseService()