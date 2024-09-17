import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import pickle

def create_embeddings_from_nlp_df(colname):

    df = pd.read_csv("../data/processed/nlp.csv")
    df = df.iloc[:,2:]

    col_values = df[colname].astype(str).values

    model = SentenceTransformer('all-MiniLM-L6-v2')
    print("making embeddings")
    # Convert descriptions/features to embeddings
    embeddings = model.encode(col_values)
    cos_matrix = cosine_similarity(embeddings)
    print("embeddings done")
    with open(f"{colname}_cos_matrix.pkl", 'wb') as e:
        pickle.dump(cos_matrix, e)

    with open(f"{colname}_embeddings.pkl", 'wb') as e:
        pickle.dump(embeddings, e)

    return embeddings, cos_matrix

if __name__ == "__main__":
    create_embeddings_from_nlp_df('desc')