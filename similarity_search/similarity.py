from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEndpointEmbeddings
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
load_dotenv()

hf_token = os.getenv('HUGGINGFACEHUB_API_TOKEN')

# Initialize embeddings
embedding_fun = HuggingFaceEndpointEmbeddings(
    model="sentence-transformers/all-MiniLM-L6-v2",  
    huggingfacehub_api_token=hf_token
)

# Lazy load the collection (only once, on first request)
_preloaded_responses_collection = None

def get_collection():
    global _preloaded_responses_collection
    if _preloaded_responses_collection is None:
        print("Loading ChromaDB collection...")
        _preloaded_responses_collection = Chroma(
            persist_directory="./chroma_db",
            embedding_function=embedding_fun
        )
        print("ChromaDB collection loaded successfully")
    return _preloaded_responses_collection

def get_similar(request):
    print('Searching for similar documents...')
    print(f'Query: {request}')
    
    collection = get_collection()
    res = collection.similarity_search_with_relevance_scores(request, k=1)
    
    print(f'Search complete. Found {len(res)} result(s)')
    return res