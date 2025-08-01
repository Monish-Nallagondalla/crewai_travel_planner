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
    website: str = Field(..., description="THe website URL to scrape")

class BrowserTools(BaseModel)