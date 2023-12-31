import datetime
import random
import time
import subprocess
import os
import re
from Openai.myopenai import *

class Playbook:
    prompt = None
    content = None
    filename = None
    foldername = None
    filepath = None
    edited = False
    errors = None 
    hostname = None
    host = None
    api = True 

    def __init__(self, prompt, host, hostname):
        
        self.prompt = prompt
        self.host = host
        self.hostname = hostname
        


    # Generate  a filename for the playbook (It doesn't include the extensions)
    def generate_filename(self): 
        # Generate a timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        # Generate a random integer between 0 and 9999
        random_num = random.randint(0, 9999)

        # Combine the timestamp and random integer to create a unique file name
        name = f"test_{timestamp}_{random_num}"

        # Generate filepath using the filename for the folder where the playbook'll be saved
        self.generate_filepath(name)

        # Save the filename including the extension
        self.filename = name + ".yml"

        print(self.filename) # Example output: test_20220329_112345_1234.txt

    def generate_filepath(self, fname):
        self.foldername = fname
        self.filepath =  "./playbooks/" +fname +"/"+ fname +".yml" 


    def set_content(self):

        dictionaryINS = {
           
            "1": " -Starting with --- \n", 
            "2": " -Playboook must ends with ... \n"
        }

        instructions = "It should be in the right format: \n"
        for key in dictionaryINS:
            instructions = instructions + dictionaryINS[key] 
        
        final_prompt = self.prompt + instructions

        self.content = ask_gpt(final_prompt)
        

     
    def create_folder(self):

        # Set the base directory for the file
        base_dir = "./playbooks/"
        os.makedirs(os.path.join(base_dir, self.foldername), exist_ok=True)



    def write_playbook(self):

        #Sanitises playbook before writing in file
        success = self.sanitize_playbook()
        if success == False: 
            exit(1)

        self.create_folder()

        # Open a new file for writing
        with open(self.filepath, "w") as file:
            # Write ansible playbook in a file
            file.write(self.content)

        #Esperamos a que escriba el fichero
        time.sleep(5)


    #Read playbook file and returns its value
    def read_playbook(self):
        
        with open(self.filepath, 'r') as f:
            file_text = f.read()
        return file_text
       
    def sanitize_playbook(self):

        print("Sanitising Ansible Playbook... ")
        # Verifica si el texto contiene --- y ...
        if '---' in self.content and '...' in self.content:    
            # Define el patrón de búsqueda utilizando expresiones regulares
            regex = r'---\n(.+?\n\.\.\.)'

            # Busca el texto que coincide con el patrón y lo imprime
            result = re.search(regex, self.content, re.DOTALL)

            if result:
                self.content = result.group(0)
                return True
            return False 
        else:
            print("Error: The playbook generated by GPT doesn't contain --- and ...")
            return False

                
    def simulate_playbook_execution(self):
      
        # Simulate the playbook execution using the ansible-playbook command with --check flag
        simulation_command = ["ansible-playbook", "--check", self.filepath]
        simulation_process = subprocess.run(simulation_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
        simulation_output = simulation_process.stdout + simulation_process.stderr
        
        if simulation_output:
            print("Simulation failed with the following output:\n{}".format(simulation_output))
            return False
        
        print("Simulation completed successfully. You can now execute the playbook.")
        return True

    def execute_playbook(self):
        
        #if not self.simulate_playbook_execution():
        #    return
        try:
          # Execute the playbook using the ansible-playbook command
            output = subprocess.check_output(["ansible-playbook", self.filepath], stderr=subprocess.STDOUT)

            return output.decode(), False
         
        except subprocess.CalledProcessError as e:
            # If there was an error executing the playbook, print the error message to the console and a boolean value
            return e.output.decode(), True
    
    #Edit playbook with a file editor
    def edit_playbook(self):
        try:
            # Use the nano text editor
            subprocess.run(["nano", self.filepath])
        except Exception as e:
            print(f"An error occurred while opening the file: {str(e)}")
    


