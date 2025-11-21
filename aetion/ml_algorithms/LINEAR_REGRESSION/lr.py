"""
he formula for linear regression is 𝑦 = 𝛽₀ + 𝛽₁𝑥₁ + ⋯ + 𝛽ᵣ𝑥ᵣ + 𝜀, representing the linear relationship between variables.
Simple linear regression involves one independent variable, whereas multiple linear regression involves two or more.
h( x ) = w * x + b  
    
  here, b is the bias.
  x represents the feature vector
  w represents the weight vector.
"""
"""
We want to fit a weight matrix and a bias term.
We want to mimimize the loss and can use gradient descent for that.
1. Define a linear regression class with inits
2. Add a fit, update, and predict method
3. fit initializes variables and iterates
4. in update weights we make a prediction, update weight and bias derivatives,
update weights and bias with learning rate
5. predict is dot-product of X and weights plus bias - as in formula
"""


import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
#import matplotlib.pyplot as plt


class LinearRegression:

    def __init__(self, learning_rate, iterations):
        self.learning_rate = learning_rate
        self.iterations = iterations
        self.loss_history = []

    def fit(self, X, y):

        self.m, self.n = X.shape # samples by features

        self.weights = np.zeros(self.n)
        self.bias = 0
        self.X = X
        self.y = y

        for i in range(self.iterations):
            self._update_weights()

        return self

    def _update_weights(self):
        y_pred = self.predict(self.X)
        
        # Calculate loss (Mean Squared Error)
        loss = np.mean((y_pred - self.y) ** 2)
        self.loss_history.append(loss)

        dW = (2 * (self.X.T).dot(y_pred - self.y)) / self.m

        dB = 2 * np.sum(y_pred - self.y) / self.m

        self.weights = self.weights - self.learning_rate * dW
        self.bias = self.bias - self.learning_rate * dB

        return self

    def predict(self, X):
        
        return X.dot(self.weights) + self.bias
    
if __name__ == '__main__':
    #import kagglehub

    # Download latest version
    # path = kagglehub.dataset_download("abhishek14398/salary-dataset-simple-linear-regression")
    # print("Path to dataset files:", path)

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
    
    print( "Trained W        ", round( model.weights[0], 2 ) )
    
    print( "Trained b        ", round( model.bias, 2 ) )
    
    print( "Initial loss     ", round( model.loss_history[0], 2 ) )
    
    print( "Final loss       ", round( model.loss_history[-1], 2 ) )
