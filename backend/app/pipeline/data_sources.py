"""
Data source connectors for fetching technology signals (GitHub, Job Board, Community, Research).
"""
import aiohttp
from typing import List, Dict, Optional
from datetime import datetime
from loguru import logger
import time

from app.config import settings


class DataSource:
    """Base class for data sources."""

    def __init__(self, rate_limit_delay: float = 1.0):
        self.rate_limit_delay = rate_limit_delay
        self.last_request_time = 0

    def _rate_limit(self):
        """Enforce rate limiting."""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - elapsed)
        self.last_request_time = time.time()

    async def fetch(self) -> List[Dict]:
        """Fetch data from source. Must be implemented by subclasses."""
        raise NotImplementedError


class GitHubSource(DataSource):
    """GitHub API data source for repository trends."""

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(rate_limit_delay=0.5)
        self.api_key = api_key
        self.base_url = "https://api.github.com"
        self.headers = {"Authorization": f"token {api_key}"} if api_key else {}

    async def fetch(self) -> List[Dict]:
        self._rate_limit()
        results = []

        try:
            async with aiohttp.ClientSession() as session:
                search_url = f"{self.base_url}/search/repositories"
                params = {
                    "q": "stars:>1000 language:python language:javascript language:java language:go",
                    "sort": "stars",
                    "order": "desc",
                    "per_page": 50,
                }

                async with session.get(search_url, headers=self.headers, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        for repo in data.get("items", [])[:20]:
                            languages = await self._get_repo_languages(repo["languages_url"], session)
                            results.append({
                                "source": "github",
                                "repo_name": repo["name"],
                                "stars": repo["stargazers_count"],
                                "forks": repo["forks_count"],
                                "languages": languages,
                                "created_at": repo["created_at"],
                                "updated_at": repo["updated_at"],
                                "timestamp": datetime.now().isoformat()
                            })
                    else:
                        logger.warning(f"GitHub API returned status {response.status}")
        except Exception as e:
            logger.error(f"Error fetching from GitHub: {e}")

        return results

    async def _get_repo_languages(self, languages_url: str, session: aiohttp.ClientSession) -> Dict[str, int]:
        try:
            async with session.get(languages_url, headers=self.headers) as response:
                if response.status == 200:
                    return await response.json()
        except Exception as e:
            logger.error(f"Error fetching repo languages: {e}")
        return {}


class JobBoardSource(DataSource):
    """Adzuna Job Board data source using API key and App ID."""

    def __init__(self, api_key: Optional[str] = None, app_id: Optional[str] = None):
        super().__init__(rate_limit_delay=2.0)
        self.api_key = api_key
        self.app_id = app_id
        self.base_url = "https://api.adzuna.com/v1/api/jobs/us/search/1"

    async def fetch(self) -> List[Dict]:
        self._rate_limit()
        results = []

        if not self.api_key or not self.app_id:
            logger.error("JobBoard API key or App ID missing")
            return results

        params = {
            "app_id": self.app_id,
            "app_key": self.api_key,
            "results_per_page": 50,
            "content-type": "application/json",
            "what": "python OR react OR javascript OR java OR go",
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.base_url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        for job in data.get("results", []):
                            results.append({
                                "source": "job_board",
                                "title": job.get("title"),
                                "description": job.get("description"),
                                "skills": job.get("tags", []),
                                "company": job.get("company", {}).get("display_name", ""),
                                "location": job.get("location", {}).get("display_name", ""),
                                "timestamp": datetime.now().isoformat()
                            })
                    else:
                        logger.warning(f"Job Board API returned status {response.status}")
        except Exception as e:
            logger.error(f"Error fetching from Job Board: {e}")

        return results


class CommunitySource(DataSource):
    """Community forums and discussion boards (mock or real API)."""

    async def fetch(self) -> List[Dict]:
        self._rate_limit()
        logger.info("Community source fetching (replace with real API if needed)")
        return []  # TODO: Implement StackOverflow / Reddit API here if required


class ResearchSource(DataSource):
    """Research papers / citations (mock or real API)."""

    async def fetch(self) -> List[Dict]:
        self._rate_limit()
        logger.info("Research source fetching (replace with real API if needed)")
        return []  # TODO: Implement arXiv / Google Scholar API here if needed


async def fetch_all_sources() -> List[Dict]:
    """Fetch data from all configured sources using API keys from settings."""
    sources = [
        GitHubSource(api_key=settings.GITHUB_API_KEY),
        JobBoardSource(api_key=settings.JOB_BOARD_API_KEY, app_id=settings.JOB_BOARD_APP_ID),
        CommunitySource(),
        ResearchSource(),
    ]

    all_data = []
    for source in sources:
        try:
            data = await source.fetch()
            all_data.extend(data)
            logger.info(f"Fetched {len(data)} records from {source.__class__.__name__}")
        except Exception as e:
            logger.error(f"Error fetching from {source.__class__.__name__}: {e}")

    return all_data
