"""
Roles API endpoints - REAL TIME IMPLEMENTATION
"""
from fastapi import APIRouter
from typing import List, Dict
from datetime import datetime
from loguru import logger
import httpx
import os
from collections import Counter

from app.models import Role
from dotenv import load_dotenv
load_dotenv()


router = APIRouter()

# ✅ KEEP ENV NAMES AS-IS
GITHUB_API_KEY = os.getenv("GITHUB_API_KEY")
JOB_BOARD_API_KEY = os.getenv("JOB_BOARD_API_KEY")   # Adzuna app_key
JOB_BOARD_APP_ID = os.getenv("JOB_BOARD_APP_ID")     # Adzuna app_id


# -------------------------------------------------
# 🔹 Fetch jobs from job board (Adzuna – REAL API)
# -------------------------------------------------
async def fetch_job_roles() -> List[Dict]:
    if not JOB_BOARD_APP_ID or not JOB_BOARD_API_KEY:
        logger.error("Job board credentials missing")
        return []

    # ✅ REAL, FIXED HOSTNAME (no env misuse)
    url = "https://api.adzuna.com/v1/api/jobs/in/search/1"

    params = {
        "app_id": JOB_BOARD_APP_ID,     # correct usage
        "app_key": JOB_BOARD_API_KEY,   # correct usage
        "results_per_page": 50,
        "what": "software engineer OR data scientist OR devops"
    }

    try:
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json().get("results", [])

    except httpx.RequestError as e:
        logger.error(f"Job API connection failed: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected job API error: {e}")
        return []


# -------------------------------------------------
# 🔹 Fetch GitHub skill popularity
# -------------------------------------------------
async def fetch_github_skills(skills: List[str]) -> Dict[str, int]:
    if not GITHUB_API_KEY or not skills:
        return {}

    headers = {
        "Authorization": f"Bearer {GITHUB_API_KEY}",
        "Accept": "application/vnd.github+json"
    }

    popularity = {}

    async with httpx.AsyncClient(timeout=15) as client:
        for skill in skills:
            try:
                params = {"q": skill}
                res = await client.get(
                    "https://api.github.com/search/repositories",
                    headers=headers,
                    params=params
                )

                if res.status_code == 200:
                    popularity[skill] = res.json().get("total_count", 0)

            except Exception as e:
                logger.warning(f"GitHub fetch failed for {skill}: {e}")

    return popularity


# -------------------------------------------------
# 🔹 MAIN ENDPOINT
# -------------------------------------------------
@router.get("/trends", response_model=List[Role])
async def get_role_trends():
    """
    Get real-time role trends using job boards + GitHub
    """
    logger.info("Fetching real-time role trends")

    jobs = await fetch_job_roles()

    # ✅ Never crash frontend
    if not jobs:
        return []

    role_skill_counter: Dict[str, Counter] = {}

    # ---------------------------
    # Extract roles & skills
    # ---------------------------
    for job in jobs:
        role_name = (job.get("title") or "").strip()
        description = (job.get("description") or "").lower()

        if not role_name:
            continue

        role_skill_counter.setdefault(role_name, Counter())

        for skill in [
            "python", "java", "aws", "docker",
            "kubernetes", "react", "sql"
        ]:
            if skill in description:
                role_skill_counter[role_name][skill.capitalize()] += 1

    roles_response: List[Role] = []

    # ---------------------------
    # Build Role objects
    # ---------------------------
    for role_name, skill_counter in role_skill_counter.items():
        skills = [s for s, _ in skill_counter.most_common(5)]

        github_stats = await fetch_github_skills(skills)

        avg_popularity = (
            sum(github_stats.values()) / len(github_stats)
            if github_stats else 0
        )

        if avg_popularity > 5000:
            trend = "increasing"
        elif avg_popularity > 1000:
            trend = "stable"
        else:
            trend = "declining"

        roles_response.append(
            Role(
                name=role_name,
                normalized_name=role_name.lower().replace(" ", "_"),
                required_skills=skills,
                demand_trend=trend,
                last_updated=datetime.utcnow()
            )
        )

    return roles_response


