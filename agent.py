from langgraph.prebuilt import create_react_agent

from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import InMemorySaver
from serpapi import GoogleSearch
llm = ChatGoogleGenerativeAI(
    api_key="AIzaSyDkk4Po9JXSK6mfYWjqZyw18cJE4pyoljg",
    model="gemini-2.5-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2
)




def serpapi_search(query: str):
    """Searches for a query using the SerpAPI."""
    params = {
        "q": query,
        "hl": "en",
        "gl": "us",
        "api_key": "7de2e832152c918073367fed1631df7586a1e021d5465a15706ae32af46af37c"
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    
    # Extract top results (titles + links)
    if "organic_results" in results:
        return [
            {"title": r["title"], "link": r["link"], "snippet": r.get("snippet", "")}
            for r in results["organic_results"][:5]
        ]
    return {"error": "No results found"}



# Create an agent with Checkpointer Memory
memory = InMemorySaver()

agent = create_react_agent(
    model=llm,
    tools=[serpapi_search],
    prompt="You are a helpful assistant",
    checkpointer=memory
)

# Run the agent
response=agent.invoke(
    {"messages": [{"role": "user", "content": "Who won in the 2nd Sep Pak Cricket match"}]},
    config={"configurable": {"thread_id": "user123"}}
)

# Last Message
print(response['messages'][-1].content)
