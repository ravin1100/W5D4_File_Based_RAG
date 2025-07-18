# backend/summarization.py

"""
This module handles summarization for text, tables, and image metadata using LangChain components
and the Gemini 2.5 Flash model. It creates custom prompts for each modality, uses chains for inference,
and wraps each summarization call in a convenient function.

Functions:
    - summarize_text: Summarizes text content.
    - summarize_table: Summarizes tabular data.
    - summarize_image: Summarizes images using their metadata.
"""

import os
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI

from dotenv import load_dotenv
load_dotenv()  # This loads all key-value pairs from '.env'

# Load Gemini API key from environment variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ----- PROMPT DESIGN -----

# General system prompt for all modalities
system_template = (
    "You are an expert assistant specialized in technical summarization. "
    "Create concise, clear, and accurate summaries for text, tables, and images. "
    "When summarizing images, use both metadata and visual description if available."
)
system_prompt = SystemMessagePromptTemplate.from_template(system_template)

# Text content summarization
human_text_prompt = HumanMessagePromptTemplate.from_template(
    "Summarize the following technical text for quick understanding:\n{content}"
)
text_prompt_template = ChatPromptTemplate.from_messages([system_prompt, human_text_prompt])

# Table summarization
human_table_prompt = HumanMessagePromptTemplate.from_template(
    "Summarize the following table or tabular data, highlighting key patterns, trends, and findings:\n{content}"
)
table_prompt_template = ChatPromptTemplate.from_messages([system_prompt, human_table_prompt])

# Image summarization (using metadata)
human_image_prompt = HumanMessagePromptTemplate.from_template(
    "Given the following image metadata and description, create a clear and informative summary of the image's contents:\n{metadata}"
)
image_prompt_template = ChatPromptTemplate.from_messages([system_prompt, human_image_prompt])

# ----- LANGCHAIN LLM SETUP -----

# Initialize Gemini 2.5 Flash model via LangChain Community connector
chat_llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0.2,
    max_output_tokens=256,
)

# Create LLM chain for each modality
text_chain = text_prompt_template | chat_llm
table_chain = table_prompt_template | chat_llm
image_chain = image_prompt_template | chat_llm


# ----- SUMMARIZATION FUNCTIONS -----

def summarize_text(content: str) -> str:
    """
    Summarize a text chunk for quick understanding.
    Args:
        content (str): The text to summarize.
    Returns:
        str: The concise summary.
    """
    result = text_chain.invoke({"content": content})
    return result["text"] if "text" in result else str(result)


def summarize_table(content: str) -> str:
    """
    Summarize table or tabular data.
    Args:
        content (str): Table as markdown, CSV, or extracted string.
    Returns:
        str: The summary of the table highlights.
    """
    result = table_chain.invoke({"content": content})
    return result["text"] if "text" in result else str(result)


def summarize_image(metadata: dict) -> str:
    """
    Summarize an image based on its metadata.
    Args:
        metadata (dict): Metadata describing the image content.
    Returns:
        str: The summary of the image.
    """
    # Convert metadata dictionary to a formatted string
    if metadata:
        metadata_str = "\n".join(f"{k}: {v}" for k, v in metadata.items())
    else:
        metadata_str = "No metadata provided."
    result = image_chain.invoke({"metadata": metadata_str})
    return result["text"] if "text" in result else str(result)



