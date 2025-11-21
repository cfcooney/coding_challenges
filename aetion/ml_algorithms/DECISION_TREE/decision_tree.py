import math
from collections import Counter

def entropy(labels):
    """Calculate entropy of a list of labels."""
    counts = Counter(labels)
    total = len(labels)
    return -sum((count/total) * math.log2(count/total) for count in counts.values())

def split_dataset(X, y, feature, threshold):
    """Split numerical features based on threshold."""
    left_X, left_y, right_X, right_y = [], [], [], []
    for xi, yi in zip(X, y):
        if xi[feature] <= threshold:
            left_X.append(xi)
            left_y.append(yi)
        else:
            right_X.append(xi)
            right_y.append(yi)
    return left_X, left_y, right_X, right_y

def best_split(X, y):
    """Find best feature and threshold using information gain."""
    base_entropy = entropy(y)
    best_gain = 0
    best_feature = None
    best_threshold = None

    n_features = len(X[0])

    for f in range(n_features):
        values = sorted(set(x[f] for x in X))
        # Try midpoints between unique values
        thresholds = [(values[i] + values[i+1]) / 2 for i in range(len(values)-1)]
        
        for t in thresholds:
            left_X, left_y, right_X, right_y = split_dataset(X, y, f, t)
            if not left_y or not right_y:  
                continue
            
            # Weighted entropy of children
            p_left = len(left_y) / len(y)
            gain = base_entropy - (p_left * entropy(left_y) + (1 - p_left) * entropy(right_y))
            
            if gain > best_gain:
                best_gain = gain
                best_feature = f
                best_threshold = t

    return best_feature, best_threshold, best_gain

class DecisionTree:
    def __init__(self, max_depth=5):
        self.max_depth = max_depth
        self.tree = None

    def build(self, X, y, depth):
        # If all labels identical → leaf
        if len(set(y)) == 1:
            return y[0]
        
        # Stop if no depth left
        if depth == self.max_depth:
            return Counter(y).most_common(1)[0][0]
        
        feature, threshold, gain = best_split(X, y)
        
        # If no usable split → leaf
        if feature is None or gain == 0:
            return Counter(y).most_common(1)[0][0]

        left_X, left_y, right_X, right_y = split_dataset(X, y, feature, threshold)

        return {
            "feature": feature,
            "threshold": threshold,
            "left": self.build(left_X, left_y, depth + 1),
            "right": self.build(right_X, right_y, depth + 1),
        }

    def fit(self, X, y):
        self.tree = self.build(X, y, 0)

    def predict_one(self, x, node):
        if not isinstance(node, dict):
            return node
        
        if x[node["feature"]] <= node["threshold"]:
            return self.predict_one(x, node["left"])
        else:
            return self.predict_one(x, node["right"])

    def predict(self, X):
        return [self.predict_one(x, self.tree) for x in X]


# --- Example usage ---

X = [
    [5.1, 3.5],
    [4.9, 3.0],
    [6.2, 3.4],
    [5.9, 3.0],
]
y = ["A", "A", "B", "B"]

tree = DecisionTree(max_depth=3)
tree.fit(X, y)

print("Tree:", tree.tree)
print("Prediction:", tree.predict([[5.0, 3.2]]))