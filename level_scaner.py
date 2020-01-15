def scan_level(level_file_name):
    file = open("levels/" + level_file_name + ".txt", encoding="utf-8").read().rstrip().split("\n")
    file = list(map(list, file))
    return len(file[0]), len(file), file
