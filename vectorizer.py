from txt_file_processor import process_txt_in_directory
import chromadb
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction

# EMBED_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"
# EMBED_MODEL = "all-MiniLM-L6-v2"
# emb_fn = SentenceTransformerEmbeddingFunction(model_name=EMBED_MODEL)

emb_fn = DefaultEmbeddingFunction()


chroma_client = chromadb.PersistentClient(path="./chroma_db")


def vectorize(file_directory):
    # chunks = process_pdfs_in_directory(file_directory)
    collection_with_chunks = process_txt_in_directory(file_directory)
    for collection, chunks in collection_with_chunks.items():
        collection = chroma_client.get_or_create_collection(name=collection, embedding_function=emb_fn)
        collection.add(documents=chunks, ids=[str(i) for i in range(1, len(chunks)+1)])


if __name__ == '__main__':

    DATA_FILE_PATH = "./data"
    vectorize(DATA_FILE_PATH)


    ########### Testing after Vectorizing ############
    # query_text = """ATP70 Washing Machine Price"""
    
    # collection = chroma_client.get_collection(name="walton_website_data", embedding_function=emb_fn)
    # results = collection.query(query_texts=[query_text], where_document={"$contains": "ATP70"}, n_results=10)


    # if results and results["documents"]:
    #     retrieved_docs = results["documents"][0]

    # context_text = "\n\n".join(retrieved_docs) if retrieved_docs else "No Relevant information was found"

    # print(context_text)