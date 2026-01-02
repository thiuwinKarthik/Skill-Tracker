"""
Feature engineering for ML models.

This module transforms raw historical data into ML-ready features including:
- Growth rates (job postings, GitHub stars, research citations)
- Decay rates (community mentions)
- Recent activity metrics
- Volatility measures
- Time-series statistics

Features are calculated per skill and aggregated over time windows.
"""
import pandas as pd
import numpy as np
from typing import Dict
from datetime import datetime, timedelta
from loguru import logger


class FeatureEngineer:
    """
    Create ML-ready features from historical time-series data.
    
    Calculates statistical features for each skill including growth rates,
    velocity metrics, and trend indicators used by forecasting and risk models.
    """
    
    def __init__(self):
        """Initialize feature engineer."""
        pass
    
    def create_features(self, historical_df: pd.DataFrame) -> pd.DataFrame:
        """Create features for each skill."""
        if historical_df.empty:
            logger.warning("Empty historical data, returning empty features")
            return pd.DataFrame()
        
        features_list = []
        
        # Group by skill
        for skill, group in historical_df.groupby('skill'):
            # Sort by date
            group = group.sort_values('date')
            
            # Calculate features
            features = self._calculate_skill_features(skill, group)
            features_list.append(features)
        
        if features_list:
            features_df = pd.DataFrame(features_list)
            return features_df
        else:
            return pd.DataFrame()
    
    def _calculate_skill_features(self, skill: str, skill_data: pd.DataFrame) -> Dict:
        """Calculate features for a single skill."""
        # Ensure date column is Timestamp type (work on a copy)
        skill_data = skill_data.copy()
        skill_data['date'] = pd.to_datetime(skill_data['date'])
        
        # Basic statistics
        latest = skill_data.iloc[-1]
        oldest = skill_data.iloc[0]
        
        # Time range - handle both Timestamp and datetime objects
        if len(skill_data) > 1:
            date_diff = pd.to_datetime(latest['date']) - pd.to_datetime(oldest['date'])
            days_span = date_diff.days
        else:
            days_span = 1
        
        # Growth rates
        job_posting_growth = self._calculate_growth_rate(
            skill_data['job_postings'].values
        )
        github_velocity = self._calculate_growth_rate(
            skill_data['github_stars'].values
        )
        community_decay = self._calculate_decay_rate(
            skill_data['community_mentions'].values
        )
        research_trend = self._calculate_growth_rate(
            skill_data['research_citations'].values
        )
        
        # Recent activity (last 30 days)
        # Ensure date column is Timestamp for comparison (work on a copy to avoid modifying original)
        skill_data = skill_data.copy()
        skill_data['date'] = pd.to_datetime(skill_data['date'])
        recent_cutoff = pd.Timestamp.now().normalize() - timedelta(days=30)
        recent_data = skill_data[skill_data['date'] >= recent_cutoff]
        
        recent_job_postings = recent_data['job_postings'].sum() if not recent_data.empty else 0
        recent_github_stars = recent_data['github_stars'].sum() if not recent_data.empty else 0
        
        # Volatility
        job_volatility = skill_data['job_postings'].std() if len(skill_data) > 1 else 0
        
        return {
            'skill': skill,
            'job_posting_growth': job_posting_growth,
            'github_velocity': github_velocity,
            'community_decay': community_decay,
            'research_trend': research_trend,
            'recent_job_postings': recent_job_postings,
            'recent_github_stars': recent_github_stars,
            'job_volatility': job_volatility,
            'days_observed': days_span,
            'total_observations': len(skill_data),
            'current_demand': latest['job_postings'] if not skill_data.empty else 0,
        }
    
    def _calculate_growth_rate(self, values: np.ndarray) -> float:
        """Calculate growth rate (percentage change)."""
        if len(values) < 2:
            return 0.0
        
        # Remove zeros to avoid division issues
        values = values[values > 0]
        if len(values) < 2:
            return 0.0
        
        first = values[0]
        last = values[-1]
        
        if first == 0:
            return 100.0 if last > 0 else 0.0
        
        return ((last - first) / first) * 100
    
    def _calculate_decay_rate(self, values: np.ndarray) -> float:
        """Calculate decay rate (negative growth)."""
        growth = self._calculate_growth_rate(values)
        return -growth  # Decay is negative growth

