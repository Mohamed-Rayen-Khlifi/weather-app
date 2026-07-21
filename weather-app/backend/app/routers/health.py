from fastapi import APIRouter
from datetime import datetime

router = APIRouter(tags=["Health"])


@router.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "Weather API",
        "time": datetime.utcnow().isoformat()
    }