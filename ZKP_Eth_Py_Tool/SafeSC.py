import optparse
import subprocess
import threading
import psutil # used to measure the cpu usage
import cProfile # another library used to measure cpu usage
import platform


from mySQL_logic import MySQL_logic
from Etherscan import EtherRetreiver
from API_CLIENT import client
import os
from zokrates_logic import logic
from ftpClient_script import ftpClient
import time # for testing code effiency
import concurrent.futures




# takes arguments from terminal
# Responsible for taking the user input of target smart contract address, verifiying it, and returning the address to the main method    
def getArguments():
    parser = optparse.OptionParser("Usage of this tool is: -a <Smart Cotract Address>\nExample of usages:\n\t[+] python SafeSC.py -a 0x6e1BD5971d8C07Ac042bfe8d4ae60276C8777c92 \n\t")  # creating a parser
    # object

    # now we add options to our parser object (target address)
    parser.add_option("-a", "--target_address", dest='trgtSC', help="Address of smart contract you are trying to view.")
    #parser.add_option("-p", "--file_path", dest='fPath', help="Path of working directory where generated files are saved.")
    

    (options, arguments) = parser.parse_args()  # puts the user input into variables
    trgtSC = options.trgtSC
    if trgtSC == None or len(trgtSC) < 42 or len(trgtSC) > 42 or (not trgtSC.startswith("0x")):
        parser.error("[-] The address provided is not a valid smart contract address !")
        
    print("You have entered a valid address.")
    return options # include the target address



def main():
    #variable_to_increment = "0x6e1BD5971d8C07Ac042bfe8d4ae60276C8777c"
    global counter
    """
    with counter_lock:
        counter += 1
        current_counter = counter
    """

    #start_time = time.time()

    options = getArguments()  # gets the arguments from the command line (target address)
    trgtSC = options.trgtSC  # Target smart contract address

   # trgtSC = "0x6e1BD5971d8C07Ac042bfe8d4ae60276C8777c92"
    #trgtSC = variable_to_increment + str(current_counter)
  
    
    #db = MySQL_logic()# creating an instance of our online database to communicate with it
    # trgtSC = userInput()# taking user input

    vrfSCaddress = checkExistingSC(str(trgtSC))
    if vrfSCaddress:
        print("[+] This rgt smart has aloready been processed, and no need to generate another verification code and public keys")
        directory = trgtSC
        # Parent Directory path
        #parent_dir = pandas.read_csv(r"C:\Users\Osama Assem\ZKP_Eth_Py_Tool\zokrates_process")
        parent_dir = "C:\\Users\\Osama Assem\\ZKP_Eth_Py_Tool\\zokrates_process"
        # Path
        path = os.path.join(parent_dir, directory)
        # Check if the directory already exists, and if not, create it
        if not os.path.exists(path):
            os.mkdir(path)
            print(f"[+] Directory '{trgtSC}' created successfully.\n")


        retreiveFileFromDB(trgtSC) # this line downloads verification smart contract, verficiation keys, and the binary files into the host's machine
        # now we need to run zokrates but only some parts of it
        # run setup ( to get the proving keys)
        # run compute witness to generate witness file
        # run generate-proof to get p
        zokrates_processing(trgtSC,0) # this command will run on the needed parts of the process
        print("\n\t*****\t Verifying the proof, with the given verification keys \t*****\t\n")
        print("Result: ")
        zokrates_processing(trgtSC,2) #verify
        #end_time = time.time()
        ##execution_time = end_time - start_time
       # result = f"Processed request {current_counter} in {execution_time:.2f} seconds"
        #print(result)
        
    else:
        print("[+] New smart contract detected, we should call EtherScan")
        # now we retrieve the source code from Etherescan.io
        #srcCode = retrieveSrcCode(trgtSC)# this is how its supposed to be, but we follow the next line for simulation purposes
        srcCode = """"

        pragma solidity ^0.8.0;

contract Calculator {
   
    function add(uint256 a, uint256 b) public pure returns (uint256) {
        return a + b;
    }

    
    function main(uint256 a, uint256 b) public pure returns (uint256) {
        return add(a, b);
    }
}
        """
        if srcCode:
            print("Source code is found on Etherscan.io")
            # send this srcCode to chatgpt api
            # generate the DSL code
            dsl_code = getDSL(srcCode, trgtSC)
            breif_summary  = getBriefSummary()
            if dsl_code:
                print("[+] DSL code generated successfully.\n")
                directory = trgtSC
                # Parent Directory path
                #parent_dir = pandas.read_csv(r"C:\Users\Osama Assem\ZKP_Eth_Py_Tool\zokrates_process")
                parent_dir = "C:\\Users\\Osama Assem\\ZKP_Eth_Py_Tool\\zokrates_process"
                # Path
                path = os.path.join(parent_dir, directory)
                # Check if the directory already exists, and if not, create it
                if not os.path.exists(path):
                    os.mkdir(path)
                    print(f"[+] Directory '{trgtSC}' created successfully.\n")
                
                # Save DSL code to a file within the directory
                file_path = os.path.join(path, "dsl_code.ZOK")
                try:
                    with open(file_path, "w") as text_file:
                        text_file.write(dsl_code)
                        print("[+] DSL code written to file successfully.")
                except PermissionError:
                    print("Permission denied. You don't have the necessary permissions to write to the file.")
                except Exception as e:
                    print(f"An error occurred: {e}")

                # Save DSL code to a file within the directory
                file_path2 = os.path.join(path, "summary.txt")
                try:
                    with open(file_path2, "w") as text_file1:
                        text_file1.write(breif_summary)
                        print("[+] Summary written to file successfully.")
                except PermissionError:
                    print("Permission denied. You don't have the necessary permissions to write to the file.")
                except Exception as e:
                    print(f"An error occurred: {e}")
               

                # call ZoKrates to perform its processing
                ##zokrates_process = logic(trgtSC) # creating an instance of the zokrates class
                #zokrates_process.compileZOK()
                dict = zokrates_processing(trgtSC,1)
                

                """
                for key, value in dict.items():
                    print(f"{key}: {value}")
                    print("\n ***********************************")
                """

                saveFileIntoDB(trgtSC,dict['binary'],'binary')
                #saveFileIntoDB(trgtSC,dict['vrfKeys'],'vrfKeys')
                saveFileIntoDB(trgtSC,dict['vrfCode'],'vrfCode')
                saveFileIntoDB(trgtSC,breif_summary,'sum')

                create_new_entry(trgtSC)

                print("\n\t*****\t Verifying the proof, with the given verification keys \t*****\t\n")
                print("Result: ")
                zokrates_processing(trgtSC,2) #verify
                #end_time = time.time()
                #execution_time = end_time - start_time
                #result = f"Processed request {current_counter} in {execution_time:.2f} seconds"
                #print(result)


                

            else:
                print("[-] DSL code generation failed")
            
        else:
            print("No source code found. \nPlease request the original creator(s) to verify them on Etherscan.io")
            exit()
        

