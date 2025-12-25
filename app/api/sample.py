from fastapi import APIRouter

router = APIRouter()


@router.get("/sample")
def sample_endpoint():
    return {"message": "This is a sample endpoint"}