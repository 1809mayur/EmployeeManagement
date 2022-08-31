def lcs(i, j, count, X, Y):
 
    if (i == 0 or j == 0):
        return count
 
    if (X[i - 1] == Y[j - 1]):
        count = lcs(i - 1, j - 1, count + 1, X, Y)
 
    count = max(count, max(lcs(i, j - 1, 0, X, Y),
                           lcs(i - 1, j, 0, X, Y)))
 
    return count
 
 
# Driver code
def longestSpecialSubstring(c,s):
    X = ""
    for i in c:
        X += i
    Y = s
    n = len(X)
    m = len(Y)
    ans = lcs(n, m , 0, X, Y)
    return ans

if __name__ == "__main__":
    m = int(input())
    c = []
    for i in range(m):
        c.append(str(input()))
    
    s = str(input())

    res = longestSpecialSubstring(c,s)
    print(res)



