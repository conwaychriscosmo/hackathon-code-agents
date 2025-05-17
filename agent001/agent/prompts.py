from langchain.prompts import PromptTemplate

# A reusable prompt template to generate clean Python code
CODE_GENERATION_PROMPT = PromptTemplate.from_template(\"\"\"
You are a professional software engineer. Your task is to write clean, tested Python code based on a task description.

Task ID: {ticket_id}
Title: {title}
Description: {description}
Acceptance Criteria:
{acceptance_criteria}

Instructions:
- Create a Python function in a .py file.
- Include a test file with at least 2 tests.
- Follow Pythonic naming conventions.
- Return only file names and their full contents as a dictionary.

Respond in JSON format:
{{
  \"main.py\": \"...code...\",
  \"test_main.py\": \"...test code...\"
}}
\"\"\")
