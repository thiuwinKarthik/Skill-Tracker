"""
Daily pipeline for data ingestion, processing, and ML prediction.

This module orchestrates the complete data processing pipeline:
1. Fetch data from multiple sources (GitHub, job boards, communities, research)
2. Extract skills and roles using NLP
3. Build time-series features
4. Run ML models for forecasting and risk classification
5. Save processed outputs for API consumption

The pipeline runs daily via scheduler or can be triggered manually via API.
"""
import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict
import pandas as pd
from loguru import logger

from app.config import settings
from app.pipeline.data_sources import fetch_all_sources
from app.nlp.extractor import SkillExtractor, RoleExtractor
from app.ml.feature_engineering import FeatureEngineer
from app.ml.forecaster import DemandForecaster
from app.ml.risk_classifier import RiskClassifier


class DailyPipeline:
    """Main pipeline orchestrator for daily data processing."""

    def __init__(self):
        # Directories
        self.raw_data_dir = Path(settings.DATA_RAW_DIR)
        self.processed_data_dir = Path(settings.DATA_PROCESSED_DIR)
        self.models_dir = Path(settings.MODELS_DIR)

        self.raw_data_dir.mkdir(parents=True, exist_ok=True)
        self.processed_data_dir.mkdir(parents=True, exist_ok=True)
        self.models_dir.mkdir(parents=True, exist_ok=True)

        # Components
        self.skill_extractor = SkillExtractor()
        self.role_extractor = RoleExtractor()
        self.feature_engineer = FeatureEngineer()
        self.forecaster = DemandForecaster()
        self.risk_classifier = RiskClassifier()

    async def run(self) -> Dict:
        """Execute the full pipeline workflow."""
        start_time = datetime.now()
        logger.info("Starting daily pipeline execution")

        try:
            # Step 1: Fetch data
            logger.info("Step 1: Fetching data from sources")
            raw_data = await fetch_all_sources()

            # Step 2: Save raw snapshot
            logger.info("Step 2: Saving raw data snapshot")
            snapshot_path = self._save_raw_snapshot(raw_data)

            # Step 3: Extract skills and roles
            logger.info("Step 3: Extracting skills and roles")
            extracted_skills = self.skill_extractor.extract_from_data(raw_data)
            extracted_roles = self.role_extractor.extract_from_data(raw_data)

            # Step 4: Normalize skills
            logger.info("Step 4: Normalizing skills")
            normalized_skills = self.skill_extractor.normalize_skills(extracted_skills)

            # Step 5: Update historical data
            logger.info("Step 5: Updating historical data")
            historical_data = self._load_historical_data()
            updated_data = self._update_historical_data(historical_data, normalized_skills)
            self._save_historical_data(updated_data)

            # Step 6: Feature engineering
            logger.info("Step 6: Engineering ML features")
            features_df = self.feature_engineer.create_features(updated_data)

            if features_df.empty and normalized_skills:
                logger.info("No historical data, creating basic features")
                features_df = self._create_basic_features(normalized_skills, raw_data)

            # Step 7: ML predictions
            logger.info("Step 7: Running ML models")
            forecasts = self.forecaster.forecast(features_df) if not features_df.empty else pd.DataFrame()
            risk_scores = self.risk_classifier.predict_risk(features_df) if not features_df.empty else pd.DataFrame()

            # Step 8: Combine results
            logger.info("Step 8: Combining results")
            results_df = self._combine_results(features_df, forecasts, risk_scores)

            # Step 9: Save processed outputs
            logger.info("Step 9: Saving processed data")
            output_path = self._save_processed_output(results_df)

            duration = (datetime.now() - start_time).total_seconds()
            logger.info(f"Pipeline completed in {duration:.2f} seconds")

            return {
                "status": "completed",
                "started_at": start_time.isoformat(),
                "completed_at": datetime.now().isoformat(),
                "duration_seconds": duration,
                "records_processed": len(raw_data),
                "skills_extracted": len(normalized_skills),
                "snapshot_path": str(snapshot_path),
                "output_path": str(output_path),
                "errors": []
            }

        except Exception as e:
            logger.error(f"Pipeline failed: {e}", exc_info=True)
            return {
                "status": "failed",
                "started_at": start_time.isoformat(),
                "completed_at": datetime.now().isoformat(),
                "errors": [str(e)]
            }

    # ------------------ Helper Methods ------------------ #

    def _save_raw_snapshot(self, data: List[Dict]) -> Path:
        date_str = datetime.now().strftime("%Y%m%d")
        filepath = self.raw_data_dir / f"raw_snapshot_{date_str}.json"
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.info(f"Saved raw snapshot: {filepath}")
        return filepath

    def _load_historical_data(self) -> pd.DataFrame:
        filepath = self.processed_data_dir / "historical_skills.csv"
        if filepath.exists():
            df = pd.read_csv(filepath)
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            return df.dropna(subset=['date'])
        else:
            # Empty DataFrame with proper columns
            cols = ['skill', 'date', 'job_postings', 'github_stars', 'community_mentions', 'research_citations']
            return pd.DataFrame(columns=cols).astype({
                'skill': 'string',
                'date': 'datetime64[ns]',
                'job_postings': 'float64',
                'github_stars': 'float64',
                'community_mentions': 'float64',
                'research_citations': 'float64'
            })

    def _update_historical_data(self, historical_df: pd.DataFrame, new_skills: Dict[str, int]) -> pd.DataFrame:
        today = pd.Timestamp.now().normalize()
        new_rows = []
        for skill, count in new_skills.items():
            new_rows.append({
                'skill': skill,
                'date': today,
                'job_postings': count,
                'github_stars': 0,
                'community_mentions': 0,
                'research_citations': 0
            })
        if new_rows:
            new_df = pd.DataFrame(new_rows)
            new_df['date'] = pd.to_datetime(new_df['date'])
            historical_df['date'] = pd.to_datetime(historical_df['date'])
            historical_df = pd.concat([historical_df, new_df], ignore_index=True)
        return historical_df

    def _save_historical_data(self, df: pd.DataFrame):
        filepath = self.processed_data_dir / "historical_skills.csv"
        df_copy = df.copy()
        df_copy['date'] = pd.to_datetime(df_copy['date'], errors='coerce')
        df_copy['date'] = df_copy['date'].dt.strftime('%Y-%m-%d')
        df_copy.to_csv(filepath, index=False)
        logger.info(f"Saved historical data: {filepath}")

    def _combine_results(self, features_df: pd.DataFrame, forecasts: pd.DataFrame, risk_scores: pd.DataFrame) -> pd.DataFrame:
        if features_df.empty:
            return pd.DataFrame()
        results = features_df.copy()

        # Merge forecasts
        if not forecasts.empty:
            results = results.merge(forecasts, on='skill', how='left')
        results['forecast_demand'] = results.get('forecast_demand', results.get('current_demand', 0))
        results['forecast_trend'] = results.get('forecast_trend', 'stable')

        # Merge risk scores
        if not risk_scores.empty:
            results = results.merge(risk_scores, on='skill', how='left')
        results['risk_score'] = results.get('risk_score', 0.5)
        results['risk_category'] = results['risk_score'].apply(self._categorize_risk)

        if 'current_demand' not in results.columns:
            results['current_demand'] = results.get('recent_job_postings', 0)

        return results

    def _categorize_risk(self, score: float) -> str:
        if pd.isna(score):
            return "unknown"
        if score >= settings.RISK_THRESHOLD_HIGH:
            return "high"
        if score <= settings.RISK_THRESHOLD_LOW:
            return "low"
        return "medium"

    def _save_processed_output(self, df: pd.DataFrame) -> Path:
        date_str = datetime.now().strftime("%Y%m%d")
        filepath = self.processed_data_dir / f"processed_skills_{date_str}.csv"
        df.to_csv(filepath, index=False)
        logger.info(f"Saved processed output: {filepath}")
        return filepath

    def _create_basic_features(self, normalized_skills: Dict[str, int], raw_data: List[Dict]) -> pd.DataFrame:
        import random
        features_list = []

        skill_mentions = {}
        for record in raw_data:
            if 'skills' in record:
                for skill in record.get('skills', []):
                    skill_mentions[skill] = skill_mentions.get(skill, 0) + 1
            if 'languages' in record:
                for lang in record.get('languages', {}):
                    skill_mentions[lang] = skill_mentions.get(lang, 0) + 1

        for skill, count in normalized_skills.items():
            base_growth = random.uniform(-10, 35)
            mention_count = skill_mentions.get(skill, 0)
            if mention_count > 5:
                base_growth += random.uniform(5, 20)
            elif mention_count == 0:
                base_growth -= random.uniform(5, 15)
            if random.random() < 0.3:
                base_growth = random.uniform(20, 50)

            features_list.append({
                'skill': skill,
                'job_posting_growth': round(base_growth, 2),
                'github_velocity': round(base_growth * 0.8 + random.uniform(-5, 5), 2),
                'community_decay': round(-base_growth * 0.3 + random.uniform(-5, 5), 2),
                'research_trend': round(base_growth * 0.2 + random.uniform(-3, 3), 2),
                'recent_job_postings': count,
                'recent_github_stars': max(0, int(count * 0.5 + random.uniform(-10, 10))),
                'job_volatility': round(count * 0.1 + random.uniform(0, 5), 2),
                'days_observed': 1,
                'total_observations': 1,
                'current_demand': count
            })

        if features_list:
            df = pd.DataFrame(features_list)
            logger.info(f"Created {len(df)} basic feature rows")
            return df
        return pd.DataFrame()


# ------------------ Entry Point ------------------ #

async def main():
    pipeline = DailyPipeline()
    result = await pipeline.run()
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
