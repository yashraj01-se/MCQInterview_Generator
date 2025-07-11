import os
import json
import pandas as pd
import traceback
from PyPDF2 import PdfReader  # Modern PyPDF2 reader

# -------------------------------------------
# Function to read PDF or TXT file
# -------------------------------------------
def read_file(file):
    try:
        file.seek(0)  # Reset pointer for Streamlit uploaded file

        if file.name.endswith(".pdf"):
            text = ""
            reader = PdfReader(file)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
            return text.strip()

        elif file.name.endswith(".txt"):
            return file.read().decode("utf-8").strip()

        else:
            raise Exception("Unsupported file format. Only PDF and TXT files are supported.")

    except Exception as e:
        raise Exception(f"Error reading the file: {str(e)}")
        
def get_table_Data(quiz_input):
    try:
        if not quiz_input:
            raise ValueError("Quiz input is empty.")

        # If quiz_input is string, clean it
        if isinstance(quiz_input, str):
            quiz_input = quiz_input.strip()

            # Remove Markdown code block formatting
            if quiz_input.startswith("```json"):
                quiz_input = quiz_input.replace("```json", "").strip()
            elif quiz_input.startswith("```"):
                quiz_input = quiz_input[3:].strip()
            if quiz_input.endswith("```"):
                quiz_input = quiz_input[:-3].strip()

            # Extract only JSON content
            first_brace = quiz_input.find("{")
            last_brace = quiz_input.rfind("}")
            if first_brace == -1 or last_brace == -1:
                raise ValueError("No JSON object found in the quiz input.")

            json_string = quiz_input[first_brace:last_brace + 1]
            quiz_dict = json.loads(json_string)

        elif isinstance(quiz_input, dict):
            quiz_dict = quiz_input
        else:
            raise ValueError("Quiz input must be a string or dictionary.")

        # Convert JSON to table-friendly list
        table_data = []
        for key, value in quiz_dict.items():
            mcq = value.get("mcq", "")
            options = value.get("options", {})
            correct = value.get("correct", "")
            options_text = "\n".join([f"{opt}: {val}" for opt, val in options.items()])

            table_data.append({
                "MCQ": mcq,
                "Choices": options_text,
                "Correct": correct
            })

        return table_data

    except Exception as e:
        print("Error while converting quiz to table format:")
        traceback.print_exception(type(e), e, e.__traceback__)
        return None