from smolagents import tool
from smolagents import WebSearchTool
# from langchain.tools import tool
import chromadb
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction


# Create Tool
@tool
def database_search(query_texts: list[str], collection: str, where_document: dict|None = None) -> str:
    """
    Retrieve relevant washing machine data from a specified ChromaDB collection
    based on a user query.

    Performs semantic search on the selected collection and returns the most
    relevant documents as a combined text context.

    Args:
        query_texts (list[str]):
            List of user queries used for semantic search. Use list of multiple variant of queries to get better result.

        collection (str): The name of the collection to search. Must be one of:
            - "walton_website_data":
                Contains general washing machine data such as model names, prices, and types from Walton.
            - "AFC90W_error_code":
                Contains error codes and troubleshooting data for AFC90W front load washing machine.
            - "AFE80H_error_code":
                Contains error codes and troubleshooting data for AFE80H front load washing machine.
            - "AFM70_90_error_code":
                Contains error codes and troubleshooting data for AFM series (AFM70, AFM90) front load washing machines.
            - "AFT80W_error_code":
                Contains error codes and troubleshooting data for AFT80W front load washing machine.
            - "ATP60_70_error_code":
                Contains error codes and troubleshooting data for ATP60 and ATP70 top load washing machines.
            - "ATP60_70_user_manual":
                Contains user manuals and detailed information for ATP60 and ATP70 top load washing machines.


        where_document (dict | None, optional):
            Optional filter applied to document content before similarity search
            using ChromaDB's `where_document` syntax. Supports:
            - "$contains": match keyword presence (e.g., {"$contains": "E1"})
            - "$regex": pattern matching (e.g., {"$regex": "E[0-9]"})
            - "$and": combine multiple conditions (e.g., {"$and": [...]})
            - "$or": match any condition (e.g., {"$or": [...]})

            Defaults to None (no filtering).

    Returns:
        str:
            Top matching documents joined by double newlines, or
            "No relevant documents found" if empty.
    """
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    emb_fn = DefaultEmbeddingFunction()
    collection = chroma_client.get_collection(name=collection, embedding_function=emb_fn)
    results = collection.query(query_texts=query_texts, where_document=where_document, n_results=10)

    if results and results["documents"]:
        retrieved_docs = results["documents"][0]

    context_docs = "\n\n".join(retrieved_docs) if retrieved_docs else "No relevant documents found"

    return context_docs

@tool
def walton_website_search(query: str) -> str:
    """
    Search for information specifically from the Walton Bangladesh website (waltonbd.com).
    
    The tool will automatically restrict results to waltonbd.com.
    Retry with a simplified query if the result is "None" i.e. not found.
    
    Use this tool only when the required information nout found in the database.

    Args:
        query (str): The search query describing the user's request.

    Returns:
        str: A summarized result of relevant information from Walton's official website.
    """
    search_tool = WebSearchTool()

    try:
        search_result = search_tool.forward(f"{query} site://waltonbd.com")
        return search_result
    except Exception:
        return None