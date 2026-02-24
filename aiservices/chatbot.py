import os
from dotenv import load_dotenv
from google.genai import Client

load_dotenv()

client = Client(api_key=os.getenv("GEMINI_API_KEY"))


def get_gemini_answer(question):
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=f"Explain clearly in 5 to 6 point not very long:\n{question}"
    )
    return response.text


def get_answer(db, question):
    results = db.similarity_search_with_score(question, k=3)

    # If no notes loaded or no match
    if not results:
        return f"Answer from internet (Gemini):\n{get_gemini_answer(question)}"

    docs, scores = zip(*results)
    best_score = min(scores)

    SIMILARITY_THRESHOLD = 0.75

    if best_score > SIMILARITY_THRESHOLD:
        return f"Answer from internet (Gemini):\n{get_gemini_answer(question)}"

    context = "\n".join([doc.page_content for doc in docs])

    return f"Answer from your notes:\n{context[:1200]}"


#==================================================== What this code does (very simple)

# Takes a question from the user

# Searches relevant content from notes (FAISS)

# Sends that content to OpenAI

# Returns a clear answer

# ========================================================How it works step by step

# Student asks a question

# FAISS finds matching note content

# OpenAI reads that content

# AI generates an answer

# Answer is returned
