def question_prompt(document, query, chatHistory):
    contexts = ""
    for context in document:
        contexts += f"{context.page_content}\n"
    prompt = f"""
    <|begin_of_text|><|start_header_id|>system<|end_header_id|>You are a helpful assistant who provides advice for users in Singapore, in getting a BTO flat.
Do not come out with any information not present in the context provided.
Be succinct with your answers.
You do not need to mention that information is taken from the current context.
You may ask the user for more information if there are multiple factors invloved.

Context: {contexts}

History: {chatHistory}

Query: {query}
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
Answer: """
    
    return prompt