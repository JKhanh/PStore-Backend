import numpy as np
import pandas as pd
import os


def cosine_similarity(v, u):
        return (v @ u) / (np.linalg.norm(v) * np.linalg.norm(u))

class Recommend:
    def __init__(self):
        recommended_path = os.path.join(os.path.dirname(__file__), 'recommended.dat')
        data_path = os.path.join(os.path.dirname(__file__), 'data.pkl')
        self.vh = np.load(recommended_path, allow_pickle=True)
        self.rating_matrix = pd.read_pickle(data_path)
        self.items = self.rating_matrix.columns.to_list()

    def recommend_by_item(self, item_id):
        highest_similarity = -np.inf
        highest_similarity_item = None
        print(self.items[:10])
        item_index = self.items.index(item_id)
        # item_index = 10
        print(item_index)
        try:
            item_index = item_index[0]

            for col in range(0, self.vh.shape[1]):
                similarity = cosine_similarity(self.vh[:,item_index], self.vh[:, col])
                if similarity > highest_similarity and col != item_index:
                    highest_similarity = similarity
                    highest_similarity_item = col

            return self.items[highest_similarity_item]
        except:
            return "Item not found"
