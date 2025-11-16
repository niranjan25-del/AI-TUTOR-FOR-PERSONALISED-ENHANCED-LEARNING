import json
import os
import re
import google.generativeai as genai

# Set up Gemini API key (use environment variables in production)
GEMINI_API_KEY = "AIzaSyBWf9DqAOLq26z1IxV0gb4u1ZTkcwpnigM"

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Define model name
MODEL_NAME = "gemini-2.0-flash-exp"

# Define directories and master files
BASE_DIR = "C:\\Users\\91959\\Downloads\\AI-Tutor-main (1)\\AI-Tutor-main"
LESSONS_DIR = os.path.join(BASE_DIR, "lessons")
QUIZZES_DIR = os.path.join(BASE_DIR, "quizzes")
MASTER_LESSONS_FILE = os.path.join(BASE_DIR, "all_lessons.json")
MASTER_QUIZZES_FILE = os.path.join(BASE_DIR, "all_quizzes.json")

# Ensure directories exist
os.makedirs(LESSONS_DIR, exist_ok=True)
os.makedirs(QUIZZES_DIR, exist_ok=True)

# Topics for lessons and quizzes
topics = [
    "Introduction to Python",
    "Variables and Data Types",
    "Conditionals",
    "Loops",
    "Functions"
]

# Gemini prompt templates with strict JSON formatting instructions

lesson_prompt = """Generate a structured JSON lesson for the topic "{topic}". 
The JSON output **must** strictly follow this format:

```json
{{
  "title": "{topic}",
  "content": [
    "A brief and clear introduction to the topic.",
    "Key concepts related to {topic}.",
    "Explain important aspects concisely.",
    "Provide an example where applicable.",
    "Example:\n\"\"\"\n# Relevant code example\n\"\"\""
  ]
}}
```"""




# Updated quiz prompt to generate exactly 50 MCQs.
quiz_prompt = """Generate a structured JSON quiz for the topic "{topic}" that includes exactly 50 multiple choice questions. Each question should have the keys "question", "options" (a list of 4 options), and "answer". The response must be strictly valid JSON and enclosed within triple backticks like ```json ... ``` with no additional text.

Output:
```json
{{
  "title": "{topic} Quiz",
  "questions": [
    {{
      "question": "Question 1: Enter question text here",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "answer": "Option A"
    }},
    {{
      "question": "Question 2: Enter question text here",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "answer": "Option A"
    }},
    {{
      "question": "Question 3: Enter question text here",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "answer": "Option A"
    }},
    {{
      "question": "Question 4: Enter question text here",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "answer": "Option A"
    }},
    {{
      "question": "Question 5: Enter question text here",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "answer": "Option A"
    }},
    // The quiz should continue with question 6 through question 50.
    // **Important:** Do not include any ellipses or commentary in the final JSON; the output must list 50 complete question objects.
  ]
}}
```"""


def extract_json(response_text):
    """Extract JSON enclosed in triple backticks from the Gemini response."""
    print("\n🧐 RAW RESPONSE FROM GEMINI:\n", response_text)  # Debugging output

    match = re.search(r'```json\s*([\s\S]*?)\s*```', response_text, re.DOTALL)
    
    if match:
        return match.group(1).strip()
    
    return response_text  # Returning the full response for debugging


def generate_content(prompt):
    """Generates structured JSON content using the Gemini API."""
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)
        json_text = extract_json(response.text.strip())
        return json_text
    except Exception as e:
        print(f"Error generating content: {e}")
        return None

def save_json(data, filepath):
    """Saves structured data to a JSON file (overwrites if exists)."""
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def append_to_master(master_file, new_data):
    """
    Appends new_data to a master JSON file.
    If the master file exists and contains a list, new_data is appended.
    Otherwise, a new list is created.
    """
if os.path.exists(master_file):
        with open(master_file, "r", encoding="utf-8") as f:
            try:
                current_data = json.load(f)
                if not isinstance(current_data, list):
