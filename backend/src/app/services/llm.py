from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

from src.core.config import GEMINI_API_KEY, CHAT_MODEL

llm = ChatGoogleGenerativeAI(
    model=CHAT_MODEL,
    api_key=GEMINI_API_KEY,
    temperature=0.3,
)


def generate_article_summary(article):
    """Generate summary for a specific article."""
    system_prompt = SystemMessagePromptTemplate.from_template("""
    You are an expert article summarizer. Create a concise, informative summary of the provided article.
    
    Guidelines:
    - Keep it 2-3 paragraphs (150-250 words)
    - Focus on the main points and key information
    - Use clear, journalistic style
    - Include important facts, dates, and figures
    - Don't add information not present in the article
    """)

    content = f"Title: {article['title']}\n\nExcerpt: {article['excerpt']}\n\nFull Article:\n{article['content']}"

    human_prompt = HumanMessagePromptTemplate.from_template(f"""
    Please summarize this article:
    
    {content}
    """)

    system_message = system_prompt.format()
    human_message = human_prompt.format(
        title=article['title'],
        excerpt=article['excerpt'],
        content=article['content'],
    )

    response = llm([system_message, human_message])
    return response.content


def generate_summary(query: str, articles: list):
    """Generate summary using Gemini LLM with modern prompt templates."""
    context = "\n\n".join([
        f"Article {i+1}: {article['title']}\n{article['excerpt']}"
        for i, article in enumerate(articles)
    ])

    system_template = """
    You are a news summarization expert. Your task is to generate a clear and concise summary that answers the user's query, using only the most relevant and accurate information from the provided articles.

Guidelines:
- Only use information from the relevant articles
- Do not include unrelated content or mention anything like "article 1" or "the article above"
- If the information is limited, explain that clearly
- Be objective, factual, and long (4-5 paragraphs)
- Maintain a journalistic tone
- Just give summary according to the query, do not add any additional information like "As an AI language model" or "Based on the articles provided"
    """

    human_template = """
    Query: {query}
    
    Articles:
    {context}
    
    Please provide a summary that answers the query based on these articles.
    """

    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(system_template),
        HumanMessagePromptTemplate.from_template(human_template),
    ])

    formatted_prompt = prompt.format_messages(query=query, context=context)
    response = llm.invoke(formatted_prompt)
    return response.content
