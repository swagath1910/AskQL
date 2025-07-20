import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

class QueryGenerator:
    def __init__(self, db_schema):
        if not os.getenv("GOOGLE_API_KEY"):
            raise ValueError("GOOGLE_API_KEY environment variable not set.")
        
        self.db_schema = db_schema
        
        # ✅ Use a valid stable Gemini model
        self.llm = ChatGoogleGenerativeAI(
            model="models/gemini-2.5-flash",
            temperature=0
        )
        
        self.prompt_template = self._create_prompt_template()
        self.chain = self.prompt_template | self.llm | StrOutputParser()

    def _create_prompt_template(self):
        template = """
        You are an expert at converting user questions into SQL queries.
        You have access to the conversation history to understand context from previous questions.
        
        Based on the database schema and conversation history below, write a SQL query that would answer the user's latest question.
        Your response must be only the SQL query. Do not include any other text or explanations.
        
        Schema:
        {schema}

        Conversation History:
        {chat_history}
        
        Latest Question:
        {question}
        
        SQL Query:
        """
        return PromptTemplate.from_template(template)

    def generate_sql(self, question, chat_history):
        return self.chain.invoke({
            "schema": self.db_schema,
            "question": question,
            "chat_history": chat_history
        })
