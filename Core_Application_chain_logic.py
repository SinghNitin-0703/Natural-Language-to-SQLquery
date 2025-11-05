import pandas as pd
import ast
import traceback

from langchain.chains import create_sql_query_chain
from langchain_core.prompts import FewShotPromptTemplate
from langchain.chains.sql_database.prompt import PROMPT_SUFFIX

# Import components from other modules
from llm_setup import llm, example_selector
from database import db
from prompts import mysql_prompt, example_prompt

print("🔗 Building LangChain components...")

# Few-shot prompt
few_shot_prompt = FewShotPromptTemplate(
    example_selector=example_selector,
    example_prompt=example_prompt,
    prefix=mysql_prompt,
    suffix=PROMPT_SUFFIX,
    input_variables=["input", "table_info", "top_k"]
)

# Create chain with few-shot prompt
query_chain = create_sql_query_chain(llm, db, prompt=few_shot_prompt)

print("✅ LangChain query chain created.")

def clean_sql_query(sql_query):
    """Clean the SQL query by removing prefixes and markdown"""
    cleaned_sql = sql_query.replace("SQLQuery:", "").strip()
    
    if cleaned_sql.startswith("```sql"):
        cleaned_sql = cleaned_sql[6:]
    elif cleaned_sql.startswith("```"):
        cleaned_sql = cleaned_sql[3:]
    
    if cleaned_sql.endswith("```"):
        cleaned_sql = cleaned_sql[:-3]
    
    return cleaned_sql.strip()

def format_result_as_table(result):
    """Format SQL result as a pandas DataFrame for better display"""
    if not result or result == "":
        return pd.DataFrame({"Result": ["No results found"]})
    
    try:
        # Convert result to DataFrame
        if isinstance(result, str):
            # Parse string representation of list of tuples
            try:
                parsed_result = ast.literal_eval(result)
                if isinstance(parsed_result, list) and parsed_result:
                    df = pd.DataFrame(parsed_result)
                    return df
                else:
                    return pd.DataFrame({"Result": [result]})
            except:
                return pd.DataFrame({"Result": [result]})
        elif isinstance(result, list):
            if result and (isinstance(result[0], tuple) or isinstance(result[0], dict)):
                df = pd.DataFrame(result)
                return df
            else:
                return pd.DataFrame({"Result": result})
        else:
            return pd.DataFrame({"Result": [str(result)]})
    except Exception as e:
        print(f"Error formatting result: {e}")
        return pd.DataFrame({"Result": [str(result)]})

def query_database(question):
    """Main function to process natural language question"""
    if not question or question.strip() == "":
        return "Please enter a question", "No query to execute", "Please enter a question first"
    
    try:
        print(f"\n🔍 Processing question: {question}")
        
        # Step 1: Generate SQL query
        print("📝 Generating SQL query...")
        sql_query = query_chain.invoke({"question": question})
        print(f"Raw query: {sql_query[:200]}...")
        
        # Step 2: Clean the query
        print("🧹 Cleaning SQL query...")
        cleaned_sql = clean_sql_query(sql_query)
        print(f"Cleaned query: {cleaned_sql}")
        
        # Step 3: Execute query
        print("🗄️ Executing query against database...")
        result = db.run(cleaned_sql)
        print(f"Query result (first 200 chars): {str(result)[:200]}...")
        
        # Step 4: Format result as table
        print("📊 Formatting results...")
        formatted_result = format_result_as_table(result)
        
        # Step 5: Get natural language explanation
        print("💡 Generating explanation...")
        final_prompt = f"""
        Based on this SQL query: {cleaned_sql}
        And this result: {result}
        
        Please provide a clean, natural language answer to the original question: {question}
        
        Be concise and focus on the key insights from the data.
        """
        
        final_answer = llm.invoke(final_prompt)
        explanation = final_answer.content
        
        print("✅ Success!")
        return cleaned_sql, formatted_result, explanation
        
    except Exception as e:
        error_trace = traceback.format_exc()
        print(f"\n❌ ERROR occurred:")
        print(error_trace)
        
        error_msg = f"❌ Error: {str(e)}\n\nPlease check the console for detailed error information."
        # Return the error message to all output fields in Gradio
        error_df = pd.DataFrame({"Error": [str(e), error_trace]})
        return f"Error generating SQL: {str(e)}", error_df, f"An error occurred: {str(e)}\n\n{error_trace}"