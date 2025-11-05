import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_community.embeddings import HuggingFaceEmbeddings
from config import GOOGLE_API_KEY
from prompts import few_shots

print("🤖 Initializing AI components...")

# Configure genai
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",  # Using 1.5-flash for speed and cost
    google_api_key=GOOGLE_API_KEY,
    temperature=0
)

# Create embeddings and vector store
print("🧠 Loading embedding model...")
to_vectorize = [" ".join(str(v) for v in example.values()) for example in few_shots]
embeddings = HuggingFaceEmbeddings(
    model_name='sentence-transformers/all-MiniLM-L6-v2',
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': True}
)

print("📚 Creating vector store...")
vectorstore = Chroma.from_texts(
    texts=to_vectorize,
    embedding=embeddings,
    metadatas=few_shots
)

example_selector = SemanticSimilarityExampleSelector(
    vectorstore=vectorstore,
    k=2
)

print("✅ AI components initialized successfully.")