# Responsible for looking in our DB for an existing entry with the value of the provided SC address.
# If found, the address is returned to main method
# If not found, Null is returned to main method
def checkExistingSC(trgtSC):
    print("\n\t*****\t Checking if the provided smart contract exists in our db \t*****\t\n")
    db = MySQL_logic()# creating an instance of our online database to communicate with it
    result = db.checkForTrgtSC(trgtSC)
    
    return result
    
    

def retrieveSrcCode(trgtSC):
    print("\n\t*****\t Retrieving Source code from Ethereum \t*****\t\n")

    etherO = EtherRetreiver()
    sourceCode = etherO.retrieveSrcCode(str(trgtSC))

    return sourceCode
    

def getDSL(srcCode, trgtAddress):
    print("\n\t*****\t Generating and retreiving corresponding DSL ZoKrates code \t*****\t\n")

    client_api = client(srcCode, trgtAddress)
    dsl_code = client_api.convert()
    
    return dsl_code

def zokrates_processing(trgtSC,option):
    zokrates_process = logic(trgtSC,"d") # creating an instance of the zokrates class
    result = zokrates_process.compileZOK(option)
    return result

def create_new_entry(trgtSC_address):
    print("\n\t*****\t Adding a new entry to the table ! \t*****\t\n")
    db = MySQL_logic()# creating an instance of our online database to communicate with it
    result = db.addSC(trgtSC_address)
    print("\n\t*****\t"+result+"\t*****\t\n")


def saveFileIntoDB(trgtSC,data,fileType):
    ftpClientO = ftpClient()
    #print("DATA TO BE SAVED IS: "+data)

    ftpClientO.uploadFile(trgtSC,data,fileType)

def retreiveFileFromDB(trgtSC):
    ftpClientO = ftpClient()
    ftpClientO.downloadFile(trgtSC,'binary')
    ftpClientO.downloadFile(trgtSC,'vrfCode')
   # ftpClientO.downloadFile(trgtSC,'vrfKeys')
    ftpClientO.downloadFile(trgtSC,'sum')

def getBriefSummary():
    client_api = client("srcCode", "trgtAddress")
    summary = client_api.briefSummary()
    # Insert a newline after every period (".")
    summary = summary.replace(".", ".\n")
    
    
   
    
    return summary

    



if __name__ == '__main__':
    #start_time = time.time()
    
   main()
   

   # end_time = time.time()
   # execution_time = end_time - start_time
   # print(f"Execution time: {execution_time} seconds")

   # counter_lock = threading.Lock()
   # counter = 10

    #max_threads = 50
    #with concurrent.futures.ThreadPoolExecutor(max_threads) as executor:
    #  [executor.submit(main) for i in range(30)]