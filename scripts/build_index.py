import pandas as pd
import faiss
import os
import pickle
from sentence_transformers import SentenceTransformer

def build_faiss_index(
    csv_path="data/scitldr_clean.csv",
    index_path="index/abstract.index",
    metadata_path="index/metadata.pkl"
):
    # Load dataset
    print(f"📥 Loading dataset from: {csv_path}")
    df = pd.read_csv(csv_path)

    if "abstract" not in df.columns:
        raise ValueError("CSV must contain an 'abstract' column.")
    
    abstracts = df["abstract"].fillna("").tolist()

    # Load embedding model
    print("🔍 Embedding abstracts with MiniLM...")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(abstracts, show_progress_bar=True)

    # Build FAISS index
    dimension = embeddings[0].shape[0]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    print(f"✅ FAISS index built with {len(embeddings)} entries")

    # Save index
    os.makedirs(os.path.dirname(index_path), exist_ok=True)
    faiss.write_index(index, index_path)
    print(f"💾 Saved index to {index_path}")

    # Save metadata (id, title, abstract, tldr)
    metadata = df[["id", "title", "abstract", "tldr"]].to_dict(orient="records")
    with open(metadata_path, "wb") as f:
        pickle.dump(metadata, f)
    print(f"💾 Saved metadata to {metadata_path}")

# Allow standalone execution
if __name__ == "__main__":
    build_faiss_index()
