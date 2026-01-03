"""
Skills API endpoints – CLEANED & STABLE
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import datetime
from pathlib import Path
import pandas as pd
from loguru import logger

from app.models import Skill, SkillDetail
from app.config import settings
from app.data.skill_descriptions import (
    get_skill_description,
    get_default_description,
)
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()


# -------------------------------------------------
# 🔹 Load latest processed CSV
# -------------------------------------------------
def _load_latest_processed_data() -> pd.DataFrame:
    processed_dir = Path(settings.DATA_PROCESSED_DIR)
    files = sorted(processed_dir.glob("processed_skills_*.csv"), reverse=True)

    if not files:
        logger.warning("No processed skill files found")
        return pd.DataFrame()

    try:
        df = pd.read_csv(files[0])
        if "skill" not in df.columns:
            logger.error("Processed CSV missing 'skill' column")
            return pd.DataFrame()

        logger.info(f"Loaded {len(df)} skills from {files[0].name}")
        return df

    except Exception as e:
        logger.error(f"Failed loading processed skills: {e}", exc_info=True)
        return pd.DataFrame()


# -------------------------------------------------
# 🔹 Helper: safely parse Skill row
# -------------------------------------------------
def _parse_skill_row(row: pd.Series, defaults: dict) -> Skill:
    return Skill(
        name=str(row.get("skill")),
        normalized_name=str(row.get("skill")),
        current_demand=float(row.get("current_demand", 0) or 0),
        forecast_demand=float(row.get("forecast_demand", row.get("current_demand", 0)) or 0),
        risk_score=float(row.get("risk_score", 0.5) or 0.5),
        risk_category=str(row.get("risk_category", defaults["risk_category"])),
        trend=str(row.get("forecast_trend", defaults["trend"])),
        last_updated=datetime.utcnow(),
    )


# -------------------------------------------------
# 🔹 GET /skills
# -------------------------------------------------
@router.get("", response_model=List[Skill])
async def get_skills(
    limit: Optional[int] = Query(None, ge=1, le=1000),
    min_risk: Optional[float] = Query(None, ge=0.0, le=1.0),
    max_risk: Optional[float] = Query(None, ge=0.0, le=1.0),
):
    df = _load_latest_processed_data()
    if df.empty:
        return []

    if "risk_score" in df.columns:
        if min_risk is not None:
            df = df[df["risk_score"] >= min_risk]
        if max_risk is not None:
            df = df[df["risk_score"] <= max_risk]

    if limit:
        df = df.head(limit)

    skills: List[Skill] = []

    for _, row in df.iterrows():
        if pd.isna(row.get("skill")):
            continue
        skills.append(
            _parse_skill_row(
                row,
                defaults={"risk_category": "unknown", "trend": "stable"},
            )
        )

    logger.info(f"Returned {len(skills)} skills")
    return skills


## ----------------------------
# GET /skills/high-risk
# ----------------------------
@router.get("/high-risk", response_model=List[Skill])
async def get_high_risk_skills(limit: int = Query(10, ge=1, le=100)):
    df = _load_latest_processed_data()
    if df.empty or "risk_score" not in df.columns:
        return []

    # Ensure numeric column
    df["risk_score"] = pd.to_numeric(df["risk_score"], errors="coerce").fillna(0)

    # Filter high-risk
    high_risk_df = df[df["risk_score"] >= settings.RISK_THRESHOLD_HIGH]

    # Fallback: if not enough rows, pick top risk scores
    if len(high_risk_df) < limit:
        high_risk_df = pd.concat([
            high_risk_df,
            df[~df.index.isin(high_risk_df.index)].nlargest(limit - len(high_risk_df), "risk_score")
        ])

    high_risk_df = high_risk_df.sort_values("risk_score", ascending=False).head(limit)

    skills = [
        _parse_skill_row(row, defaults={"risk_category": "high", "trend": "decreasing"})
        for _, row in high_risk_df.iterrows()
        if not pd.isna(row.get("skill"))
    ]
    logger.info(f"Returned {len(skills)} high-risk skills")
    return skills


# ----------------------------
# GET /skills/emerging
# ----------------------------
@router.get("/emerging", response_model=List[Skill])
async def get_emerging_skills(limit: int = Query(10, ge=1, le=100)):
    df = _load_latest_processed_data()
    if df.empty or not {"risk_score", "job_posting_growth"}.issubset(df.columns):
        return []

    # Ensure numeric columns
    df["risk_score"] = pd.to_numeric(df["risk_score"], errors="coerce").fillna(1.0)
    df["job_posting_growth"] = pd.to_numeric(df["job_posting_growth"], errors="coerce").fillna(0)

    thresholds = [20.0, 5.0, 0.0]  # progressive thresholds
    emerging_df = pd.DataFrame()

    for t in thresholds:
        emerging_df = df[
            (df["risk_score"] <= settings.RISK_THRESHOLD_LOW) &
            (df["job_posting_growth"] > t)
        ]
        if not emerging_df.empty:
            break

    # Fallback: top low-risk skills by growth
    if emerging_df.empty:
        emerging_df = df[df["risk_score"] <= settings.RISK_THRESHOLD_LOW]
        if emerging_df.empty:
            # Last resort: top skills by growth
            emerging_df = df

    emerging_df = emerging_df.sort_values("job_posting_growth", ascending=False).head(limit)

    skills = [
        _parse_skill_row(row, defaults={"risk_category": "low", "trend": "increasing"})
        for _, row in emerging_df.iterrows()
        if not pd.isna(row.get("skill"))
    ]

    logger.info(f"Returned {len(skills)} emerging skills")
    return skills

# -------------------------------------------------
# 🔹 GET /skills/{skill_name}
# -------------------------------------------------
@router.get("/{skill_name}", response_model=SkillDetail)
async def get_skill_detail(skill_name: str):
    df = _load_latest_processed_data()
    if df.empty:
        raise HTTPException(status_code=404, detail="No data available")

    match = df[df["skill"].str.lower() == skill_name.lower()]
    if match.empty:
        raise HTTPException(status_code=404, detail="Skill not found")

    row = match.iloc[0]

    info = get_skill_description(skill_name) or get_default_description(skill_name)

    return SkillDetail(
        name=str(row.get("skill")),
        normalized_name=str(row.get("skill")),
        current_demand=float(row.get("current_demand", 0) or 0),
        forecast_demand=float(row.get("forecast_demand", row.get("current_demand", 0)) or 0),
        risk_score=float(row.get("risk_score", 0.5) or 0.5),
        risk_category=str(row.get("risk_category", "unknown")),
        trend=str(row.get("forecast_trend", "stable")),
        last_updated=datetime.utcnow(),
        job_posting_growth=float(row.get("job_posting_growth", 0) or 0),
        github_velocity=float(row.get("github_velocity", 0) or 0),
        community_mentions=float(row.get("community_decay", 0) or 0),
        research_citations=float(row.get("research_trend", 0) or 0),
        related_skills=[],
        historical_data=[],
        description=info.get("description", ""),
        category=info.get("category", "Technology"),
        popularity=info.get("popularity", "Medium"),
        trend_info=info.get("trend", "Stable"),
    )
