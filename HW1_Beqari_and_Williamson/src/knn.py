from statistics import mode
from sklearn.metrics import accuracy_score
import pandas as pd
import numpy as np

# read in the data
x_train = pd.read_pickle("x_train.pkl");
x_eval  = pd.read_pickle("x_eval.pkl");
x_test  = pd.read_pickle("x_test.pkl");

# *** knn from scratch ***

num_neighbors = 30

def euclidean_distance(x, y):
    return np.linalg.norm(x-y)

def cosine_similarity(x, y):
    return np.dot(x, y) / (np.linalg.norm(x) * np.linalg.norm(y))

def knn(rows, row, num_neighbors):
    distance_and_label = []
    # calculate distance and keep track of labels
    for target_row in rows:
        train_embeddings = np.array(target_row[0])
        test_embeddings = np.array(row)
        distance = cosine_similarity(train_embeddings, test_embeddings)
        label = target_row[1]
        distance_and_label.append([distance, label])
    # sort the list by distance positional element
    # save only the k-th specified neigbors
    sorted_distance_and_label = sorted(distance_and_label, key=lambda x: x[0], reverse=True)[:num_neighbors]
    # return the mode of the neighbors 
    knn_labels = [element[1] for element in sorted_distance_and_label]
    prediction = mode(knn_labels)
    # prediction = max(set(knn_labels), key=knn_labels.count)
    return prediction

# step 3: evaluate
# x_eval["prediction"] = x_eval["embeddings"].apply(lambda row: knn(x_train[["embeddings", "label"]].values.tolist(), row, num_neighbors))
# print(accuracy_score(x_eval["label"].tolist(), x_eval["prediction"].tolist()))

# step 4: predict
x_test["prediction"] = x_test["embeddings"].apply(lambda row: knn(x_train[["embeddings", "label"]].values.tolist(), row, num_neighbors))
x_test["prediction"].to_csv(r'predictions_beqari_and_williamson.txt', header=None, index=None)

# check number of prediction rows
row, col = x_test.shape
print("num rows written: ", row)
