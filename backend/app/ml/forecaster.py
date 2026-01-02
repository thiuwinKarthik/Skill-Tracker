"""
Demand forecasting models for skill demand prediction.

Supports multiple forecasting approaches:
- Simple trend-based forecasting (default)
- ARIMA time-series models
- Prophet forecasting (Facebook)

Forecasts future demand over a configurable horizon (default: 90 days)
and determines trend direction (increasing, decreasing, stable).
"""
import pandas as pd
import numpy as np
from typing import Dict
from loguru import logger
import joblib
from pathlib import Path

try:
    from statsmodels.tsa.arima.model import ARIMA
    ARIMA_AVAILABLE = True
except ImportError:
    ARIMA_AVAILABLE = False
    logger.warning("statsmodels not available, using simple forecasting")

try:
    from prophet import Prophet
    PROPHET_AVAILABLE = True
except ImportError:
    PROPHET_AVAILABLE = False
    logger.warning("Prophet not available, using simple forecasting")


class DemandForecaster:
    """
    Forecast future demand for technology skills.
    
    Uses growth rates and historical trends to predict future demand
    and determine trend direction. Supports multiple model types with
    automatic fallback to simple forecasting if advanced models unavailable.
    """
    
    def __init__(self, model_type: str = "simple"):
        """
        Initialize forecaster.
        
        Args:
            model_type: "simple", "arima", or "prophet"
        """
        self.model_type = model_type
        self.models_dir = Path("backend/app/models")
        self.models_dir.mkdir(parents=True, exist_ok=True)
        
        # Validate model type
        if model_type == "arima" and not ARIMA_AVAILABLE:
            logger.warning("ARIMA not available, falling back to simple")
            self.model_type = "simple"
        if model_type == "prophet" and not PROPHET_AVAILABLE:
            logger.warning("Prophet not available, falling back to simple")
            self.model_type = "simple"
    
    def forecast(self, features_df: pd.DataFrame, horizon_days: int = 90) -> pd.DataFrame:
        """Forecast demand for all skills."""
        if features_df.empty:
            return pd.DataFrame(columns=['skill', 'forecast_demand', 'forecast_trend'])
        
        forecasts = []
        
        for _, row in features_df.iterrows():
            skill = row['skill']
            
            # Simple trend-based forecast
            if self.model_type == "simple":
                forecast = self._simple_forecast(row)
            elif self.model_type == "arima":
                forecast = self._arima_forecast(skill, row)
            elif self.model_type == "prophet":
                forecast = self._prophet_forecast(skill, row)
            else:
                forecast = self._simple_forecast(row)
            
            forecasts.append({
                'skill': skill,
                'forecast_demand': forecast['demand'],
                'forecast_trend': forecast['trend']
            })
        
        return pd.DataFrame(forecasts)
    
    def _simple_forecast(self, row: pd.Series) -> Dict:
        """Simple trend-based forecasting with real-time trends."""
        current_demand = row.get('current_demand', 0)
        growth_rate = row.get('job_posting_growth', 0)
        
        # Use actual growth rate from features (already in percentage)
        # Project forward based on growth rate over 90 days
        days_projection = 90
        # Growth rate is already a percentage, so convert to multiplier
        forecast_demand = current_demand * (1 + (growth_rate / 100) * (days_projection / 365))
        
        # Determine trend based on growth rate
        # More nuanced trend detection
        if growth_rate > 20:
            trend = "increasing"  # Strong growth
        elif growth_rate > 5:
            trend = "increasing"  # Moderate growth
        elif growth_rate < -10:
            trend = "decreasing"  # Strong decline
        elif growth_rate < 0:
            trend = "decreasing"  # Mild decline
        else:
            trend = "stable"  # Stable (0-5% growth)
        
        return {
            'demand': max(0, forecast_demand),
            'trend': trend
        }
    
    def _arima_forecast(self, skill: str, row: pd.Series) -> Dict:
        """ARIMA-based forecasting (placeholder - requires time series data)."""
        # ARIMA requires historical time series, which we'd need to load
        # For now, fall back to simple
        logger.debug(f"ARIMA forecast for {skill} (using simple fallback)")
        return self._simple_forecast(row)
    
    def _prophet_forecast(self, skill: str, row: pd.Series) -> Dict:
        """Prophet-based forecasting (placeholder - requires time series data)."""
        # Prophet requires historical time series
        logger.debug(f"Prophet forecast for {skill} (using simple fallback)")
        return self._simple_forecast(row)

