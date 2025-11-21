"""
Not really fitting as such but we define the training data
predict method, euclidan distance, find neigbors
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from scipy.stats import mode
from sklearn.neighbors import KNeighborsClassifier

class KNNClassifier:

    def __init__(self, k=3):
        self.k = k

    def fit(self, X, y):
        self.X = X
        self.y = y
        self.m, self.n = self.X.shape

    def predict(self, X_test):
        """loop through test set"""
        self.X_test = X_test
        self.m_test, self.n_test = self.X_test.shape
        self.preds = np.zeros(self.m_test)

        for i in range(self.m_test):
            neigbors = self.find_neighbors(X_test[i])
            neigbors = mode(neigbors)[0][0]

            self.preds[i] = neigbors
        return self.preds


    def find_neighbors(self, x):
        """oop through train set"""
        distance = np.zeros(self.m)

        for i in range(self.m):
            distance[i] = self.euclidian(x, self.X[i])

        index = distance.argsort()
        y_preds = self.y[index]
        return y_preds[:self.k]
    
    def euclidian(self, x, x_i):
        return np.sqrt(np.sum(np.square(x - x_i)))

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


   



    def euclidian(self, x, x_i):
        return np.sqrt(np.sum(np.square(x - x_i)))