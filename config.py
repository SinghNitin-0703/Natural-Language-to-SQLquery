import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
env_file = os.path.join(script_dir, "google_apiKEY.env")

print(f"📂 Script directory: {script_dir}")
print(f"🔍 Looking for env file at: {env_file}")

if os.path.exists(env_file):
    load_dotenv(dotenv_path=env_file)
    print(f"✅ Found and loaded {env_file}")
else:
    print(f"⚠️ Warning: {env_file} not found, trying default .env")
    load_dotenv() # Load .env as a fallback

# --- Google API Key ---
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    print("\n❌ ERROR: API key not found!")
    print(f"Please check your google_apiKEY.env file contains:")
    print("GOOGLE_API_KEY=your_actual_key_here")
    print("\nMake sure the file is in the same directory as the script!")
    raise ValueError("API key not found in environment variables")
else:
    print("✅ Google API key loaded successfully")


# --- Database Credentials ---
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME")

# Validate database credentials
if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_NAME]):
    print("\n⚠️ WARNING: Some database credentials are missing!")
    print(f"DB_USER: {'✅' if DB_USER else '❌'}")
    print(f"DB_PASSWORD: {'✅' if DB_PASSWORD else '❌'}")
    print(f"DB_HOST: {'✅' if DB_HOST else '❌'}")
    print(f"DB_NAME: {'✅' if DB_NAME else '❌'}")
    raise ValueError("Missing database credentials in environment variables")
else:
    print("✅ Database credentials loaded successfully")

# Create encoded MySQL URI
password_encoded = quote_plus(DB_PASSWORD)
mysql_uri = f"mysql+pymysql://{DB_USER}:{password_encoded}@{DB_HOST}:{DB_PORT}/{DB_NAME}"