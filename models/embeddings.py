# %%
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import matplotlib.pyplot as plt
import pickle

### THis file makes the cosine_matrix using embedding model from huggingface

# %%
df = pd.read_csv("nlp_df.csv")

# %%
df = df.iloc[:,2:]

# %%
# %%
features = list(df['features'].values)

# %%
model = SentenceTransformer('all-MiniLM-L6-v2')

# Convert descriptions to embeddings
embeddings = model.encode(features)
cos_matrix = cosine_similarity(embeddings)

with open("cos_matrix.pkl", 'wb') as e:
    pickle.dump(cos_matrix, e)

with open("embeddings.pkl", 'wb') as e:
    pickle.dump(embeddings, e)