"""
Data source connectors for fetching technology signals.
"""
import requests
import aiohttp
from typing import List, Dict, Optional
from datetime import datetime
from loguru import logger
from bs4 import BeautifulSoup
import time


class DataSource:
    """Base class for data sources."""
    
    def __init__(self, rate_limit_delay: float = 1.0):
        self.rate_limit_delay = rate_limit_delay
        self.last_request_time = 0
    
    def _rate_limit(self):
        """Enforce rate limiting."""
        current_time = time.time()
        elapsed = current_time - self.last_request_time
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
        self.headers = {}
        if api_key:
            self.headers["Authorization"] = f"token {api_key}"
    
    async def fetch(self) -> List[Dict]:
        """Fetch trending repositories and technologies."""
        self._rate_limit()
        results = []
        
        try:
            # Search for trending repositories
            async with aiohttp.ClientSession() as session:
                # Search for repositories with high activity
                search_url = f"{self.base_url}/search/repositories"
                params = {
                    "q": "stars:>1000 language:python language:javascript language:java language:go",
                    "sort": "stars",
                    "order": "desc",
                    "per_page": 50
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
        """Get language statistics for a repository."""
        try:
            async with session.get(languages_url, headers=self.headers) as response:
                if response.status == 200:
                    return await response.json()
        except Exception as e:
            logger.error(f"Error fetching languages: {e}")
        return {}


class JobBoardSource(DataSource):
    """Job board data source (mock implementation - replace with real API)."""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(rate_limit_delay=2.0)
        self.api_key = api_key
    
    async def fetch(self) -> List[Dict]:
        """Fetch job postings data."""
        self._rate_limit()
        results = []
        
        # Mock implementation - replace with actual job board API
        # Examples: Indeed API, LinkedIn API, etc.
        logger.info("Fetching job board data (mock implementation)")
        
        # Simulated job postings with realistic current trends
        # These reflect real 2024 tech trends
        mock_jobs = [
            {
                "source": "job_board",
                "title": "Senior React Developer",
                "description": "Looking for React, TypeScript, Node.js developer with Next.js experience",
                "skills": ["React", "TypeScript", "Node.js", "Next.js"],
                "timestamp": datetime.now().isoformat()
            },
            {
                "source": "job_board",
                "title": "Python ML Engineer",
                "description": "Python, TensorFlow, PyTorch, scikit-learn required",
                "skills": ["Python", "TensorFlow", "PyTorch", "scikit-learn"],
                "timestamp": datetime.now().isoformat()
            },
            {
                "source": "job_board",
                "title": "Full Stack Developer",
                "description": "React, Python, FastAPI, PostgreSQL",
                "skills": ["React", "Python", "FastAPI", "PostgreSQL"],
                "timestamp": datetime.now().isoformat()
            },
            {
                "source": "job_board",
                "title": "DevOps Engineer",
                "description": "Kubernetes, Docker, AWS, Terraform",
                "skills": ["Kubernetes", "Docker", "AWS", "Terraform"],
                "timestamp": datetime.now().isoformat()
            },
            {
                "source": "job_board",
                "title": "Data Engineer",
                "description": "Python, Spark, Airflow, Snowflake",
                "skills": ["Python", "Spark", "Airflow", "Snowflake"],
                "timestamp": datetime.now().isoformat()
            },
            {
                "source": "job_board",
                "title": "Frontend Developer",
                "description": "Vue.js, JavaScript, Tailwind CSS",
                "skills": ["Vue.js", "JavaScript", "Tailwind CSS"],
                "timestamp": datetime.now().isoformat()
            },
            {
                "source": "job_board",
                "title": "Backend Developer",
                "description": "Go, gRPC, Microservices, Redis",
                "skills": ["Go", "gRPC", "Microservices", "Redis"],
                "timestamp": datetime.now().isoformat()
            },
            {
                "source": "job_board",
                "title": "Rust Systems Engineer",
                "description": "Rust, Systems Programming, Performance",
                "skills": ["Rust", "Systems Programming"],
                "timestamp": datetime.now().isoformat()
            }
        ]
        
        results.extend(mock_jobs)
        return results


class CommunitySource(DataSource):
    """Community forums and discussion boards (mock implementation)."""
    
    def __init__(self):
        super().__init__(rate_limit_delay=1.5)
    
    async def fetch(self) -> List[Dict]:
        """Fetch community mentions."""
        self._rate_limit()
        results = []
        
        # Mock implementation - replace with actual community APIs
        # Examples: Stack Overflow API, Reddit API, etc.
        logger.info("Fetching community data (mock implementation)")
        
        # Realistic community mentions reflecting current trends
        mock_mentions = [
            {
                "source": "community",
                "platform": "stackoverflow",
                "topic": "React vs Vue.js vs Angular 2024",
                "mentions": ["React", "Vue.js", "Angular"],
                "engagement": 250,
                "timestamp": datetime.now().isoformat()
            },
            {
                "source": "community",
                "platform": "reddit",
                "topic": "Python vs Go for backend",
                "mentions": ["Python", "Go"],
                "engagement": 180,
                "timestamp": datetime.now().isoformat()
            },
            {
                "source": "community",
                "platform": "stackoverflow",
                "topic": "TypeScript adoption",
                "mentions": ["TypeScript", "JavaScript"],
                "engagement": 320,
                "timestamp": datetime.now().isoformat()
            },
            {
                "source": "community",
                "platform": "reddit",
                "topic": "Rust for systems programming",
                "mentions": ["Rust", "C++"],
                "engagement": 150,
                "timestamp": datetime.now().isoformat()
            }
        ]
        
        results.extend(mock_mentions)
        return results


class ResearchSource(DataSource):
    """Research papers and academic sources (mock implementation)."""
    
    def __init__(self):
        super().__init__(rate_limit_delay=2.0)
    
    async def fetch(self) -> List[Dict]:
        """Fetch research citations."""
        self._rate_limit()
        results = []
        
        # Mock implementation - replace with actual research APIs
        # Examples: arXiv API, Google Scholar API, etc.
        logger.info("Fetching research data (mock implementation)")
        
        mock_research = [
            {
                "source": "research",
                "title": "Machine Learning in Production",
                "technologies": ["Python", "TensorFlow", "Kubernetes"],
                "citations": 45,
                "timestamp": datetime.now().isoformat()
            }
        ]
        
        results.extend(mock_research)
        return results


async def fetch_all_sources(github_key: Optional[str] = None, job_board_key: Optional[str] = None) -> List[Dict]:
    """Fetch data from all configured sources."""
    sources = [
        GitHubSource(api_key=github_key),
        JobBoardSource(api_key=job_board_key),
        CommunitySource(),
        ResearchSource()
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

