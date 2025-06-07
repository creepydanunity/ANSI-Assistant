
def get_ask_system_prompt(mode: str = "strict"):
    system_prompt = (
        "You are a senior backend engineer reviewing a specific codebase. "
        "Use the provided code context to answer questions about its architecture and implementation."
        "Avoid vague phrases and general programming advice; be specific, confident, and professional."
        if mode == "advisory" else
        "You are a code assistant. Answer strictly based on the provided context. "
        "If the context does not contain the answer, respond with 'No relevant information found.' "
        "Do not make anything up."
    )
    
    return system_prompt

def get_ask_prompt(context, question):
    return f"""The following are code-related descriptions from a project:\n{context}\n\nQuestion: {question}\nAnswer:"""

def get_intent_prompt(question):
    return f"""
    Classify the following question as either "strict" or "advisory".

    Rules:
    - Use "strict" if the question requires factual answers strictly from code.
    - Use "advisory" if the question asks for design advice, recommendations, or architectural insights.

    Only output one word: strict or advisory.

    Question: {question}
    Answer:"""