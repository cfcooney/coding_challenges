"""
Basic Assumption:

All instances correspond to points in the n-dimensional space where n represents the number of features in any instance.
The nearest neighbors of an instance are defined in terms of the Euclidean distance.

K-Nearest Neighbors Classifier first stores the training examples. During prediction, when it encounters a new instance (or test example) to predict, it finds the K number of training instances nearest to this new instance.  Then assigns the most common class among the K-Nearest training instances to this test instance.

The optimal choice for K is by validating errors on test data. K can also be chosen by the square root of m, where m is the number of examples in the dataset.

Pseudocode:
Store all training examples.
Repeat steps 3, 4, and 5 for each test example.
Find the K number of training examples nearest to the current test example.
y_pred for current test example =  most common class among K-Nearest training instances.
Go to step 2.

1. Create KKN class
2. Create methods for fit, predict euclidian distance, finding neighbors
3. fit just instantiates the data
4. predict would run through test set, find neighbors and find mode of k
5. find_neighbors would iterate through the train set against x and find the distances for each - sort and index for y
6. euclidian - square root of sum of squares of x-xi
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from scipy.stats import mode
from sklearn.neighbors import KNeighborsClassifier

class KNNClassifier:

    def __init__(self, k=3):
        self.k = k

    def fit(self, X_train, y_train):
        self.X_train = X_train
        self.y_train = y_train

        # no_of_training_examples, no_of_features
        self.m, self.n = X_train.shape
        
    def predict(self, X_test):
        self.X_test = X_test

        self.m_test, self.n = self.X_test.shape
        y_pred = np.zeros(self.m_test)

        for i in range(self.m_test):
            x = self.X_test[i]

            neighbors = np.zeros(self.k)
            neighbors = self.find_neighbors(x)

            y_pred[i] = mode(neighbors)[0][0]

        return y_pred
    
    def find_neighbors(self, x):
        """calculate all the euclidean distances between current 
        test example x and training set X_train"""
        euclidian_distances = np.zeros(self.m)

        for i in range(self.m):
            distance = self.euclidian(x, self.X_train[i])
            euclidian_distances[i] = distance

        inds = euclidian_distances.argsort()
        y_train_sorted = self.y_train[inds]
        return y_train_sorted[:self.k]
    
    def euclidian(self, x, x_train):

        return np.sqrt(np.sum(np.square(x - x_train)))
    
if __name__ == '__main__':
    df = pd.read_csv( "diabetes.csv" )

    X = df.iloc[:,:-1].values

    Y = df.iloc[:,-1:].values
    
    # Splitting dataset into train and test set

    X_train, X_test, Y_train, Y_test = train_test_split( 
      X, Y, test_size = 1/3, random_state = 0 )
    
    # Model training
    
    model = KNNClassifier(k=3)
    
    model.fit(X_train, Y_train)

    Y_pred = model.predict( X_test )

    correctly_classified = 0
    count = 0
    
    for count in range( np.size( Y_pred ) ) :
        
        if Y_test[count] == Y_pred[count] :
            
            correctly_classified = correctly_classified + 1

        count = count + 1

    print( "Accuracy on test set by our model       :  ", ( 
      correctly_classified / count ) * 100 )
