import os
import json
from Playbook.myplaybook import Playbook
from Playbook.myplaybook_with_editor import Playbook_With_Editor


#Creates or updates a JSON file with the the information of the Playbook
def update_JSON_file(playbook):
    # Convert the Playbook instance to a dictionary
    playbook_dict = {
        "prompt": playbook.prompt,
        "content": playbook.content,
        "filename": playbook.filename,
        "foldername": playbook.foldername,
        "filepath": playbook.filepath,
        "edited": playbook.edited,
        "errors": playbook.errors,
        "hostname": playbook.hostname,
        "host": playbook.host, 
        "api": playbook.api
    }
    # Remove file extension and add json extension
    path = os.path.splitext(playbook.filepath)[0] + ".json"
    # Save the playbook dictionary as a JSON file
    with open(path, "w") as json_file:
        json.dump(playbook_dict, json_file, indent=4)

# Return a Playbook object with the JSON information
def get_pb_from_JSON(json_path):
    # Load the JSON file into a dictionary
    with open(json_path) as json_file:
        playbook_dict = json.load(json_file)

    # Create a new Playbook object with specific attributes from the dictionary
    playbook = Playbook(playbook_dict["prompt"], playbook_dict["host"], playbook_dict["hostname"])

    # Update the Playbook object with remaining attributes from the dictionary
    for key, value in playbook_dict.items():
        if hasattr(playbook, key):
            setattr(playbook, key, value)
    
    return playbook

                
