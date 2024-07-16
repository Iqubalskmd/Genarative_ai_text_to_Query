from dotenv import load_dotenv
import streamlit as st
import os
import sqlite3
import google.generativeai as genai

# Load all the environment variables
load_dotenv()

# Configure GenAI Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Google Gemini Model and provide queries as response
def get_gemini_response(question,prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt[0],question])
    return response.text

# Function to retrieve query from the database
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows

# Define your prompt
prompt = [
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name STUDENT and has the following columns - NAME, CLASS, SECTION.

    For example:
    - Example 1: "How many entries of records are present?", the SQL command will be something like this: SELECT COUNT(*) FROM STUDENT;
    - Example 2: "Tell me all the students studying in Data Science class?", the SQL command will be something like this: SELECT * FROM STUDENT WHERE CLASS="Data Science";
    """
]

# Streamlit App
st.set_page_config(page_title="I can Retrieve Any SQL query")
st.header("Gemini App To Retrieve SQL Data")

question = st.text_input("Input: ", key="input")

submit = st.button("Ask the question")

# If submit is clicked
if submit:
    sql_query = get_gemini_response(question, prompt)
    st.write(f"Generated SQL Query: {sql_query}")
    try:
        response = read_sql_query(sql_query, "student.db")
        st.subheader("The Response is")
        for row in response:
            st.write(row)
    except Exception as e:
        st.error(f"An error occurred: {e}")
