import yaml

def initialize():
    global config
    with open(".\storage\config.yml", "r", encoding="utf-8") as stream:
        config = yaml.load(stream, Loader = yaml.FullLoader)