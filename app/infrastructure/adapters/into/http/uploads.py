from fastapi import APIRouter, UploadFile, File, HTTPException, status
import os
import uuid
import shutil

router = APIRouter(prefix="/uploads", tags=["uploads"])

UPLOAD_DIR = "static/uploads/logos"

# Create the upload directory if it does not exist
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/logo", status_code=status.HTTP_201_CREATED)
async def upload_logo(file: UploadFile = File(...)):
    """
    Subir un logo y obtener la URL local
    """
    allowed_extensions = {".png", ".jpg", ".jpeg", ".svg", ".webp"}
    file_ext = os.path.splitext(file.filename)[1].lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File type not supported"
        )
    
    try:
        # Generate unique filename to avoid collisions
        unique_filename = f"{uuid.uuid4().hex}{file_ext}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        return {
            "message": "File uploaded successfully",
            "url": f"/{file_path.replace(os.sep, '/')}"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Could not upload file: {str(e)}"
        )
