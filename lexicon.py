def read_list(file_path):
    with open(file_path) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    return content


WORDS = read_list("twl2016.txt")

if __name__ == "__main__":
    import random

    print(random.choice(WORDS))
