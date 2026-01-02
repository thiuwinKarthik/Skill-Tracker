"""
Risk classification model for skill obsolescence prediction.

Calculates obsolescence risk scores (0.0-1.0) based on multiple factors:
- Job posting growth trends
- Community activity decay
- Recent activity levels
- Market volatility

Uses rule-based approach with potential for ML model integration.
Higher scores indicate higher risk of obsolescence.
"""
import pandas as pd
import numpy as np
from typing import Dict
from loguru import logger
import joblib
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler


class RiskClassifier:
    """
    Classify obsolescence risk for technology skills.
    
    Calculates risk scores based on growth trends, community activity,
    and market signals. Scores range from 0.0 (low risk) to 1.0 (high risk).
    Currently uses rule-based approach with extensibility for ML models.
    """
    
    def __init__(self):
        """Initialize risk classifier."""
        self.models_dir = Path("backend/app/models")
        self.models_dir.mkdir(parents=True, exist_ok=True)
        self.model = None
        self.scaler = StandardScaler()
        self.feature_columns = [
            'job_posting_growth',
            'github_velocity',
            'community_decay',
            'research_trend',
            'recent_job_postings',
            'recent_github_stars',
            'job_volatility',
        ]
    
    def predict_risk(self, features_df: pd.DataFrame) -> pd.DataFrame:
        """Predict obsolescence risk for all skills."""
        if features_df.empty:
            return pd.DataFrame(columns=['skill', 'risk_score'])
        
        # Prepare features
        X = self._prepare_features(features_df)
        
        # Predict risk scores
        risk_scores = self._calculate_risk_scores(features_df, X)
        
        return pd.DataFrame([
            {'skill': skill, 'risk_score': score}
            for skill, score in risk_scores.items()
        ])
    
    def _prepare_features(self, features_df: pd.DataFrame) -> np.ndarray:
        """Prepare feature matrix."""
        # Select and fill missing values
        X = features_df[self.feature_columns].copy()
        X = X.fillna(0)
        
        # Normalize
        try:
            X_scaled = self.scaler.fit_transform(X)
        except Exception as e:
            logger.warning(f"Scaling failed: {e}, using raw features")
            X_scaled = X.values
        
        return X_scaled
    
    def _calculate_risk_scores(self, features_df: pd.DataFrame, X: np.ndarray) -> Dict[str, float]:
        """Calculate risk scores using rule-based approach (can be replaced with ML model)."""
        risk_scores = {}
        
        for idx, row in features_df.iterrows():
            skill = row['skill']
            
            # Rule-based risk calculation
            risk_factors = []
            
            # Negative growth indicates risk
            growth = row.get('job_posting_growth', 0)
            if growth < -20:
                risk_factors.append(0.4)
            elif growth < -10:
                risk_factors.append(0.2)
            elif growth < 0:
                risk_factors.append(0.1)
            
            # High community decay indicates risk
            decay = row.get('community_decay', 0)
            if decay > 30:
                risk_factors.append(0.3)
            elif decay > 15:
                risk_factors.append(0.15)
            
            # Low recent activity indicates risk
            recent_jobs = row.get('recent_job_postings', 0)
            if recent_jobs == 0:
                risk_factors.append(0.2)
            elif recent_jobs < 5:
                risk_factors.append(0.1)
            
            # High volatility indicates uncertainty/risk
            volatility = row.get('job_volatility', 0)
            if volatility > 50:
                risk_factors.append(0.1)
            
            # Combine risk factors (sum with cap at 1.0)
            risk_score = min(1.0, sum(risk_factors))
            
            # Ensure we have some variation in risk scores
            # If no risk factors, assign a base risk based on growth
            if risk_score == 0:
                # Skills with negative growth get some base risk
                if growth < 0:
                    risk_score = abs(growth) / 100.0  # Convert negative growth to risk
                    risk_score = min(0.6, risk_score)  # Cap at 0.6
                else:
                    risk_score = 0.1  # Low base risk for stable/positive growth
            
            # Add some randomness for demonstration (remove in production)
            risk_score = min(1.0, risk_score + np.random.uniform(-0.05, 0.05))
            risk_score = max(0.0, risk_score)
            
            risk_scores[skill] = round(risk_score, 3)
        
        return risk_scores
    
    def train_model(self, training_data: pd.DataFrame, labels: pd.Series):
        """Train ML model on historical data (for future use)."""
        # This would train a proper ML model given labeled historical data
        # For now, we use rule-based approach
        logger.info("Training risk classifier model")
        # Placeholder for future ML model training
        pass

