# API Assistant for data analysis

This is the backend API for the data analysis assistant project. It provides endpoints for processing and analyzing data through chat-like interactions.
Assistant is a solution enabling analysts to ask questions in natural language and obtain answers, accompanied by detailed explanations.


## Build with

The project uses:
* [Python](https://www.python.org/)
* [LangChain](https://www.langchain.com/)
* [Ollama](https://ollama.com/)
* [Postgres](https://www.postgresql.org/)


## Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- ollama (for local llm model)
- Postgres
    - If you want to test, you can use the GTFS data from [Ile-De-France Mobilité](https://www.data.gouv.fr/fr/datasets/horaires-prevus-sur-les-lignes-de-transport-en-commun-dile-de-france-gtfs-datahub/).
    - The database schema and an import script can be found [here](data/base_gtfs_test/base_analyst_llm_export.sql)
- **An LLM isn't smarter than you are, so you have to tell him what you want. There has to be a description of your columns in your database tables.**

### Installation

1. Clone this repository:
```bash
git clone https://github.com/Wizo17/analyst_assistant_llm
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
```bash
# Windows
venv\Scripts\activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```
<em>If you have a problem, use python 3.12.0 and requirements_all.txt</em>

5. Create .env file:
```bash
cp .env_example .env
```

6. **Update .env file**:

## Running the API

You can start the API server using one of these methods:

### Method 1: Using uvicorn directly
```bash
uvicorn app:app --host 0.0.0.0 --port 7575 --reload
```

### Method 2: Using the run script
```bash
python run.py
```

The API will be available at `http://localhost:7575`


## API Endpoints

### Base URL
- `GET /` - Check API status

### Chat Endpoints
- `GET /chat/infos` - Retrieve system information
- `POST /chat/init` - Initialize a new chat session
- `POST /chat/query` - Send a query for analysis
- `POST /chat/download` - Download analysis results


## Development

To add new features or modify existing ones:
1. Create feature branch
2. Implement changes
3. Add tests
4. Submit pull request


## Logging

Logs are handled by the custom logger in `src/utils/logger.py`. Check the console output or logs/ folder for logs or during development.


## Versions
**LTS:** [1.0.0](https://github.com/Wizo17/analyst_assistant_llm)

## Authors

* [@wizo17](https://github.com/Wizo17)

## License

This project is licensed under the ``MIT`` License - see [LICENSE](LICENSE) for more information.
