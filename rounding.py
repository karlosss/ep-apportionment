from math import ceil, floor, sqrt


def standard(x):
    if x-int(x) < 0.5:
        return int(x)
    return int(x)+1


def geometric(x):
    if x < sqrt(x*(x+1)):
        return int(x)
    return int(x+1)


def harmonic(x):
    if x < (x*(x+1)) / (x+0.5):
        return int(x)
    return int(x+1)
