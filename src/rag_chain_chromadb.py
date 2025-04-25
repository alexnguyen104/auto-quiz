import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

import chromadb

# Load the API key from env variables
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI-API-KEY')
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

RAG_PROMPT_TEMPLATE = """
You are an AI quiz generator. Your task is to create {num_questions} multiple-choice quiz questions based on the following information:

**Information:**
{context}

**Instructions:**

1.  **Carefully read and understand the provided information.**
2.  **Identify the core concepts, key facts, and significant details within the text.**
3.  **Formulate {num_questions} multiple-choice questions that directly test understanding of these main points.** Ensure each question is specific and clearly indicates what knowledge is being assessed. The questions should be in {language}.
4.  **For each question, develop four distinct answer choices (A, B, C, D).** One of these options must be the correct answer, directly supported by the provided information. The other three options should be plausible but clearly incorrect (distractors) to someone who understands the material.
5.  **Ensure that only one answer choice is definitively correct for each question.**
6.  **Avoid making the correct answer consistently the same letter (e.g., always 'A').** Vary the position of the correct answer across the questions.
7.  **Your response must be formatted as a 2-D list in Python syntax.**
8.  **Each inner list (representing a question) must contain exactly 6 elements in the following order:** \[QUESTION, OPTION A, OPTION B, OPTION C, OPTION D, ANSWER].
9.  **The "ANSWER" element should contain the letter (A, B, C, or D) corresponding to the correct answer choice.**

**Example of the desired output format:**

[
    ["What is the primary function of the mitochondria?", "Protein synthesis", "Energy production", "Waste removal", "DNA replication", "B"],
    ["Which gas makes up the majority of Earth's atmosphere?", "Oxygen", "Carbon Dioxide", "Nitrogen", "Hydrogen", "C"]
]
"""

PROMPT = PromptTemplate.from_template(RAG_PROMPT_TEMPLATE)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def create_rag_chain(chunks, user_info):
    # tránh "tenants" error
    chromadb.api.client.SharedSystemClient.clear_system_cache()

    embeddings = OpenAIEmbeddings()
    doc_search = Chroma.from_documents(chunks, embeddings)
    retriever = doc_search.as_retriever(search_type="mmr")
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

    rag_chain = (
        {"context": retriever | format_docs, "num_questions": RunnablePassthrough(), "language": lambda _: user_info["lang"]}
        | PROMPT
        | llm
        | StrOutputParser()
    )

    print("Chain created completely!")

    return rag_chain