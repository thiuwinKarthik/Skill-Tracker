"""
Skill descriptions and metadata for technology skills.
"""
from typing import Dict, Optional

SKILL_DESCRIPTIONS: Dict[str, Dict[str, str]] = {
    "React": {
        "description": "React is a popular JavaScript library for building user interfaces, particularly web applications. Developed by Facebook, it uses a component-based architecture and virtual DOM for efficient rendering. React is widely used in modern web development and has a large ecosystem of tools and libraries.",
        "category": "Frontend Framework",
        "popularity": "Very High",
        "trend": "Growing"
    },
    "Angular": {
        "description": "Angular is a TypeScript-based web application framework developed by Google. It provides a complete solution for building large-scale applications with features like dependency injection, routing, and form handling built-in. While still popular, it faces competition from React and Vue.js.",
        "category": "Frontend Framework",
        "popularity": "High",
        "trend": "Stable"
    },
    "Vue.js": {
        "description": "Vue.js is a progressive JavaScript framework for building user interfaces. It's known for its gentle learning curve, excellent documentation, and flexibility. Vue.js is gaining popularity, especially in the Asian market and among developers who want a simpler alternative to React or Angular.",
        "category": "Frontend Framework",
        "popularity": "High",
        "trend": "Growing"
    },
    "Python": {
        "description": "Python is a high-level, interpreted programming language known for its simplicity and readability. It's widely used in web development, data science, machine learning, automation, and scientific computing. Python has one of the largest ecosystems and is consistently ranked as one of the most popular programming languages.",
        "category": "Programming Language",
        "popularity": "Very High",
        "trend": "Growing"
    },
    "JavaScript": {
        "description": "JavaScript is the core programming language of the web, enabling interactive web pages and web applications. It's used for both frontend and backend development (Node.js). JavaScript is essential for modern web development and continues to evolve with new features and frameworks.",
        "category": "Programming Language",
        "popularity": "Very High",
        "trend": "Stable"
    },
    "TypeScript": {
        "description": "TypeScript is a typed superset of JavaScript that compiles to plain JavaScript. It adds static type checking, which helps catch errors early and improves code maintainability. TypeScript is increasingly adopted in large-scale projects and is the language of choice for Angular and many React projects.",
        "category": "Programming Language",
        "popularity": "High",
        "trend": "Growing"
    },
    "Node.js": {
        "description": "Node.js is a JavaScript runtime built on Chrome's V8 engine that allows JavaScript to run on the server side. It's known for its event-driven, non-blocking I/O model, making it efficient for building scalable network applications. Node.js has a vast ecosystem of packages (npm) and is widely used for backend development.",
        "category": "Runtime Environment",
        "popularity": "Very High",
        "trend": "Stable"
    },
    "Java": {
        "description": "Java is a class-based, object-oriented programming language designed to have as few implementation dependencies as possible. It's widely used in enterprise applications, Android development, and large-scale systems. Java has a mature ecosystem and strong community support.",
        "category": "Programming Language",
        "popularity": "High",
        "trend": "Stable"
    },
    "Go": {
        "description": "Go (Golang) is a statically typed, compiled programming language designed at Google. It's known for its simplicity, concurrency features, and excellent performance. Go is popular for building microservices, cloud-native applications, and system tools. It's gaining significant traction in backend development.",
        "category": "Programming Language",
        "popularity": "Medium",
        "trend": "Growing"
    },
    "Rust": {
        "description": "Rust is a systems programming language focused on safety, speed, and concurrency. It provides memory safety without garbage collection, making it ideal for performance-critical applications. Rust is gaining popularity for systems programming, web assembly, and blockchain development.",
        "category": "Programming Language",
        "popularity": "Medium",
        "trend": "Growing"
    },
    "TensorFlow": {
        "description": "TensorFlow is an open-source machine learning framework developed by Google. It's used for building and training machine learning models, particularly deep learning neural networks. TensorFlow is widely used in research and production for AI/ML applications.",
        "category": "ML Framework",
        "popularity": "High",
        "trend": "Stable"
    },
    "PyTorch": {
        "description": "PyTorch is an open-source machine learning library developed by Facebook's AI Research lab. It's known for its dynamic computation graph and Pythonic interface, making it popular for research and prototyping. PyTorch is increasingly used in production environments.",
        "category": "ML Framework",
        "popularity": "High",
        "trend": "Growing"
    },
    "Kubernetes": {
        "description": "Kubernetes is an open-source container orchestration platform for automating deployment, scaling, and management of containerized applications. It's the de facto standard for container orchestration and is essential for cloud-native development and DevOps practices.",
        "category": "DevOps Tool",
        "popularity": "High",
        "trend": "Growing"
    },
    "Docker": {
        "description": "Docker is a platform for developing, shipping, and running applications using containerization. It allows applications to run consistently across different environments. Docker is fundamental to modern DevOps practices and microservices architecture.",
        "category": "DevOps Tool",
        "popularity": "Very High",
        "trend": "Stable"
    },
    "AWS": {
        "description": "Amazon Web Services (AWS) is a comprehensive cloud computing platform offering over 200 services including computing, storage, databases, and machine learning. AWS is the market leader in cloud services and is essential for cloud-native development and infrastructure management.",
        "category": "Cloud Platform",
        "popularity": "Very High",
        "trend": "Growing"
    },
    "FastAPI": {
        "description": "FastAPI is a modern, fast web framework for building APIs with Python based on standard Python type hints. It's known for its high performance, automatic API documentation, and ease of use. FastAPI is gaining popularity as an alternative to Flask and Django for API development.",
        "category": "Web Framework",
        "popularity": "Medium",
        "trend": "Growing"
    },
    "PostgreSQL": {
        "description": "PostgreSQL is a powerful, open-source relational database management system known for its reliability, feature robustness, and performance. It supports advanced data types and has excellent concurrency control. PostgreSQL is widely used in production environments.",
        "category": "Database",
        "popularity": "High",
        "trend": "Stable"
    },
    "MongoDB": {
        "description": "MongoDB is a NoSQL document database that stores data in flexible, JSON-like documents. It's known for its scalability and flexibility, making it popular for applications with evolving data schemas. MongoDB is widely used in modern web applications.",
        "category": "Database",
        "popularity": "High",
        "trend": "Stable"
    },
    "Redis": {
        "description": "Redis is an in-memory data structure store used as a database, cache, and message broker. It's known for its high performance and support for various data structures. Redis is essential for building high-performance applications requiring fast data access.",
        "category": "Database/Cache",
        "popularity": "High",
        "trend": "Stable"
    }
}


def get_skill_description(skill_name: str) -> Optional[Dict[str, str]]:
    """Get description and metadata for a skill."""
    # Try exact match first
    if skill_name in SKILL_DESCRIPTIONS:
        return SKILL_DESCRIPTIONS[skill_name]
    
    # Try case-insensitive match
    skill_lower = skill_name.lower()
    for key, value in SKILL_DESCRIPTIONS.items():
        if key.lower() == skill_lower:
            return value
    
    # Try partial match
    for key, value in SKILL_DESCRIPTIONS.items():
        if skill_lower in key.lower() or key.lower() in skill_lower:
            return value
    
    return None


def get_default_description(skill_name: str) -> Dict[str, str]:
    """Get default description for skills without specific descriptions."""
    return {
        "description": f"{skill_name} is a technology skill in high demand in the current job market. The skill shows varying levels of adoption across different industries and use cases.",
        "category": "Technology",
        "popularity": "Medium",
        "trend": "Stable"
    }

