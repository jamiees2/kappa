import yaml


def load(src):
    data = ""
    with open(src, 'r', encoding='utf-8') as f:
        data = f.read()
    return yaml.load(data)


def dump(data):
    return yaml.dump(data)
