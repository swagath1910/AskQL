# Conversational SQL Query Generator

This project is a web application that allows users to convert natural language queries into SQL using Large Language Models (LLMs) and LangChain. The application is built with Streamlit, providing an intuitive user interface for interacting with relational databases without the need to write SQL queries manually.

## Project Structure

```
conversational-sql-generator
├── app.py                  # Main entry point of the Streamlit application
├── core
│   ├── db_connector.py     # Manages database connections and queries
│   └── query_generator.py   # Converts natural language to SQL queries
├── data
│   └── sample_database.db   # Sample SQLite database for testing
├── .env.example             # Example environment variables
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```

## Features

- **Natural Language Processing**: Users can input queries in natural language, which are then converted to SQL.
- **Database Interaction**: The application connects to a SQLite database, allowing users to retrieve data seamlessly.
- **User-Friendly Interface**: Built with Streamlit, the application provides an easy-to-use interface for users of all technical levels.

## Setup Instructions

1. **Clone the Repository**:
   ```
   git clone <repository-url>
   cd conversational-sql-generator
   ```

2. **Create a Virtual Environment** (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:
   ```
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**:
   Copy `.env.example` to `.env` and update the variables as needed.

5. **Run the Application**:
   ```
   streamlit run app.py
   ```

## Usage

- Open the application in your web browser.
- Enter a natural language query in the input box.
- Click the "Generate SQL" button to see the corresponding SQL query and the results retrieved from the database.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.