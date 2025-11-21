import numpy as np
from scipy.spatial.distance import cosine
from sklearn.datasets import load_diabetes
from sklearn.metrics import root_mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor


# Read dataset for regression
dataset = load_diabetes()

# print(dataset.head())
# print(dataset.info())
x = dataset["data"]
y = dataset["target"]



x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=1)


def knn(x_train: np.ndarray, y_train: np.ndarray, x_test: np.ndarray, k: int = 3) -> np.ndarray:
    """
    Predicts value for each row in x_test using the k-nearest neighbors regression algorithm, using the
    data in (x_train, y_train) as reference / neighbors.
    """
    all_preds = np.zeros(x_test.shape[0])
    for i, x in enumerate(x_test):
        distance_to_train = np.zeros(x_train.shape[0])
        for x_i in x_train:
            distance_to_train[i] = _distance(x, x_i)
            print(distance_to_train)
            index = np.argsort(distance_to_train)
            y_preds = y_train[index]
            y_preds = y_preds[:k]

        all_preds[i] = np.mean(y_preds)

    # TODO: implement this function
    return all_preds #np.zeros(x_test.shape[0])


def _distance(x: np.ndarray, y: np.ndarray) -> float:
    """Calculate cosine distance between 2 vectors"""
    return cosine(x, y)


if __name__ == "__main__":
    # Solution using custom implementation
    predictions = knn(x_train, y_train, x_test, k=3)
    rmse = root_mean_squared_error(y_test, predictions)
    print("RMSE:", rmse)

    # Solution using scikit-learn
    model = KNeighborsRegressor(n_neighbors=3)
    model.fit(x_train, y_train)
    model_preds = model.predict(x_test)
    model_rmse = root_mean_squared_error(y_test, model_preds)
    print("RMSE from sklearn:", model_rmse)
