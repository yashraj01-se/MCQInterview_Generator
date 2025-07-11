import os
import json
import pandas as pd
import traceback
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain_core.callbacks import CallbackManager, StdOutCallbackHandler

#load_dotenv()
#key=os.getenv("GOOGLE_API_KEY")
os.environ["GOOGLE_API_KEY"] = "AIzaSyBlREC38UpTS0vSPDbNPreurvKxEXCAeuQ"

llm = ChatGoogleGenerativeAI(
    model="models/gemini-1.5-flash",
    temperature=0.7
)

TEMPLATE = """
Text:
{text}

You are an expert MCQ maker. Using ONLY the information in the text above,
generate **{number} unique multiple choice questions** suitable for {subject}
students. Use a {tone} tone.

Return your answer **exactly** in the JSON format shown below (no extra keys,
no markdown). Each question must have **four** options, one correct answer, and
a one line explanation.

### JSON_SCHEMA
{response_json}
"""

prompt = PromptTemplate(
    template=TEMPLATE,
    input_variables=["text", "number", "subject", "tone", "response_json"]
)

generate_quiz = LLMChain(
    llm=llm,
    prompt=prompt,
    output_key="quiz",
    verbose=True 
)

TEMPLATE2 = """
You are an expert English grammarian and writer.  
Given a Multiple Choice Quiz for {subject} students:

• Evaluate the complexity of each question and provide a complete analysis of the quiz (maximum 50 words for the complexity summary).  
• If any question is not in line with the cognitive and analytical abilities of the students, update those questions and adjust the tone so it perfectly fits the students.

Quiz_MCQs:
{quiz}

Check from an expert English writer of the above quiz:
"""

response_json = """
{
  "1": {
    "mcq": "multiple choice question",
    "options": {
      "a": "choice here",
      "b": "choice here",
      "c": "choice here",
      "d": "choice here"
    },
    "correct": "correct answer"
  },
  "2": {
    "mcq": "multiple choice question",
    "options": {
      "a": "choice here",
      "b": "choice here",
      "c": "choice here",
      "d": "choice here"
    },
    "correct": "correct answer"
  },
  "3": {
    "mcq": "multiple choice question",
    "options": {
      "a": "choice here",
      "b": "choice here",
      "c": "choice here",
      "d": "choice here"
    },
    "correct": "correct answer"
  },
  "4": {
    "mcq": "multiple choice question",
    "options": {
      "a": "choice here",
      "b": "choice here",
      "c": "choice here",
      "d": "choice here"
    },
    "correct": "correct answer"
  }
}
"""


quiz_evaluation_prompt = PromptTemplate(
    template=TEMPLATE2,
    input_variables=["subject", "quiz"]
)

review_quiz = LLMChain(
    llm=llm,
    prompt=quiz_evaluation_prompt,
    output_key="review",
    verbose=True 
)

gene_eval_chain = SequentialChain(
    chains=[generate_quiz, review_quiz],
    input_variables=["text", "number", "subject", "tone", "response_json"],
    output_variables=["quiz","review"],
    verbose=True
)


