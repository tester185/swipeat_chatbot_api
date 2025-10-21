from dotenv import load_dotenv
import os
import json
import requests
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from openai import OpenAI
load_dotenv()
hf_token=os.getenv('HUGGINGFACEHUB_API_TOKEN')
base_url=os.getenv('BASE_URL')

api_key = os.getenv("OPENAI_API_KEY")
base_url=os.getenv('BASE_URL')
client=OpenAI(api_key=api_key,base_url=base_url)


def embed(req):
    embedder_model=HuggingFaceEndpointEmbeddings(model="sentence-transformers/all-MiniLM-L6-v2",huggingfacehub_api_token=hf_token)
    return embedder_model.embed_query(req)
