import pickle 
import pandas as pd
import re
from sklearn.metrics.pairwise import cosine_similarity
from fuzzywuzzy  import fuzz

class Recommender:
    def __init__(self, recommend_on='desc'):
        DATA_PATH = "../data/processed/nlp.csv"
        self.df = pd.read_csv(DATA_PATH)
        # removing extra columns
        self.df = self.df.iloc[:,2:]

        with  open(f'{recommend_on}_embeddings.pkl', 'rb') as e:
            embeddings = pickle.load(e)

        self.cos_matrix = cosine_similarity(embeddings)

    def have_common_word(self, str1, str2):
    # Split strings into sets of words
        words1 = set(str1.split())
        words2 = set(str2.split())
        
        # Check for intersection between the two sets
        return bool(words1 & words2)


    def similarity_score(self, A, B):
            similarity = fuzz.ratio(A, B)  # Adjust threshold based on needs
            # print(f"'{A}' and '{B}' are similar with a similarity score of {similarity}")
            return similarity
        
   
    def auto_suggest(self, query, suggestions, n=5):
        # Return all suggestions containing the query as a substring
        suggestions = list(self.df['name'].astype('str').values)
        matches = [s for s in suggestions if query in s.lower()]
        return matches[:n]
    
   
    def generate_recommendations(self, app_name=None, app_index=None):
        """
        Generates recommendations based on similarity to the description or features of a given app
        """

        self.app_index = self.df[self.df['name'] == app_name].index[0] if app_index == None else app_index
        self.app_name = self.df.iloc[app_index]['name'] if app_name == None else app_name
        self.app_dev = self.df.iloc[app_index]['developer']
        self.app_cat= self.df.iloc[app_index]['category']

        simliarity_vector = self.cos_matrix[app_index]
        recommendations = sorted(enumerate(simliarity_vector), reverse=True, key=lambda x: x[1])
        self.recommended_indices =[x[0] for x in recommendations]
        self.recommended_df = self.df.iloc[self.recommended_indices][["name", 'developer', 'category']]
        # print(self.recommended_df)
        print("App to be recommended for", self.df.iloc[app_index]['name'])


    def you_might_like(self, app_name=None, app_index=None, n_recommendations=5):
        """
        Filters the recommendations to be a different from the developer of the app
        """

        self.generate_recommendations(app_name=app_name, app_index=app_index)
        count = 0
        final_indices = []
        for index,name, dev, cat in zip(self.recommended_indices,self.recommended_df['name'], self.recommended_df['developer'].values, self.recommended_df['category'].values):
            print(index, name, dev, cat)
            # This similarity score so that the same app but different year is not recommended 
            ss = self.similarity_score(dev, self.app_dev)
            print(ss)
            if ss < 30: 
                # print('ok')
                final_indices.append((index, name))
                count +=1
            if count == n_recommendations:
                return final_indices
            
            

if __name__ == "__main__":
    recommender = Recommender()
    print("final", recommender.you_might_like(app_index=1))

