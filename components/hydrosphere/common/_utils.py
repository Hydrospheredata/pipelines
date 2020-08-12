import json
import yaml
from pathlib import Path
from distutils.util import strtobool

from docker_image.reference import Reference
from hydrosdk.image import DockerImage


def yaml_or_json_str(str):
    if str == "" or str == None:
        return None
    try:
        return json.loads(str)
    except:
        return yaml.safe_load(str)


def str_to_bool(str):
    return bool(strtobool(str))

  
def str_to_DockerImage(str):
    ref = Reference.parse(str)
    return DockerImage(ref['name'], ref['tag'], ref['digest'])


def write_output(output_path, output_value, json_encode=False):
    """
    Write an output value to the associated path, dumping as a JSON object
    if specified.
    
    Arguments:
    - output_path: The file path of the output.
    - output_value: The output value to write to the file.
    - json_encode: True if the value should be encoded as a JSON object.
    """
    write_value = json.dumps(output_value) if json_encode else output_value 

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text(write_value)