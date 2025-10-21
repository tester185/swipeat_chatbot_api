
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from scipy.spatial import distance
import os
import sys
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


load_dotenv()

hf_token=os.getenv('HUGGINGFACEHUB_API_TOKEN')
embedding_fun = HuggingFaceEndpointEmbeddings(
    model="sentence-transformers/all-MiniLM-L6-v2",  
    huggingfacehub_api_token=hf_token
)
preloaded_responses_collection=Chroma(persist_directory="./chroma_db",embedding_function=embedding_fun)

def get_similar(request):
    print('IM HEEEEEERE')
    print(request)
    res=preloaded_responses_collection.similarity_search_with_relevance_scores(request,k=1)
    print('im done ')
    return res