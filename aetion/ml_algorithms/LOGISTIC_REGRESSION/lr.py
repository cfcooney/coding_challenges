"""
Logistic regression is a statistical method used for binary classification tasks where we need to categorize data into one of two classes. 
The algorithm differs in its approach as it uses curved S-shaped function (sigmoid function) for plotting any real-valued input to a value between 0 and 1.
"""

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
#import matplotlib.pyplot as plt

class LogisticRegression:
    def __init__(self, learning_rate=0.01, iterations=1000):
        self.learning_rate = learning_rate
        self.iterations = iterations
        self.weights = None
        self.bias = 0
        self.loss_history = []

    def sigmoid(self, z):
        """Sigmoid activation function. Takes a linear set of outputs and compresses into a probability distribution."""
        return 1 / (1 + np.exp(-z))

    def loss(self, h, y):
        """cross-entropy loss. calculates how wrong your predictions are.
        True label 1 → penalty = -log(model’s predicted probability for 1)
        True label 0 → penalty = -log(model’s predicted probability for 0)"""
        m = len(y)
        return - (1/m) * np.sum(y*np.log(h) + (1-y)*np.log(1-h))

    def fit(self, X, y):
        m, n = X.shape
        self.weights = np.zeros(n)

        for _ in range(self.iterations):
            z = np.dot(X, self.weights) + self.bias
            #print(f"Sigmoid input: {z}")
            h = self.sigmoid(z)
            #print(f"Sigmoid output: {h}")
            # these lines calculate the gradient, telling the model how to adjust the weights to reduce loss
            # h-y is the prediction error
            # Computes the derivative of the loss with respect to the weights
            dw = (1/m) * np.dot(X.T, (h - y))
            db = (1/m) * np.sum(h - y)

            self.weights -= self.learning_rate * dw
            self.bias -= self.learning_rate * db

            self.loss_history.append(self.loss(h, y))

    def predict(self, X):
        return (self.sigmoid(np.dot(X, self.weights) + self.bias) >= 0.5).astype(int)
    

if __name__ == '__main__':
    np.random.seed(42)
    X = np.random.rand(200, 2) * 10
    y = (X[:, 0] + X[:, 1] > 10).astype(int)

    # Split into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Scale the data for faster convergence
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Train our logistic regression model
    model = LogisticRegression(learning_rate=0.1, iterations=1000)
    model.fit(X_train, y_train)

    # Evaluate accuracy
    predictions = model.predict(X_test)
    accuracy = np.mean(predictions == y_test)
    print(f"Model Accuracy: {accuracy:.2f}")