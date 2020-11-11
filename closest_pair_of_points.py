import math

def euclidean_distance(player, out): 
    return math.sqrt(math.pow( (player[0] - out[0]), 2) + math.pow( (player[1] - out[1]), 2) )

def distance(X, n):
    min_dist = euclidean_distance(X[0], X[1])

    for i,(x,y) in enumerate(X):
        for j in range(i+1, n):
            if distance(X[i], X[j]) < min_dist:
                min_dist = distance(X[i], X[j])  
    
    return min_dist
