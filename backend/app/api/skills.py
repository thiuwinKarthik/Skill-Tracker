"""
Skills API endpoints.
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import datetime
import pandas as pd
from pathlib import Path
from loguru import logger

from app.models import Skill, SkillDetail
from app.config import settings
from app.data.skill_descriptions import get_skill_description, get_default_description

router = APIRouter()


def _load_latest_processed_data() -> pd.DataFrame:
    """
    Load the most recent processed data file.
    
    Returns:
        pd.DataFrame: DataFrame containing skill data, or empty DataFrame if no data found.
    
    The function:
    - Searches for files matching pattern 'processed_skills_*.csv'
    - Loads the most recent file (by filename date)
    - Validates required columns exist
    - Returns empty DataFrame if no files found or errors occur
    """
    processed_dir = Path(settings.DATA_PROCESSED_DIR)
    
    # Find latest processed file
    processed_files = sorted(processed_dir.glob("processed_skills_*.csv"), reverse=True)
    
    if not processed_files:
        logger.warning(f"No processed files found in {processed_dir}")
        return pd.DataFrame()
    
    try:
        latest_file = processed_files[0]
        logger.info(f"Loading processed data from: {latest_file}")
        df = pd.read_csv(latest_file)
        
        # Log what we found
        logger.info(f"Loaded {len(df)} rows, columns: {df.columns.tolist()}")
        
        # Check if required columns exist
        required_cols = ['skill']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            logger.error(f"Missing required columns in CSV: {missing_cols}")
            return pd.DataFrame()
        
        return df
    except Exception as e:
        logger.error(f"Error loading processed data from {processed_files[0]}: {e}", exc_info=True)
        return pd.DataFrame()


@router.get("", response_model=List[Skill])
async def get_skills(
    limit: Optional[int] = Query(None, ge=1, le=1000, description="Limit the number of results returned"),
    min_risk: Optional[float] = Query(None, ge=0.0, le=1.0, description="Minimum risk score (0.0-1.0)"),
    max_risk: Optional[float] = Query(None, ge=0.0, le=1.0, description="Maximum risk score (0.0-1.0)")
):
    """
    Get all skills with their risk scores and trends.
    
    Args:
        limit: Maximum number of skills to return (1-1000)
        min_risk: Filter skills with risk score >= this value
        max_risk: Filter skills with risk score <= this value
    
    Returns:
        List[Skill]: List of skill objects with risk scores, demand, and trends
    
    Example:
        GET /skills?limit=10&min_risk=0.5
    """
    df = _load_latest_processed_data()
    
    if df.empty:
        return []
    
    # Filter by risk if specified
    if 'risk_score' in df.columns:
        if min_risk is not None:
            df = df[df['risk_score'] >= min_risk]
        if max_risk is not None:
            df = df[df['risk_score'] <= max_risk]
    
    # Limit results
    if limit:
        df = df.head(limit)
    
    skills = []
    for idx, row in df.iterrows():
        try:
            # Get skill name - required field
            skill_name = row.get('skill')
            if pd.isna(skill_name) or not skill_name:
                logger.warning(f"Row {idx} has empty skill name, skipping")
                continue
            
            # Get values with defaults
            current_demand = row.get('current_demand', 0)
            forecast_demand = row.get('forecast_demand', current_demand)  # Default to current if missing
            risk_score = row.get('risk_score', 0.5)
            risk_category = row.get('risk_category', 'unknown')
            forecast_trend = row.get('forecast_trend', 'stable')
            
            # Convert to proper types
            skill = Skill(
                name=str(skill_name),
                normalized_name=str(skill_name),
                current_demand=float(current_demand) if not pd.isna(current_demand) else 0.0,
                forecast_demand=float(forecast_demand) if not pd.isna(forecast_demand) else float(current_demand) if not pd.isna(current_demand) else 0.0,
                risk_score=float(risk_score) if not pd.isna(risk_score) else 0.5,
                risk_category=str(risk_category) if not pd.isna(risk_category) else 'unknown',
                trend=str(forecast_trend) if not pd.isna(forecast_trend) else 'stable',
                last_updated=datetime.now()
            )
            skills.append(skill)
        except Exception as e:
            logger.warning(f"Error parsing skill row {idx}: {e}, row data: {row.to_dict()}")
            continue
    
    logger.info(f"Successfully parsed {len(skills)} skills from {len(df)} rows")
    return skills


# IMPORTANT: Specific routes must come BEFORE parameterized routes
# FastAPI matches routes in order, so /high-risk and /emerging must come before /{skill_name}
@router.get("/high-risk", response_model=List[Skill])
async def get_high_risk_skills(limit: Optional[int] = Query(10, ge=1, le=100, description="Number of skills to return")):
    """
    Get skills with high obsolescence risk (≥70%).
    
    Skills are filtered by risk_score >= RISK_THRESHOLD_HIGH (0.7).
    If no skills meet the threshold, returns top risk scores anyway.
    
    Args:
        limit: Maximum number of skills to return (1-100, default: 10)
    
    Returns:
        List[Skill]: List of high-risk skills sorted by risk score (descending)
    
    Example:
        GET /skills/high-risk?limit=20
    """
    df = _load_latest_processed_data()
    
    if df.empty:
        logger.warning("No data available for high-risk skills")
        return []
    
    # Check if risk_score column exists
    if 'risk_score' not in df.columns:
        logger.warning("risk_score column not found in data")
        return []
    
    # Log risk score statistics for debugging
    risk_scores = df['risk_score'].dropna()
    if len(risk_scores) > 0:
        logger.info(f"Risk score stats - Min: {risk_scores.min():.3f}, Max: {risk_scores.max():.3f}, Mean: {risk_scores.mean():.3f}, Threshold: {settings.RISK_THRESHOLD_HIGH}")
        logger.info(f"Skills above threshold: {len(risk_scores[risk_scores >= settings.RISK_THRESHOLD_HIGH])}")
    
    # Filter high risk - use proper DataFrame column access
    high_risk_df = df[df['risk_score'] >= settings.RISK_THRESHOLD_HIGH].copy()
    
    if high_risk_df.empty:
        logger.info(f"No skills found with risk_score >= {settings.RISK_THRESHOLD_HIGH}")
        # If no skills meet threshold, return top risk scores anyway (for demonstration)
        if len(risk_scores) > 0:
            # Get top risk scores (even if below threshold)
            high_risk_df = df.nlargest(limit, 'risk_score').copy()
            logger.info(f"Returning top {len(high_risk_df)} risk scores (below threshold)")
            # Log top risk scores for debugging
            top_risks = df.nlargest(5, 'risk_score')[['skill', 'risk_score']].to_dict('records')
            logger.info(f"Top 5 risk scores: {top_risks}")
        else:
            return []
    
    # Sort by risk score descending
    high_risk_df = high_risk_df.sort_values('risk_score', ascending=False)
    
    # Limit
    high_risk_df = high_risk_df.head(limit)
    
    logger.info(f"Found {len(high_risk_df)} high-risk skills (threshold: {settings.RISK_THRESHOLD_HIGH})")
    
    skills = []
    for idx, row in high_risk_df.iterrows():
        try:
            # Get skill name - required field
            skill_name = row.get('skill') if 'skill' in row else row.get('skill', 'Unknown')
            if pd.isna(skill_name) or not skill_name:
                logger.warning(f"Row {idx} has empty skill name, skipping")
                continue
            
            # Get values with proper NaN handling
            current_demand = row.get('current_demand', 0) if 'current_demand' in row else 0
            forecast_demand = row.get('forecast_demand', current_demand) if 'forecast_demand' in row else current_demand
            risk_score = row.get('risk_score', 0.5) if 'risk_score' in row else 0.5
            risk_category = row.get('risk_category', 'high') if 'risk_category' in row else 'high'
            forecast_trend = row.get('forecast_trend', 'decreasing') if 'forecast_trend' in row else 'decreasing'
            
            skill = Skill(
                name=str(skill_name),
                normalized_name=str(skill_name),
                current_demand=float(current_demand) if not pd.isna(current_demand) else 0.0,
                forecast_demand=float(forecast_demand) if not pd.isna(forecast_demand) else float(current_demand) if not pd.isna(current_demand) else 0.0,
                risk_score=float(risk_score) if not pd.isna(risk_score) else 0.5,
                risk_category=str(risk_category) if not pd.isna(risk_category) else 'high',
                trend=str(forecast_trend) if not pd.isna(forecast_trend) else 'decreasing',
                last_updated=datetime.now()
            )
            skills.append(skill)
        except Exception as e:
            logger.warning(f"Error parsing skill row {idx}: {e}, row data: {dict(row)}")
            continue
    
    logger.info(f"Returning {len(skills)} high-risk skills")
    return skills


@router.get("/emerging", response_model=List[Skill])
async def get_emerging_skills(limit: Optional[int] = Query(10, ge=1, le=100, description="Number of skills to return")):
    """
    Get emerging skills with low obsolescence risk and high growth potential.
    
    Uses progressive filtering:
    1. risk <= 0.3 AND growth > 20% (strict)
    2. risk <= 0.3 AND growth > 5% (relaxed)
    3. risk <= 0.3 AND growth > 0% (any positive)
    4. Top low-risk skills by growth (fallback)
    
    Args:
        limit: Maximum number of skills to return (1-100, default: 10)
    
    Returns:
        List[Skill]: List of emerging skills sorted by growth (descending)
    
    Example:
        GET /skills/emerging?limit=25
    """
    df = _load_latest_processed_data()
    
    if df.empty:
        logger.warning("No data available for emerging skills")
        return []
    
    # Filter low risk and high growth
    # Check if required columns exist
    if 'risk_score' not in df.columns:
        logger.warning("risk_score column not found")
        return []
    
    if 'job_posting_growth' not in df.columns:
        logger.warning("job_posting_growth column not found")
        return []
    
    # Log statistics for debugging
    risk_scores = df['risk_score'].dropna()
    growth_scores = df['job_posting_growth'].dropna()
    if len(risk_scores) > 0 and len(growth_scores) > 0:
        logger.info(f"Emerging filter - Risk threshold: {settings.RISK_THRESHOLD_LOW}, Growth threshold: 20")
        logger.info(f"Risk scores - Min: {risk_scores.min():.3f}, Max: {risk_scores.max():.3f}")
        logger.info(f"Growth scores - Min: {growth_scores.min():.3f}, Max: {growth_scores.max():.3f}")
    
    # Filter: low risk (<= 0.3) AND positive growth
    # Start with strict criteria, then relax if needed
    growth_threshold = 20.0
    
    emerging_df = df[
        (df['risk_score'] <= settings.RISK_THRESHOLD_LOW) &
        (df['job_posting_growth'] > growth_threshold)
    ].copy()
    
    # If no results with strict criteria, relax growth threshold
    if emerging_df.empty:
        logger.info(f"No skills found with risk <= {settings.RISK_THRESHOLD_LOW} AND growth > {growth_threshold}")
        # Try with lower growth threshold (5%)
        growth_threshold = 5.0
        emerging_df = df[
            (df['risk_score'] <= settings.RISK_THRESHOLD_LOW) &
            (df['job_posting_growth'] > growth_threshold)
        ].copy()
        logger.info(f"Trying with growth threshold {growth_threshold}: found {len(emerging_df)} skills")
    
    # If still empty, try with any positive growth
    if emerging_df.empty:
        growth_threshold = 0.0
        emerging_df = df[
            (df['risk_score'] <= settings.RISK_THRESHOLD_LOW) &
            (df['job_posting_growth'] > growth_threshold)
        ].copy()
        logger.info(f"Trying with any positive growth: found {len(emerging_df)} skills")
    
    # If still empty, return top low-risk skills by growth
    if emerging_df.empty:
        logger.info("No skills match emerging criteria, returning top low-risk skills")
        low_risk_df = df[df['risk_score'] <= settings.RISK_THRESHOLD_LOW].copy()
        if not low_risk_df.empty:
            emerging_df = low_risk_df.nlargest(limit, 'job_posting_growth')
            logger.info(f"Returning top {len(emerging_df)} low-risk skills by growth")
        else:
            # Last resort: return top skills by growth regardless of risk
            emerging_df = df.nlargest(limit, 'job_posting_growth').copy()
            logger.info(f"Returning top {len(emerging_df)} skills by growth (regardless of risk)")
    
    # Sort by growth descending
    emerging_df = emerging_df.sort_values('job_posting_growth', ascending=False)
    
    # Limit
    emerging_df = emerging_df.head(limit)
    
    logger.info(f"Found {len(emerging_df)} emerging skills")
    
    skills = []
    for idx, row in emerging_df.iterrows():
        try:
            # Get skill name
            skill_name = row.get('skill') if 'skill' in row else 'Unknown'
            if pd.isna(skill_name) or not skill_name:
                logger.warning(f"Row {idx} has empty skill name, skipping")
                continue
            
            # Get values with proper NaN handling
            current_demand = row.get('current_demand', 0) if 'current_demand' in row else 0
            forecast_demand = row.get('forecast_demand', current_demand) if 'forecast_demand' in row else current_demand
            risk_score = row.get('risk_score', 0.5) if 'risk_score' in row else 0.5
            risk_category = row.get('risk_category', 'low') if 'risk_category' in row else 'low'
            forecast_trend = row.get('forecast_trend', 'increasing') if 'forecast_trend' in row else 'increasing'
            
            skill = Skill(
                name=str(skill_name),
                normalized_name=str(skill_name),
                current_demand=float(current_demand) if not pd.isna(current_demand) else 0.0,
                forecast_demand=float(forecast_demand) if not pd.isna(forecast_demand) else float(current_demand) if not pd.isna(current_demand) else 0.0,
                risk_score=float(risk_score) if not pd.isna(risk_score) else 0.5,
                risk_category=str(risk_category) if not pd.isna(risk_category) else 'low',
                trend=str(forecast_trend) if not pd.isna(forecast_trend) else 'increasing',
                last_updated=datetime.now()
            )
            skills.append(skill)
        except Exception as e:
            logger.warning(f"Error parsing skill row {idx}: {e}, row data: {dict(row)}")
            continue
    
    logger.info(f"Returning {len(skills)} emerging skills")
    return skills


# Parameterized route must come LAST (after all specific routes)
@router.get("/{skill_name}", response_model=SkillDetail)
async def get_skill_detail(skill_name: str):
    """
    Get detailed information about a specific skill.
    
    Returns comprehensive skill data including:
    - Current and forecasted demand
    - Risk score and category
    - Growth metrics (job postings, GitHub, community, research)
    - Skill description and metadata
    - Related skills
    
    Args:
        skill_name: Name of the skill (case-insensitive, URL encoded)
    
    Returns:
        SkillDetail: Detailed skill information with description and metadata
    
    Raises:
        HTTPException: 404 if skill not found or no data available
    
    Example:
        GET /skills/React
        GET /skills/Python
    """
    df = _load_latest_processed_data()
    
    if df.empty:
        raise HTTPException(status_code=404, detail="No data available")
    
    # Find skill (case-insensitive)
    skill_row = df[df['skill'].str.lower() == skill_name.lower()]
    
    if skill_row.empty:
        raise HTTPException(status_code=404, detail=f"Skill '{skill_name}' not found")
    
    row = skill_row.iloc[0]
    
    try:
        # Get values with proper NaN handling
        skill_name_val = row.get('skill', skill_name) if 'skill' in row else skill_name
        current_demand = row.get('current_demand', 0) if 'current_demand' in row else 0
        forecast_demand = row.get('forecast_demand', current_demand) if 'forecast_demand' in row else current_demand
        risk_score = row.get('risk_score', 0.5) if 'risk_score' in row else 0.5
        risk_category = row.get('risk_category', 'unknown') if 'risk_category' in row else 'unknown'
        forecast_trend = row.get('forecast_trend', 'stable') if 'forecast_trend' in row else 'stable'
        job_posting_growth = row.get('job_posting_growth', 0) if 'job_posting_growth' in row else 0
        github_velocity = row.get('github_velocity', 0) if 'github_velocity' in row else 0
        community_decay = row.get('community_decay', 0) if 'community_decay' in row else 0
        research_trend = row.get('research_trend', 0) if 'research_trend' in row else 0
        
        # Get skill description and metadata
        skill_info = get_skill_description(str(skill_name_val))
        if not skill_info:
            skill_info = get_default_description(str(skill_name_val))
        
        skill_detail = SkillDetail(
            name=str(skill_name_val),
            normalized_name=str(skill_name_val),
            current_demand=float(current_demand) if not pd.isna(current_demand) else 0.0,
            forecast_demand=float(forecast_demand) if not pd.isna(forecast_demand) else float(current_demand) if not pd.isna(current_demand) else 0.0,
            risk_score=float(risk_score) if not pd.isna(risk_score) else 0.5,
            risk_category=str(risk_category) if not pd.isna(risk_category) else 'unknown',
            trend=str(forecast_trend) if not pd.isna(forecast_trend) else 'stable',
            last_updated=datetime.now(),
            job_posting_growth=float(job_posting_growth) if not pd.isna(job_posting_growth) else 0.0,
            github_velocity=float(github_velocity) if not pd.isna(github_velocity) else 0.0,
            community_mentions=float(community_decay) if not pd.isna(community_decay) else 0.0,
            research_citations=float(research_trend) if not pd.isna(research_trend) else 0.0,
            related_skills=[],  # Would be populated from dependency graph
            historical_data=[],  # Would be populated from historical data
            description=skill_info.get('description', ''),
            category=skill_info.get('category', 'Technology'),
            popularity=skill_info.get('popularity', 'Medium'),
            trend_info=skill_info.get('trend', 'Stable')
        )
        
        logger.info(f"Successfully created skill detail for: {skill_name}")
        return skill_detail
    except Exception as e:
        logger.error(f"Error creating skill detail for {skill_name}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error processing skill data: {str(e)}")

