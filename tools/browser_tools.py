import json
import requests
import streamlit as st
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from unstructured.partition.html import partition_html
from crewai import Agent, Task
#from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from crewai import LLM

class WebsiteInput(BaseModel):
    website: str = Field(..., description="The website URL to scrape")

class BrowserTools(BaseTool):
    name: str = "Scrape website content"
    description: str = "Useful to scrape and summarize a website content"
    args_schema: type[BaseModel] = WebsiteInput

    def _run(self,website:str)-> str:
        try:
            url = f"https://chrome.browserless.io/content?token={st.secrets['BROWSERLESS_API_KEY']}"
            payload = json.dumps({"url": website})
            headers = {'cache-control': 'no-cache', 'content-type': 'application/json'}
            response = requests.request("POST", url, headers=headers, data=payload)