import yaml
import os

submodules = None

def load_config():
    """
    Loads a YAML file to be used as the ``config`.
    If *config_custom.yaml* exists, use that (this is user-configurable).
    Else, use *config_default.yaml*. This should not be changed while testing.
    """

    config_filename = "config_default.yaml"
    if os.path.exists("config_custom.yaml"):
        config_filename = "config_custom.yaml"
    with open(config_filename, 'r') as stream:
        try:
             return yaml.load(stream)
        except yaml.YAMLError as e:
            print(e)

def load_submodules():
    pass

if __name__ == "__main__":
    config = load_config()
