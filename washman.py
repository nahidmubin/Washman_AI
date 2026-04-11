from huggingface_hub import InferenceClient
import chromadb
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.environ["HUGGINGFACE_API_KEY"]

hf_client = InferenceClient(api_key=API_KEY)

COLLECTION="washing_machine_data"
chroma_client = chromadb.PersistentClient(path="./chroma_db")
emb_fn = DefaultEmbeddingFunction()
collection = chroma_client.get_collection(name=COLLECTION, embedding_function=emb_fn)


def washmans_reply(user_prompt):

    results = collection.query(query_texts=[user_prompt], n_results=10)

    if results and results["documents"]:
        retrieved_docs = results["documents"][0]

    context_docs = "\n\n".join(retrieved_docs) if retrieved_docs else "No relevant documents found"



    # Step 3: Build RAG-enhanced system prompt
    system_prompt = f"""
    You are Walton Washman — an AI assistant for Walton washing machines.
    All responses must be in English, clear, friendly, and step-by-step.

    Use the following manual context if relevant:
    {context_docs}

    Responsibilities:
    1) Troubleshooting using model number, error codes, or symptoms.
    2) Buying guide: model, capacity, front/top load, features.
    3) Usage & maintenance: installation, detergent, cleaning, vibration, noise.
    4) Safety first: never instruct unsafe electrical/water work. Refer to official service if needed.
    """

    # Step 4: Send to LLM
    stream = hf_client.chat.completions.create(
        model="meta-llama/Meta-Llama-3-8B-Instruct",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens=1024,
        stream=True,
    )

    for chunk in stream:
        if not chunk.choices:
            continue

        delta = chunk.choices[0].delta

        if not delta:
            continue

        content = getattr(delta, "content", None)

        if content:
            yield content



if __name__ == "__main__":

    user_prompt = input("What's your question? ")
    reply = washmans_reply(user_prompt)

    print("\n\nModel Response:\n")
    for token in reply:
        print(token, end="", flush=True)
