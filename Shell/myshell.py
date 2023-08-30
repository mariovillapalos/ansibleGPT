import os
import signal
from Playbook.myplaybook import *
from Playbook.myplaybook_with_editor import *
from Utils.terminalColors import *
from Utils.json_handler import *

# Capture "Ctrl+C" to prevent it from displaying faults
def signal_handler(sig, frame):
    print("\n\nGoodbye :)")
    exit(0)

signal.signal(signal.SIGINT, signal_handler)


def menuMain():
    os.system('clear')
      
    while True:
        os.system('clear')
      

        print(prCyan("Choose a method: "))
        print(prGreen("[1] Create a playbook"))
        print(prGreen("[2] Edit a playbook"))
        print(prGreen("[3] Execute a playbook"))
        print(prGreen("[4] Simulate playbook execution"))
        print(prRed("[n] Exit/Quit"))

 

        option = input(prCyan("What would you like to do? Answer: ")) 
        
        if option =="1":
            menuCreate()
                   
        elif option == "2":
            menuEdit()

        elif option == "3":
            menuExecute()

        elif option == "4":
            menuSimulateExecution()

        elif option== "n":
            print("\nGoodbye :)") 
            exit()

        else:
            print("\n Not a valid choice! Pleasem try again. You only must enter the number of that method.")

def menuCreate():

    goback = False

    while goback == False:

        os.system("clear")

        print(prGreen("[1] Create a playbook with OpenAI API"))
        print(prGreen("[2] Create a playbook by YOURSELF"))
        print(prGreen("[3] Return to main menu"))

        suboption = input(prCyan("How do you want to create the playbook? Answer: "))

        if suboption == "1":

            print(" create playbook Chat GPT")
            create("1")
            input(prYellow("Press Enter to continue"))

        elif suboption == "2":

            print(" create playbook yourself")
            create("2")
            input(prYellow("Press Enter to continue"))

        elif suboption == "3":

            goback = True

        else:
            print(prYellow("\nNot a valid choice! Please try again. You only must enter the number of that method."))
            input(prYellow("Press Enter to continue"))
            #break

def create(method):
    stop = False
    while stop == False:
        #os.system('clear')
      
               
        # The host managed (OS)g 
        host = input(prYellow("For which host is applied the playbook? Answer: "))
        #The hostname in the Ansible Playbook
        hostname = input(prYellow("Which is the hostname of that host? Answer: "))

        #Creates playbook using chat GPT API
        if method == "1":
            
            # The prompt used to ask chat GPT
            prompt = input(prYellow("Type a prompt in order to get the playbook created by GPT API: ") ) 
            
            #Creates the Playbook object
            playbook = Playbook(prompt, host, hostname)

            # Generates a filename for the playbook
            playbook.generate_filename()


            playbook.set_content()
            playbook.write_playbook()

            #Creates a JSON file with the Playbook attributes
            update_JSON_file(playbook)
            print(playbook.content)

        #Creates playbook using text Editor
        else:
            playbook = Playbook_With_Editor(host, hostname)

            # Generates a filename for the playbook
            playbook.generate_filename()

            #Creates a Playbook using a file editor
            playbook.write_playbook()

            #Updates playbook content with the playbook file
            playbook.content = playbook.read_playbook()

            #Creates a JSON file with the Playbook attributes
            update_JSON_file(playbook)
        stop = True
           
# find a playbook by its filename
def find_playbook(filename):
    
    # Añade la extensión .yml si el usuario no la ha incluido
    if not filename.endswith('.yml'):
        filename += '.yml'

    # Define el directorio base en el que se buscará el archivo
    base_directory = "./playbooks/"

    # Define el subdirectorio donde se buscará el archivo
    subdirectory = filename.replace(".yml","")

    # Crea la ruta completa al archivo
    filepath = os.path.join(base_directory, subdirectory, filename)

    # Comprueba si el archivo existe
    if os.path.isfile(filepath):
        print(f"El archivo {filepath} existe.")
        json_path = "./playbooks/"  + subdirectory + "/" + subdirectory +".json"
        playbook = get_pb_from_JSON(json_path)  # Asume que get_pb_from_JSON() es una función que recupera un playbook como objeto.
        return True, playbook
    else:
        print(f"El archivo {filepath} no existe.")
        return False, None

#List all plaubooks which are in /Playbooks folder
def list_playbooks():
    # Define the path of the playbooks directory
    directory = "./playbooks/"
    
    # Use os.listdir to get a list of all files/directories stored in the playbooks directory.
    files = os.listdir(directory)

    # Create a dictionary with numbers as keys and file names as values
    playbook_filenames = {i+1: filename for i, filename in enumerate(files)}
    
    return playbook_filenames

def select_playbook():
    while True:
        # Get the playbook filenames
        playbook_dict = list_playbooks()

        # Iterate over the dictionary and print key-value pairs
        for key, value in playbook_dict.items():
            print(f'[{key}] {value}')
        print("[n] Return to previous menu")
        answer = input(prLightGray("Type the filename of the playbook. Answer: "))
        
        # Check if the selected_playbook is a valid key in the playbook_dict
        if answer.isdigit() and int(answer) in playbook_dict.keys():
            # If the key is valid, assign the value associated with that key
            selected_playbook = playbook_dict[int(answer)]
            found, playbook = find_playbook(selected_playbook)
            
            if found == True:
                return True, playbook
            
        elif answer.lower() == 'n':
            break
        else:
            input("Invalid selection. Please enter a valid number. Press Enter to try again.")

    return False, None

def menuEdit():
    
    goback = False
    while goback == False:
        
        os.system("clear")
        print(prGreen("[1] Select a playbook"))
        print(prGreen("[2] Return to main menu"))
        
        suboption = input(prCyan("Select one of the options above: "))
        
        if suboption == "1":
            
            found, playbook = select_playbook()
            
            if found == True:
                playbook.edit_playbook()
                input(prYellow("Press Enter to continue"))

        
        elif suboption == "2":
            goback = True
        else:
            print(prYellow("\nNot a valid choice! Please try again. You only must enter the number of that method."))
            input(prYellow("Press Enter to continue"))
            #break


def menuExecute():
    
    goback = False
    while goback == False:
        
        os.system("clear")
        print(prGreen("[1] Select a playbook"))
        print(prGreen("[2] Return to main menu"))
        
        suboption = input(prCyan("Select one of the options above: "))
        
        if suboption == "1":

            found, playbook = select_playbook()
            
            if found == True:
                output, error = playbook.execute_playbook()
                if error == False:
                    print("Playbook SUCCESFULLY executed \n")
                    print(output)
                else:
                    print("ERROR: Execution has failed")
                    print(output)

            input(prYellow("Press Enter to continue"))

        
        elif suboption == "2":
            goback = True
        else:
            print(prYellow("\nNot a valid choice! Please try again. You only must enter the number of that method."))
            input(prYellow("Press Enter to continue"))
            #break


def menuSimulateExecution():
    
    goback = False
    while goback == False:
        
        os.system("clear")
        print(prGreen("[1] Select a playbook"))
        print(prGreen("[2] Return to main menu"))
        
        suboption = input(prCyan("Select one of the options above: "))
        
        if suboption == "1":
            
            found, playbook = select_playbook()
            
            if found == True:
                playbook.simulate_playbook_execution()
                input(prYellow("Press Enter to continue"))

        
        elif suboption == "2":
            goback = True
        else:
            print(prYellow("\nNot a valid choice! Please try again. You only must enter the number of that method."))
            input(prYellow("Press Enter to continue"))
            #break




if __name__ == '__main__':
    menuMain()


