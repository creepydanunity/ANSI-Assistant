
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