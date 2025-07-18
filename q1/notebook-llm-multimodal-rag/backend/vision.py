# backend/vision.py

"""
This module wraps image-to-text and visual content handling using the Gemini 2.5 Flash model via LangChain.
It is designed to generate summaries and extract high-level information from images (or image metadata), supporting multimodal RAG processing.
"""

import os
from typing import Dict, Any
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain
from langchain_community.chat_models import ChatGoogleGenerativeAI

# Load the Gemini API key from environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ----- PROMPT DESIGN -----

# System prompt for robust image content summaries
system_template = (
    "You are an expert visual content analyst. Given an image, its metadata, and context, "
    "write a concise and informative summary focusing on objects, relationships, and details relevant for technical search and reasoning."
)
system_prompt = SystemMessagePromptTemplate.from_template(system_template)

# Human message prompt; {image_data} is expected to be a description or metadata dictionary.
human_image_prompt = HumanMessagePromptTemplate.from_template(
    "Here is the image context (metadata and/or alt text):\n{image_data}\nPlease summarize this image for a technical user."
)
image_prompt_template = ChatPromptTemplate.from_messages([system_prompt, human_image_prompt])

# ----- LANGCHAIN LLM SETUP -----

# Initialize Gemini 2.5 Flash model via LangChain
vision_llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0.1,
    max_output_tokens=256,
)
image_chain = LLMChain(llm=vision_llm, prompt=image_prompt_template)

# ----- CORE IMAGE SUMMARY FUNCTION -----

def analyze_image(image_metadata: Dict[str, Any]) -> str:
    """
    Uses Gemini 2.5 Flash LLM (via LangChain) to summarize an image for retrieval augmentation.
    Args:
        image_metadata (dict): Metadata or contextual description of the image.
    Returns:
        str: Gemini-generated image summary.
    """
    # Format the metadata for prompt input
    if image_metadata:
        image_data_str = "\n".join(f"{k}: {v}" for k, v in image_metadata.items())
    else:
        image_data_str = "No metadata provided."
    # Call the LLM chain to generate the summary
    result = image_chain.invoke({"image_data": image_data_str})
    return result["text"] if "text" in result else str(result)
