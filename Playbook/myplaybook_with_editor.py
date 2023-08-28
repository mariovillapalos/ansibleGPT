
from Playbook.myplaybook import Playbook
import os
import time
class Playbook_With_Editor(Playbook):
    api = False

    def __init__(self, host, hostname):
        
        self.host = host
        self.hostname = hostname
        

    def write_playbook(self):
        
        self.create_folder()
        # Open a new file for writing
        file = open(self.filepath, "w") 
        file.close()

        #Esperamos a que escriba el fichero
        time.sleep(5)
        
        #Open the file with vim
        os.system(f'sudo nano {self.filepath}')

