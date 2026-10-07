import os

def text_2_chunks(txt_file_path, chunk_size=500, overlap=50):

    with open(txt_file_path, "r", encoding='utf-8') as f:
        text = f.read()

    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end == len(text):
            break
        start = end - overlap
    return chunks


def process_txt_in_directory(txt_directory, chunk_size=500, chunk_overlap=50):

    collection_with_chunks = {}
    for filename in os.listdir(txt_directory):
        if filename.lower().endswith(".txt"):
            txt_path = os.path.join(txt_directory, filename)
            print(f"\nProcessing {filename}...")
            chunks = text_2_chunks(txt_path, chunk_size, chunk_overlap)
            collection = os.path.splitext(filename)[0]
            collection_with_chunks[collection] = chunks
            print(f"Total chunks created for {filename}: {len(chunks)}")

    return collection_with_chunks

if __name__ == '__main__':
    chunks = process_txt_in_directory('data/')

    print(chunks[:100])