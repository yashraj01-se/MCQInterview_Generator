import os
import json
import pandas as pd
import traceback
from src.mcq_gen.utils import read_file,get_table_Data
import streamlit as st
from src.mcq_gen.MCQGenerator import gene_eval_chain
from src.mcq_gen.Logger import logging

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

#creating the title:
st.title("MCQ Creator Application with LangChain")

#creating a form using st.form:
with st.form("user_inputs"):
    #loading file:
    uploaded_file=st.file_uploader("Upload a PDF or TXT file.")

    #Input Fields:
    mcq_count=st.number_input("No. of MCQs",min_value=3,max_value=50)

    #Subject:
    subject=st.text_input("Insert Subject",max_chars=20)

    #Quiz Tone:
    tone=st.text_input("Complexity level od Questions",max_chars=20,placeholder="Simple")

    #Add submit Button:
    button=st.form_submit_button("Create MCQs")

    #check if the button id clicked or not and all fields have input or not:

    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("Loading..."):
            try:
                text=read_file(uploaded_file)
                result = gene_eval_chain(
                    {
                         "text": text,            # the passage the MCQs are built from
                         "number": mcq_count,             # how many questions you want
                         "subject": subject,    # or whatever subject
                         "tone": tone,
                         "response_json":response_json
                    }
                    )
            
            except Exception as e:
                traceback.print_exception(type(e),e,e.__traceback__)
                st.error("Error")
                
            else:
                if isinstance(result,dict):
                    quiz=result.get("quiz",None)
                    if quiz is not None:
                        table_data = get_table_Data(quiz)
                        if table_data:
                            df = pd.DataFrame(table_data)
                            df.index = df.index + 1
                            st.table(df)
                            st.text_area(label="Review", value=result["review"])
                        else:
                            st.error("Could not parse quiz data into table format.")

                else:
                    st.write(result)
                
        
    
