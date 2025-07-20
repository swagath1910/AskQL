import streamlit as st
import os
import pandas as pd
from dotenv import load_dotenv
from core.db_connector import DBConnector
from core.query_generator import QueryGenerator

# Load environment variables from .env file
load_dotenv()

# --- App Configuration ---
st.set_page_config(
    page_title="Conversational SQL",
    page_icon="🤖",
    layout="wide"
)

# --- Database and Query Generator Initialization ---
DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'sample_database.db')

@st.cache_resource
def get_db_connector():
    """Creates and returns a DBConnector instance."""
    if not os.path.exists(DB_PATH):
        st.error(f"Database file not found. Please run 'python3 scripts/setup_database.py' first.")
        st.stop()
    connector = DBConnector(DB_PATH)
    connector.connect()
    return connector

@st.cache_resource
def get_query_generator(_connector):
    """Creates and returns a QueryGenerator instance."""
    if not os.getenv("GOOGLE_API_KEY"):
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    schema = _connector.get_schema()
    if not schema:
        st.error("Failed to retrieve database schema.")
        st.stop()
    return QueryGenerator(db_schema=schema)

# --- Main App Logic ---
db_connector = get_db_connector()
query_generator = get_query_generator(db_connector)

st.title("🤖 Conversational SQL Query Generator")
st.write("Ask questions about the database. I can remember our conversation for follow-up questions.")

with st.expander("View Database Schema"):
    st.text(query_generator.db_schema)

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How can I help you query the database?"}]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "results" in message:
            st.dataframe(message["results"])

# Format chat history for the LLM
def format_chat_history(messages):
    history = ""
    for msg in messages[:-1]: # Exclude the last user message
        if msg["role"] == "user":
            history += f"User: {msg['content']}\n"
        elif msg["role"] == "assistant" and "sql_query" in msg:
            history += f"Assistant (SQL): {msg['sql_query']}\n"
    return history

# Handle user input
if prompt := st.chat_input("Your question..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate and execute SQL
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                chat_history = format_chat_history(st.session_state.messages)
                generated_sql = query_generator.generate_sql(prompt, chat_history)
                clean_sql = generated_sql.strip().replace("```sql", "").replace("```", "").strip()

                st.markdown("Here is the generated SQL query:")
                st.code(clean_sql, language="sql")
                
                results, columns = db_connector.execute_query(clean_sql)
                
                st.markdown("And here are the results:")
                if results is not None and columns:
                    df = pd.DataFrame(results, columns=columns)
                    st.dataframe(df)
                    # Store everything in the message for redisplay
                    assistant_message = {
                        "role": "assistant", 
                        "content": f"Generated SQL:\n```sql\n{clean_sql}\n```",
                        "sql_query": clean_sql,
                        "results": df
                    }
                else:
                    st.success("Query executed successfully, but it returned no data.")
                    assistant_message = {
                        "role": "assistant", 
                        "content": f"The query `{clean_sql}` executed successfully but returned no data.",
                        "sql_query": clean_sql
                    }
                st.session_state.messages.append(assistant_message)

            except Exception as e:
                error_message = f"An error occurred: {e}"
                st.error(error_message)
                st.session_state.messages.append({"role": "assistant", "content": error_message})