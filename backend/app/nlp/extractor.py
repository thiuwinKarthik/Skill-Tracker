"""
NLP-based skill and role extraction.

This module provides functionality to extract technology skills and job roles
from unstructured text data using:
- Pattern matching (regex)
- spaCy NER (Named Entity Recognition)
- Keyword matching
- Skill name normalization

Supports extraction from job postings, GitHub repositories, community discussions,
and research papers.
"""
import re
from typing import List, Dict, Set
from collections import Counter
from loguru import logger

try:
    import spacy
    from spacy import displacy
except ImportError:
    logger.warning("spaCy not installed. Install with: python -m spacy download en_core_web_sm")
    spacy = None


class SkillExtractor:
    """
    Extract and normalize technology skills from text data.
    
    Uses multiple extraction methods:
    - Regex pattern matching for common technologies
    - spaCy NER for entity recognition
    - Direct keyword matching against known skills
    - Normalization to standard skill names
    """
    
    # Skill normalization mapping
    SKILL_MAPPING = {
        "js": "JavaScript",
        "javascript": "JavaScript",
        "ts": "TypeScript",
        "typescript": "TypeScript",
        "py": "Python",
        "python": "Python",
        "java": "Java",
        "cpp": "C++",
        "c++": "C++",
        "c#": "C#",
        "csharp": "C#",
        "go": "Go",
        "golang": "Go",
        "rust": "Rust",
        "php": "PHP",
        "ruby": "Ruby",
        "swift": "Swift",
        "kotlin": "Kotlin",
        "scala": "Scala",
        "react": "React",
        "reactjs": "React",
        "angular": "Angular",
        "angularjs": "Angular",
        "vue": "Vue.js",
        "vuejs": "Vue.js",
        "node": "Node.js",
        "nodejs": "Node.js",
        "spring": "Spring Boot",
        "springboot": "Spring Boot",
        "spring boot": "Spring Boot",
        "django": "Django",
        "flask": "Flask",
        "express": "Express.js",
        "expressjs": "Express.js",
        "tensorflow": "TensorFlow",
        "pytorch": "PyTorch",
        "keras": "Keras",
        "scikit-learn": "scikit-learn",
        "sklearn": "scikit-learn",
        "kubernetes": "Kubernetes",
        "k8s": "Kubernetes",
        "docker": "Docker",
        "aws": "AWS",
        "azure": "Azure",
        "gcp": "Google Cloud",
        "google cloud": "Google Cloud",
    }
    
    # Common skill patterns
    SKILL_PATTERNS = [
        r'\b(?:Java|Python|JavaScript|TypeScript|C\+\+|C#|Go|Rust|PHP|Ruby|Swift|Kotlin|Scala)\b',
        r'\b(?:React|Angular|Vue\.?js?|Node\.?js?|Express\.?js?)\b',
        r'\b(?:Spring Boot|Django|Flask|FastAPI|Rails)\b',
        r'\b(?:TensorFlow|PyTorch|Keras|scikit-learn|Pandas|NumPy)\b',
        r'\b(?:Kubernetes|Docker|AWS|Azure|Google Cloud|GCP)\b',
        r'\b(?:PostgreSQL|MySQL|MongoDB|Redis|Elasticsearch)\b',
        r'\b(?:Git|GitHub|GitLab|CI/CD|Jenkins|GitLab CI)\b',
    ]
    
    def __init__(self):
        """Initialize the skill extractor."""
        self.nlp = None
        if spacy:
            try:
                self.nlp = spacy.load("en_core_web_sm")
            except OSError:
                logger.warning("spaCy model 'en_core_web_sm' not found. Install with: python -m spacy download en_core_web_sm")
    
    def extract_from_data(self, data: List[Dict]) -> List[str]:
        """Extract skills from raw data."""
        all_skills = []
        
        for record in data:
            # Extract from description/title fields
            text_fields = []
            if "description" in record:
                text_fields.append(record["description"])
            if "title" in record:
                text_fields.append(record["title"])
            if "topic" in record:
                text_fields.append(record["topic"])
            
            for text in text_fields:
                if text:
                    skills = self.extract_from_text(str(text))
                    all_skills.extend(skills)
            
            # Extract from explicit skills field
            if "skills" in record and isinstance(record["skills"], list):
                all_skills.extend(record["skills"])
            if "languages" in record and isinstance(record["languages"], dict):
                all_skills.extend(record["languages"].keys())
            if "technologies" in record and isinstance(record["technologies"], list):
                all_skills.extend(record["technologies"])
        
        return all_skills
    
    def extract_from_text(self, text: str) -> List[str]:
        """Extract skills from a text string."""
        if not text:
            return []
        
        skills = set()
        
        # Method 1: Pattern matching
        for pattern in self.SKILL_PATTERNS:
            matches = re.findall(pattern, text, re.IGNORECASE)
            skills.update(m.lower() for m in matches)
        
        # Method 2: spaCy NER (if available)
        if self.nlp:
            doc = self.nlp(text)
            # Extract entities that might be technologies
            for ent in doc.ents:
                if ent.label_ in ["ORG", "PRODUCT"]:
                    # Check if it's a known technology
                    ent_lower = ent.text.lower()
                    if any(skill in ent_lower for skill in self.SKILL_MAPPING.keys()):
                        skills.add(ent_lower)
        
        # Method 3: Direct keyword matching
        text_lower = text.lower()
        for skill_key, skill_normalized in self.SKILL_MAPPING.items():
            if skill_key in text_lower:
                skills.add(skill_key)
        
        return list(skills)
    
    def normalize_skills(self, skills: List[str]) -> Dict[str, int]:
        """Normalize skill names and count occurrences."""
        normalized = {}
        
        for skill in skills:
            skill_lower = skill.lower().strip()
            
            # Map to normalized name
            normalized_name = self.SKILL_MAPPING.get(skill_lower, skill.title())
            
            # Handle special cases
            if normalized_name not in normalized:
                normalized[normalized_name] = 0
            normalized[normalized_name] += 1
        
        return normalized


