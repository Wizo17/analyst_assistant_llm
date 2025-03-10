# Chatbot Assistant for data analysis Front Example

The Intelligent SQL Assistant is a solution enabling analysts to ask questions in natural language and obtain answers, accompanied by detailed explanations.

## Features

- Modern and intuitive user interface
- SQL query generation from natural language questions
- Detailed explanation of generated SQL queries
- Download results in JSON or CSV format
- Management of multiple chat sessions
- Ability to rename chat sessions

## Prerequisites

- Node.js (v14 or higher)
- npm (v6 or higher)
- Backend API with Python and FastAPI running on http://localhost:7575

## Installation

1. Clone this repository:
```bash
git clone https://github.com/Wizo17/analyst_assistant_llm
cd front/chatbot-app
```

2. Install dependencies:
```bash
npm install
```

3. Start the application in development mode:
```bash
npm start
```

The application will be accessible at [http://localhost:3000](http://localhost:3000).

## Usage

1. Make sure the backend API is running on http://localhost:7575 (bakend)
2. Launch the frontend application
3. Create a new chat session by clicking on "New Chat"
4. Ask your questions about the data
5. Use the toggles to customize the responses:
   - **Detailed Answer**: Get detailed explanations
   - **File Format**: Choose between JSON and CSV for downloads
   - **Sample Data**: Use a sample of data or the complete dataset
6. Rename chat sessions by hovering over a session and clicking the edit icon

## Project Structure

```
src/
├── components/       # React components
├── context/          # React context for state management
├── services/         # Services for API calls
├── styles/           # Global styles and themes
├── types/            # TypeScript type definitions
└── utils/            # Utility functions
```

## Backend API

The application communicates with a backend API that must expose the following endpoints:

- `GET /` - Connection verification
- `GET /chat/infos` - Retrieve system information
- `POST /chat/init/` - Initialize a chat session
- `POST /chat/query` - Send a query
- `POST /chat/download` - Download a results file

## Features in Detail

### Chat Sessions
- Create multiple chat sessions
- Switch between sessions
- Rename sessions for better organization

### Query Options
- Toggle detailed explanations for SQL queries
- Choose output format (JSON/CSV)
- Select between sample data or full dataset

### Results Handling
- View formatted responses
- Copy text to clipboard
- Download result files

## Versions
**LTS:** [1.0.0](https://github.com/Wizo17/analyst_assistant_llm)

## Authors

* [@wizo17](https://github.com/Wizo17)

## License

This project is licensed under the ``MIT`` License - see [LICENSE](LICENSE) for more information.
