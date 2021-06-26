

def gcd(a,b):
    '''recursive Euclid algorithm'''
    if b == 0:
        return a
    else:
        return gcd(b, a%b)

