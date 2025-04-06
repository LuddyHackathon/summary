import openai
import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set your OpenAI API key from the environment variable
openai.api_key = os.environ.get("OPENAI_API_KEY")

def get_summary_and_actions(transcript_text, language=None):
    """
    Generates a summary and extracts action items from a meeting transcript.
    If a language is provided, the output will be in that language;
    otherwise, it will use the same language as the transcript.
    The output will be in valid JSON format with two keys: 'summary' and 'action_items'.
    """
    if language:
        language_instruction = f"Provide the summary and action items in {language}."
    else:
        language_instruction = "Provide the summary and action items in the same language as the transcript."
    
    # Craft the prompt with multi-language and JSON output instructions
    prompt = (
        "You are an AI assistant that helps extract key insights from meeting transcripts and supports multiple languages. "
        f"{language_instruction} "
        "Based on the following meeting transcript, provide a concise summary of the discussion and list all action items "
        "with details such as assigned owners, deadlines, or follow-up tasks. "
        "Return the output in valid JSON format with two keys: 'summary' and 'action_items'. "
        "For example:\n"
        '{ "summary": "The meeting discussed...", "action_items": ["Review financial report", "Schedule follow-up meeting"] }\n'
        "\nTranscript:\n" + transcript_text
    )
    
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Use a model you have access to
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
    )
    
    result_text = response.choices[0].message.content
    
    # Try to parse the result as JSON; if parsing fails, return the raw text
    try:
        result_json = json.loads(result_text)
    except json.JSONDecodeError:
        result_json = {"raw_output": result_text}
    
    return result_json

if __name__ == "__main__":
    # New example transcript from a quarterly financial review meeting
    whisper_output = {
        "text": (
            "Hello everyone, welcome to our quarterly financial review meeting. "
            "We reviewed our performance for Q2. "
            "Mark: Our revenue increased by 15% compared to Q1, but our expenses also rose. "
            "Anna: We need to implement cost optimization strategies to improve profitability. "
            "John: I propose setting up a detailed follow-up meeting with the finance team next week. "
            "The meeting concluded with the decision to analyze expense reports further."
        ),
        "segments": [
            {"id": 0, "start": 0.0, "end": 6.0, "text": "Hello everyone, welcome to our quarterly financial review meeting."},
            {"id": 1, "start": 6.1, "end": 12.0, "text": "We reviewed our performance for Q2."},
            {"id": 2, "start": 12.1, "end": 18.0, "text": "Mark: Our revenue increased by 15% compared to Q1, but our expenses also rose."},
            {"id": 3, "start": 18.1, "end": 24.0, "text": "Anna: We need to implement cost optimization strategies to improve profitability."},
            {"id": 4, "start": 24.1, "end": 30.0, "text": "John: I propose setting up a detailed follow-up meeting with the finance team next week."},
            {"id": 5, "start": 30.1, "end": 36.0, "text": "The meeting concluded with the decision to analyze expense reports further."}
        ]
    }

    # Extract the transcript text from the Whisper AI JSON output
    transcript_text = whisper_output.get("text", "")
    
    # Force output in Spanish for this example
    result = get_summary_and_actions(transcript_text, language="")
    print(json.dumps(result, indent=4, ensure_ascii=False))
