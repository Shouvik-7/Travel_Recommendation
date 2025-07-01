import boto3
import streamlit as st
from langchain.embeddings import BedrockEmbeddings
from langchain.llms.bedrock import Bedrock
from langchain.llms import openai
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
import pymongo
from pymongo import MongoClient
from langchain.vectorstores import MongoDBAtlasVectorSearch
from langchain.document_loaders import DirectoryLoader
from langchain.llms import Bedrock
from langchain.chains import RetrievalQA
import awswrangler as wr
import boto3
from langchain.chains import LLMChain
import openai
import pymongo
from langchain.chat_models import ChatOpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")

load_dotenv()

# Access AWS credentials
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")


# Initialize Mongo client
client = MongoClient("mongodb+srv://s04538219:f2nwXFe06VbmEwgi@cluster0.fl5hb94.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
dbname = "members_db"
collectionName = "collection_of_text_blobs"
collection = client[dbname][collectionName]

# bedrock embeddings
bedrock = boto3.client(service_name='bedrock-runtime', region_name='us-east-1')
bedrock_embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v1",client=bedrock)

# Create a MongoDB Atlas vector store
vector_store = MongoDBAtlasVectorSearch(
    collection=collection,
    embedding=bedrock_embeddings,  # use the BedrockEmbeddings instance
    index_name="memberindex",   # the name of your Atlas vector index
    text_key="text",             # field in your MongoDB doc that contains the text
    embedding_key="embedding"    # field in your MongoDB doc that contains the embedding
)


# Create a retriever from the vector store
retriever = vector_store.as_retriever(search_kwargs={"k": 1})

# Streamlit app setup
st.title("Personalized Travel Recommendation")
    
# Input query from user    
query = st.text_input("Enter Member Query:")

# If the button is clicked, process the query
if st.button("Get response"):
    with st.spinner("Processing..."):
        
        # Run the query
        docs = retriever.get_relevant_documents(query)

        # Output results
        toptext = docs[0].page_content

        # LLM
        # def get_llm():
        #     model_id = "meta.llama3-8b-instruct-v1:0"
        #     #model_id = "ai21.jamba-1-5-mini-v1:0"
        #     llm = Bedrock(
        #         model_id=model_id,
        #         client=bedrock,
        #         model_kwargs={
        #             "temperature": 0.6}
        #     )
        #     return llm
        # llm = get_llm()
        llm = ChatOpenAI(model_name="gpt-4", temperature=0.7)
        

        # Prompt to classify the content
        prompt = PromptTemplate.from_template(""" Your name is trip advisor. You are the best Travel Advisor in the world. 
        Given the following details of a member, give similar travel recommendation the member.                                      
        Text:
        "{text}"
                                              
                                              "{q}"
                                            
        output:
                """)

        # Build the chain
        type_chain = LLMChain(llm=llm, prompt=prompt)


        # Example retrieved document (could come from MongoDB or retriever

        # Run the chain
        response = type_chain.run({"text": toptext,"q":query})
        
        # Display the response
        st.write(f"Response: {response}")



            



