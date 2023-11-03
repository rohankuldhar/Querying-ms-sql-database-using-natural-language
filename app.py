from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAI
from langchain.agents import AgentExecutor
from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI
from sqlalchemy import create_engine
import os
from urllib.parse import quote_plus
import pyodbc as odbc 
import openai
import streamlit as st

st.header("MS SQL Database querying using natural langauage")

os.environ['OPENAI_API_KEY'] = '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'



conn =  "DRIVER={ODBC Driver 17 for SQL Server};Server=DESKTOP-OI287L1;Database=AdventureWorks2019;trusted_connection=yes;"
quoted = quote_plus(conn)
target_connection = 'mssql+pyodbc:///?odbc_connect={}'.format(quoted)
engine = create_engine(target_connection)


db = SQLDatabase(engine)

llm=OpenAI(temperature=0)
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

#ZERO_SHOT_REACT_DESCRIPTION Agent type

agent_executor = create_sql_agent(
    llm=OpenAI(temperature=0),
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
)

prompt=st.text_input('Enter the text')

if st.button('Submit'):
    final=agent_executor.run(prompt)
    st.text(final)
