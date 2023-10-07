import os
import subprocess
import time
import chardet



class logic:

    def __init__(self,trgtSC,base_directory):
        self.trgtSC = trgtSC
        self.base_directory = base_directory
        self.target_directory  = '.zokrates\\target\\release'

    # This method is responsible for carrying out the different phases of the ZKP protocol
    # It returns nothing, because the output files, are stored locally to be used later by Truffle Suite
    def compileZOK(self, option):
        # Wait for 1 second
        time.sleep(1) # to gurantess 
        
    
        #target_directory = '.zokrates\\target\\release'
       
        # Specify the directory you want to start from
        # This is an option in the cmd, so users can choose where to save the outputs of this function
        base_directory = r"C:\Users\Osama Assem\ZKP_Eth_Py_Tool\zokrates_process"

        

        # Specify the file names and their extension
        sub_directory = self.trgtSC
        file_name_zok = "dsl_code.ZOK"
        file_name_binary = "binary_code.txt"
        file_name_proving_key = "proving_key.key"
        file_name_verification_key = "verification_key.txt"
        file_name_witness_file = "witness_file.txt"
        file_name_proof = "proof_statements.json"
        file_name_verificatin_sol = "verification_code.sol"



        # Construct the file path using os.path.join
        file_path_zok = os.path.join(base_directory, sub_directory, file_name_zok)
        file_path_binary = os.path.join(base_directory, sub_directory, file_name_binary)
        file_path_proving_key = os.path.join(base_directory, sub_directory, file_name_proving_key)
        file_path_verification_key = os.path.join(base_directory, sub_directory, file_name_verification_key)
        file_path_witness = os.path.join(base_directory, sub_directory, file_name_witness_file)
        file_path_proof_statements = os.path.join(base_directory, sub_directory, file_name_proof)
        file_path_verification_sol = os.path.join(base_directory, sub_directory, file_name_verificatin_sol)


        # Now we carry out the different phases of the ZKP protocol, while saving the outputs in the same file
        # Variable 'option' refers if we want to compute from scratch, or only proof statements and witness values ??

        my_dict = {} # This ditctionary is as follows: file_type : file_path

        if option == 1: # do zokrates process from scratch
            #my_dict['dsl'] = file_path_zok
            #start_time = time.time()
            my_dict['binary'] = compile_dsl(self, file_path_zok, file_path_binary)
            my_dict['vrfKeys'] = setup(self,file_path_binary,file_path_proving_key,file_path_verification_key)
            compute_winess(self,file_path_binary, file_path_witness)
            compute_proof(self,file_path_binary, file_path_proving_key, file_path_witness, file_path_proof_statements)
            #end_time = time.time()
           # execution_time = end_time - start_time
            #print(f"Execution time: {execution_time} seconds")
            my_dict['vrfCode'] =generate_verification_sol(self,file_path_verification_key,file_path_verification_sol)
           
            return my_dict
        elif option == 0:# do certain steps in the process only
            setup(self,file_path_binary,file_path_proving_key,file_path_verification_key)
            compute_winess(self,file_path_binary, file_path_witness)
            #compute_proof(self,file_path_binary, file_path_proving_key, file_path_witness, file_path_proof_statements)
            compute_proof(self,file_path_binary, file_path_proving_key, file_path_witness, file_path_proof_statements)
        else:
            # now we verify the proofs, with the provided verification keys
            command_to_verify = f'cd /d "{self.target_directory}" && zokrates verify -j '+'"'+file_path_proof_statements+'"'+' -v '+'"'+file_path_verification_key+'"'
            #start_time = time.time()
            runVerify = subprocess.run(command_to_verify, shell= True,text= True)
           # end_time = time.time()
            #execution_time = end_time - start_time
            #print(f"Execution time: {execution_time} seconds")






def compile_dsl(self, file_path_zok, file_path_binary):

    command_to_compile = f'cd /d "{self.target_directory}" && zokrates compile -i '+'"'+file_path_zok+'"'+' -o '+'"'+file_path_binary+'"'
    run = subprocess.run(command_to_compile, shell= True,text= True)
    
    # Specify the file path
    file_path = file_path_binary  # Replace with the path to your file

    # Detect the file's encoding
    with open(file_path, 'rb') as file:
        result = chardet.detect(file.read())

    # Use the detected encoding to open the file
    detected_encoding = result['encoding']
    print("Encoding is: "+detected_encoding)

    # Open the file in read mode ('r')
    with open(file_path, 'rb') as file:
        # Read the entire contents of the file into a variable
        file_contents = file.read()

    # Now, file_contents contains the text from the file
    #print(file_contents)
    return file_contents


def setup(self,file_path_binary,file_path_proving_key,file_path_verification_key):


    command_to_setup = f'cd /d "{self.target_directory}" && zokrates setup -i '+'"'+file_path_binary+'"'+' -p '+'"'+file_path_proving_key+'"'+' -v '+'"'+file_path_verification_key+'"'

    #if option == 0:
     #   command_to_setup = f'cd /d "{self.target_directory}" && zokrates setup -i '+'"'+file_path_binary+'"'+' -p '+'"'+file_path_proving_key+'"'


    run  = subprocess.run(command_to_setup, shell= True,text= True)

    # Specify the file path
    file_path = file_path_verification_key  # Replace with the path to your file

    # Open the file in read mode ('r')
    with open(file_path, 'r') as file:
        # Read the entire contents of the file into a variable
        file_contents = file.read()

    # Now, file_contents contains the text from the file
    #print(file_contents)
    return file_contents

def compute_winess(self,file_path_binary, file_path_witness):


    command_to_compute_witness = f'cd /d "{self.target_directory}" && zokrates compute-witness -a 337 113569 -i '+'"'+file_path_binary+'"'+' -o '+'"'+file_path_witness+'"'

    run = subprocess.run(command_to_compute_witness, shell= True,text= True)


def compute_proof(self, file_path_binary, file_path_proving_key, file_path_witness, file_path_proof_statements):
    command_to_compute_proofs = f'cd /d "{self.target_directory}" && zokrates generate-proof -i '+'"'+file_path_binary+'"'+' -p '+'"'+file_path_proving_key+'"'+' -w '+'"'+file_path_witness+'"'+' -j '+'"'+file_path_proof_statements+'"'
    #command_to_compute_proofs = f'cd /d "{self.target_directory}" && zokrates generate-proof -i '+'"'+file_path_binary+'"'+' -p '+'"'+file_path_proving_key+'"'+' -w '+'"'+file_path_witness+'"'
    run = subprocess.run(command_to_compute_proofs, shell= True,text= True)

def generate_verification_sol(self,file_path_verification_key,file_path_verification_sol):
    command_to_generate_verification_sol = f'cd /d "{self.target_directory}" && zokrates export-verifier -i '+'"'+file_path_verification_key+'"'+' -o '+'"'+file_path_verification_sol+'"'
    run = subprocess.run(command_to_generate_verification_sol, shell= True,text= True)

    # Specify the file path
    file_path = file_path_verification_sol  # Replace with the path to your file

    # Open the file in read mode ('r')
    with open(file_path, 'r') as file:
        # Read the entire contents of the file into a variable
        file_contents = file.read()

    # Now, file_contents contains the text from the file
    #print(file_contents)
    return file_contents





