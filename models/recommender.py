import pickle 
import pandas as pd
import re
from sklearn.metrics.pairwise import cosine_similarity
from fuzzywuzzy  import fuzz

class Recommender:
    def __init__(self):
        df = pd.read_csv('nlp_df.csv')
        self.df = df.iloc[:,2:]

        with  open('embeddings.pkl', 'rb') as e:
            embeddings = pickle.load(e)

        self.cos_matrix = cosine_similarity(embeddings)

    def similarity_score(self, A, B):
            similarity = fuzz.ratio(A, B)  # Adjust threshold based on needs
            # print(f"'{A}' and '{B}' are similar with a similarity score of {similarity}")
            return similarity
        
    def recommend(self, app_name):
        df, cos_matrix = self.df, self.cos_matrix

        app_index = df[df['name'] == app_name].index[0]
        app_dev = df.iloc[app_index]['developer']
        app_cat= df.iloc[app_index]['category']

        simliarity_vector = cos_matrix[app_index]
        recommendations = sorted(enumerate(simliarity_vector), reverse=True, key=lambda x: x[1])
        recommended_indices =[x[0] for x in recommendations]
        recommended_df = df.iloc[recommended_indices][["name", 'developer', 'category']]
        print(recommended_df)
        
        count = 0
        for i, dev, cat in zip(recommended_indices, recommended_df['developer'].values, recommended_df['category'].values):
            final_indices = []
            # This similarity score so that the same app but different year is not recommended 
            if self.similarity_score(dev, app_dev)<100:
                final_indices.append(i)
                count +=1
            if count == 5:
                return final_indices

                


if __name__ == "__main__":
    recommender = Recommender()
    print(recommender.recommend('reaConverter Pro 2021'))
