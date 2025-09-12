from pdf_processor import process_pdfs_in_directory
from txt_file_processor import process_txt_in_directory
import chromadb
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction

# EMBED_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"
# EMBED_MODEL = "all-MiniLM-L6-v2"
# emb_fn = SentenceTransformerEmbeddingFunction(model_name=EMBED_MODEL)

emb_fn = DefaultEmbeddingFunction()


chroma_client = chromadb.PersistentClient(path="./chroma_db")


def vectorize(file_directory, collection):
    chunks = process_pdfs_in_directory(file_directory)
    chunks.extend(process_txt_in_directory(file_directory))
    collection = chroma_client.get_or_create_collection(name=collection, embedding_function=emb_fn)
    collection.add(documents=chunks, ids=[str(i) for i in range(1, len(chunks)+1)])


if __name__ == '__main__':

    DATA_FILE_PATH = "./data"
    COLLECTION="washing_machine_data"
    vectorize(DATA_FILE_PATH, COLLECTION)

    query_text = """ATP70 Washing Machine Price"""
    
    collection = chroma_client.get_collection(name=COLLECTION, embedding_function=emb_fn)
    results = collection.query(query_texts=[query_text], n_results=3)


    if results and results["documents"]:
        retrieved_docs = results["documents"][0]

    context_text = "\n\n".join(retrieved_docs) if retrieved_docs else "No Relevant information was found"

    print(context_text)