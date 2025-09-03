from langchain.prompts import ChatPromptTemplate


def summarize(articles, llm):
    """Summarize retrieved articles with Gemini (LangChain runnable style)."""
    if not articles:
        return "No articles to summarize."

    combined = "\n\n".join(a.page_content for a in articles)

    prompt = ChatPromptTemplate.from_template(
        """
        You are a helpful assistant. Summarize the following news articles into a concise report:
        - Highlight the main events
        - Group similar points together
        - Keep it factual and objective
        - Limit to ~300 words
        - Cite URLs for reference at the end
        - If articles are not relevant, just say "No relevant articles found."

        Articles:
        {articles}

        Summary:
        """
    )

    chain = prompt | llm
    response = chain.invoke({"articles": combined})
    return response.content
