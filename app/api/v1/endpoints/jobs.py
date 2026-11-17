from fastapi import APIRouter, status

router = APIRouter()

job_data = [
    {"id": 1, "title": "Software Engineer", "company": "Tech Corp"},
    {"id": 2, "title": "Product Manager", "company": "Innovate Inc"}
]

total_jobs = len(job_data)

@router.get("/jobs", status_code=status.HTTP_200_OK)
async def get_jobs():
    return {
        "message": "List of jobs",
        "total_jobs": total_jobs,
        "jobs": job_data
    }