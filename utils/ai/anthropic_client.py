"""
Anthropic client utilities for gcPanel AI features.

This module provides integration with the Anthropic API for AI-powered features
in the gcPanel Construction Management Dashboard.
"""

import os
import sys
import anthropic
from anthropic import Anthropic

def get_anthropic_client():
    """
    Initialize and return the Anthropic client.
    
    Returns:
        Anthropic: An initialized Anthropic client instance.
        
    Raises:
        SystemExit: If the Anthropic API key is not set.
    """
    # the newest Anthropic model is "claude-3-5-sonnet-20241022" which was released October 22, 2024
    anthropic_key = os.environ.get('ANTHROPIC_API_KEY')
    
    if not anthropic_key:
        return None
    
    return Anthropic(api_key=anthropic_key)

def analyze_document(document_text, query):
    """
    Analyze document text with a specific query using Anthropic's Claude.
    
    Args:
        document_text (str): The text content of the document to analyze.
        query (str): The specific question or analysis request.
        
    Returns:
        str: The AI analysis result.
    """
    client = get_anthropic_client()
    
    if not client:
        return "Anthropic API key not configured. Please add the ANTHROPIC_API_KEY to your environment variables."
    
    try:
        # the newest Anthropic model is "claude-3-5-sonnet-20241022" which was released October 22, 2024
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text", 
                            "text": f"You are a construction management AI assistant. I have a project document that I need you to analyze:\n\n{document_text}\n\nMy specific question is: {query}"
                        }
                    ]
                }
            ]
        )
        
        # Access content safely
        if message.content and len(message.content) > 0:
            if hasattr(message.content[0], 'text'):
                return message.content[0].text
            else:
                return str(message.content[0])
        return "No analysis could be generated."
    except Exception as e:
        return f"Error connecting to Anthropic API: {str(e)}"

def generate_project_insights(project_data):
    """
    Generate insights about project data using Anthropic's Claude.
    
    Args:
        project_data (dict): Project data in a structured format.
        
    Returns:
        str: AI-generated insights about the project.
    """
    client = get_anthropic_client()
    
    if not client:
        return "Anthropic API key not configured. Please add the ANTHROPIC_API_KEY to your environment variables."
    
    try:
        # Convert project data to a text representation
        project_text = "\n".join([f"{key}: {value}" for key, value in project_data.items()])
        
        # the newest Anthropic model is "claude-3-5-sonnet-20241022" which was released October 22, 2024
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1500,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"You are a construction management AI assistant. Here is the current project data:\n\n{project_text}\n\nBased on this information, provide insights about the project status, identify potential issues, and suggest recommendations for improving project performance."
                        }
                    ]
                }
            ]
        )
        
        # Access content safely
        if message.content and len(message.content) > 0:
            if hasattr(message.content[0], 'text'):
                return message.content[0].text
            else:
                return str(message.content[0])
        return "No insights could be generated."
    except Exception as e:
        return f"Error connecting to Anthropic API: {str(e)}"

def generate_risk_analysis(project_data, timeframe="next_30_days"):
    """
    Generate risk analysis for a construction project using Anthropic's Claude.
    
    Args:
        project_data (dict): Project data in a structured format.
        timeframe (str): The timeframe for risk analysis (next_30_days, next_90_days, project_completion).
        
    Returns:
        str: AI-generated risk analysis.
    """
    client = get_anthropic_client()
    
    if not client:
        return "Anthropic API key not configured. Please add the ANTHROPIC_API_KEY to your environment variables."
    
    try:
        # Convert project data to a text representation
        project_text = "\n".join([f"{key}: {value}" for key, value in project_data.items()])
        
        timeframe_prompt = {
            "next_30_days": "Focus on immediate risks in the next 30 days.",
            "next_90_days": "Focus on medium-term risks over the next 90 days.",
            "project_completion": "Focus on risks from now until project completion."
        }.get(timeframe, "Focus on immediate risks in the next 30 days.")
        
        # the newest Anthropic model is "claude-3-5-sonnet-20241022" which was released October 22, 2024
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1500,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"You are a construction risk management AI assistant. Here is the current project data:\n\n{project_text}\n\n{timeframe_prompt}\n\nIdentify the top 5 risks, rate their likelihood and impact on a scale of 1-5, and provide specific mitigation strategies for each."
                        }
                    ]
                }
            ]
        )
        
        # Access content safely
        if message.content and len(message.content) > 0:
            if hasattr(message.content[0], 'text'):
                return message.content[0].text
            else:
                return str(message.content[0])
        return "No risk analysis could be generated."
    except Exception as e:
        return f"Error connecting to Anthropic API: {str(e)}"