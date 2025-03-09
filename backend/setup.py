from setuptools import setup, find_packages

setup(
    name="analyst_assistant_llm",
    version="0.0.1",
    author="William ZOUNON",
    author_email="williamzounon@gmail.com",
    description="Assistant that uses LLMs to provide information from the database. Uses LangChain, CrewAI, Ollama, Python, Postgres, FastAPI.",
    packages=find_packages(where="src"),
    package_dir={'': 'src'},
    install_requires=[
        "fastapi",
        "uvicorn",
        "psycopg2",
        "langchain",
        "crewai",
        "ollama",
        "pydantic",
        "python-dotenv",
        "setuptools"

    ],
)