class RoleExtractor:
    """Extract and normalize job roles from text data."""
    
    # Role normalization mapping
    ROLE_MAPPING = {
        "developer": "Software Developer",
        "dev": "Software Developer",
        "programmer": "Software Developer",
        "engineer": "Software Engineer",
        "swe": "Software Engineer",
        "data scientist": "Data Scientist",
        "data engineer": "Data Engineer",
        "ml engineer": "ML Engineer",
        "machine learning engineer": "ML Engineer",
        "backend developer": "Backend Developer",
        "backend engineer": "Backend Developer",
        "frontend developer": "Frontend Developer",
        "frontend engineer": "Frontend Developer",
        "full stack": "Full Stack Developer",
        "fullstack": "Full Stack Developer",
        "devops": "DevOps Engineer",
        "devops engineer": "DevOps Engineer",
        "sre": "Site Reliability Engineer",
        "site reliability engineer": "Site Reliability Engineer",
    }
    
    ROLE_PATTERNS = [
        r'\b(?:Senior|Junior|Lead|Principal)\s+(?:Software\s+)?(?:Developer|Engineer|Programmer)\b',
        r'\b(?:Data\s+)?(?:Scientist|Engineer|Analyst)\b',
        r'\b(?:ML|Machine Learning|AI)\s+Engineer\b',
        r'\b(?:Backend|Frontend|Full Stack|Full-Stack)\s+(?:Developer|Engineer)\b',
        r'\bDevOps\s+Engineer\b',
        r'\bSRE\b',
    ]
    
    def __init__(self):
        """Initialize the role extractor."""
        self.nlp = None
        if spacy:
            try:
                self.nlp = spacy.load("en_core_web_sm")
            except OSError:
                logger.warning("spaCy model not found")
    
    def extract_from_data(self, data: List[Dict]) -> List[str]:
        """Extract roles from raw data."""
        all_roles = []
        
        for record in data:
            # Extract from title
            if "title" in record:
                roles = self.extract_from_text(str(record["title"]))
                all_roles.extend(roles)
        
        return all_roles
    
    def extract_from_text(self, text: str) -> List[str]:
        """Extract roles from a text string."""
        if not text:
            return []
        
        roles = set()
        
        # Pattern matching
        for pattern in self.ROLE_PATTERNS:
            matches = re.findall(pattern, text, re.IGNORECASE)
            roles.update(m.lower() for m in matches)
        
        # Direct keyword matching
        text_lower = text.lower()
        for role_key, role_normalized in self.ROLE_MAPPING.items():
            if role_key in text_lower:
                roles.add(role_normalized)
        
        return list(roles)
    
    def normalize_roles(self, roles: List[str]) -> Dict[str, int]:
        """Normalize role names and count occurrences."""
        normalized = {}
        
        for role in roles:
            role_lower = role.lower().strip()
            normalized_name = self.ROLE_MAPPING.get(role_lower, role.title())
            
            if normalized_name not in normalized:
                normalized[normalized_name] = 0
            normalized[normalized_name] += 1
        
        return normalized

