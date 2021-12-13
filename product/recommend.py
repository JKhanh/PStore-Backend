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
        items = []
        # highest_similarity = -np.inf
        # highest_similarity_item = None
        item_index = self.items.index(item_id)
        # item_index = 10
        # print(item_index)
        try:
            item_index = item_index[0]
            for col in range(0, self.vh.shape[1]):
                if col == item_index:
                    continue
                similarity = cosine_similarity(self.vh[:,item_index], self.vh[:, col])
                items.append((col, similarity))
                # if similarity > highest_similarity and col != item_index:
                #     highest_similarity = similarity
                #     highest_similarity_item = col

            return sorted(items, key=lambda x: x[1], reverse=True)[:10]
        except:
            return "Item not found"

if __name__ == "__main__":
    rec = Recommend()
    print(rec.recommend_by_item('B001B39Y6Q'))
