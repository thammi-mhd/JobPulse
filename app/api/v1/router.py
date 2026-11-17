from fastapi import APIRouter

from app.api.v1.endpoints import jobs, users

router = APIRouter()


router.include_router(jobs.router, tags=["jobs"])
router.include_router(users.router, tags=["users"])