def update_statistics(record):
    file = open("statistics.txt").read().rstrip().split("\n")
    file = list(map(int, file))
    top = file[:3]
    print(top)
    if top[0] < record:
        top = [record, top[0], top[1]]
    elif top[1] < record:
        top = [top[0], record, top[-1]]
    elif top[2] < record:
        top[2] = record
    file = open("statistics.txt", mode="w")
    for elem in top:
        file.write(str(elem) + "\n")
    file.write(str(record))
    file.close()
