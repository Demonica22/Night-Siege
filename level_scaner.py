def scan_level(level_file_name):
    file = open(level_file_name + ".txt", encoding="utf-8").read().split("\n")
    file = list(map(list, file[:-1]))
    return len(file[0]), len(file), file
