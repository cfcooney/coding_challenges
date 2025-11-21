import numpy as np

def kmeans(X, k=2, max_iters=100, tol=1e-4):
    """
    Simple K-Means clustering implementation.

    Parameters:
        X: numpy array of shape (m, n) - m samples, n features
        k: number of clusters
        max_iters: maximum number of iterations
        tol: tolerance for convergence (change in centroids)

    Returns:
        centroids: final cluster centroids
        labels: cluster assignments for each sample
    """
    m, n = X.shape

    # Step 1: Initialize centroids randomly from the data points
    centroids = X[np.random.choice(m, k, replace=False)]

    for iteration in range(max_iters):
        # Step 2: Assign points to the nearest centroid
        labels = np.array([np.argmin([np.linalg.norm(x - c) for c in centroids]) for x in X])

        # Step 3: Compute new centroids as mean of assigned points
        new_centroids = np.array([X[labels == i].mean(axis=0) for i in range(k)])

        # Step 4: Check for convergence
        if np.all(np.linalg.norm(new_centroids - centroids, axis=1) < tol):
            break

        centroids = new_centroids

    return centroids, labels


# --- Example usage ---
if __name__ == "__main__":
    # Some 2D sample points
    X = np.array([
        [1, 2],
        [1, 4],
        [1, 0],
        [10, 2],
        [10, 4],
        [10, 0]
    ])

    centroids, labels = kmeans(X, k=2)
    print("Centroids:\n", centroids)
    print("Labels:\n", labels)