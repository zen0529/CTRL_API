

async def llm_query(energy_level : int, energy_states : list, emotional_states: list, mental_states: list):
    try:

        template = """
        TOPCIT (Test of Practical Competency in IT) is designed to assess competencies in practical IT skills such as programming, algorithm problem-solving, and 
        IT business understanding. TOPCIT questions are typically scenario-based, requiring critical thinking and practical application of knowledge in areas like 
        software development, database management, algorithms, and IT ethics.  Use the context to generate scenarios before creating a question.
        You are an Information Technology College Teacher tasked to create simulated exam questions for TOPCIT.

        The context provides key information for creating exam questions. Ensure every question explicitly references or relies on details from the context.
        Always use the information provided in <context> to generate your answers. Do not include any details that are not directly supported by the context.
        Don't reference the context without explicitly putting it in the question.
        <context>
        {context}
        </context>

        Query: {input}
        """

        prompt_template = PromptTemplate(template=template)
        
        prompt_text = prompt_template.invoke({"context": context, "input": input})
        
        response = LLM.invoke(prompt_text)
        return response.content

    except Exception as e:
        raise ValueError(f"An error occurred while querying the RAG model: {str(e)}")