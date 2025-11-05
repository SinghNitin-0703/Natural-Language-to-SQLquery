from langchain_community.utilities import SQLDatabase
from config import mysql_uri

print("🗄️ Initializing database connection...")
db = SQLDatabase.from_uri(mysql_uri)
print("✅ Database connection established.")