import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split


class LinearRegression:

    def __init__(self, learning_rate=0.01, iterations=1000):
        self.lr = learning_rate
        self.n_iters = iterations

    def fit(self, X, y):
        self.X = X
        self.y = y
        self.m, self.n = self.X.shape

        self.w = np.zeros(self.n)
        self.b = 0
        
        for i in range(self.n_iters):
            self._update_weights()

    def _update_weights(self):
        y_pred = self.predict(self.X)
        error = y_pred - self.y

        dW = 2 * (self.X.T).dot(error) / self.m
        dB = 2 * np.sum(error) / self.m

        self.w -= self.lr * dW
        self.b -= self.lr * dB

    def predict(self, X):
        return np.dot(X, self.w) + self.b
    
df = pd.read_csv( "salary_dataset.csv" )

X = df.iloc[:, 1:2].values

Y = df.iloc[:, 2].values

X_train, X_test, Y_train, Y_test = train_test_split( 
    X, Y, test_size = 0.2, random_state = 0)

model = LinearRegression(learning_rate=0.0001, iterations=1000)

model.fit(X_train, Y_train)

#
#  Prediction on test set

Y_pred = model.predict( X_test )

print( "Predicted values ", np.round( Y_pred[:3], 2 ) ) 

print( "Real values      ", Y_test[:3] )

print( "Trained W        ", round( model.w[0], 2 ) )

print( "Trained b        ", round( model.b, 2 ) )