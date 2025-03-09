from setuptools import setup, find_packages

setup(
    name="analyst_assistant_llm",
    version="1.0.0",
    author="William ZOUNON",
    author_email="williamzounon@gmail.com",
    description="Assistant that uses LLMs to provide information from the database. Uses LangChain, Ollama, Python, Postgres, FastAPI.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/Wizo17/analyst_assistant_llm",
    packages=find_packages(where="src"),
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        "python-dotenv",
        "setuptools",
        "fastapi",
        "uvicorn",
        "psycopg2",
        "langchain",
        "langchain-community",
        "langchain-ollama",
        "langchain-openai",
        "langchain-anthropic",
        "langgraph",
        "ollama",
        "pydantic",
        "sqlalchemy",
        "pandas",
        "sqlparse"
    ],
    entry_points={
        'console_scripts': [
            'start-api=app:main',
        ],
    },
)