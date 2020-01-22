def get_statistics():
    file = open("statistics.txt").read().rstrip().split("\n")
    file = list(map(int, file))
    return file
