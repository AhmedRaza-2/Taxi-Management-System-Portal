import os
def loadData(file):
    data = []
    if os.path.exists(file):
        with open(file, "r") as f:
            data = [line.strip() for line in f.readlines()]
    return data
def saveData(file, data):
    with open(file, "w") as f:
        for line in data:
            f.write(line + "\n")
def appendData(file, line):
    with open(file, "a") as f:
        f.write(line + "\n")
