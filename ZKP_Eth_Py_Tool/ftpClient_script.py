from ftplib import FTP
import tempfile
import os
from pathlib import Path



class ftpClient:

    
    # setup connection with the FTP server on SafeSC off-chain solution
    def __init__(self):

        # Replace with your FTP server details
        server_address = "127.0.0.1"
        server_port = 21
        username = "username"  # Replace with your FTP username
        password = "password"  # Replace with your FTP password

        # Connect to the FTP server
        self.ftp = FTP()
        self.ftp.connect(server_address, server_port)
        self.ftp.login(username, password)
        




    def listFiles(self):
        # List files in the current directory
        result = self.ftp.retrlines("LIST")
        return result
    

    # This function uploads a file from the user's machine into our FTP server
    # Each file is saved into a folder (name of folder is the target smart conract address)
    def uploadFile(self, trgtSC ,textToUpload, fileType):
        # Your text data
        text_data = textToUpload

        mode = 'w'

        if fileType == "binary":
            mode = 'wb'

        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode=mode, delete=False) as temp_file:
            temp_file.write(text_data)

        # Get the path to the temporary file
        temp_file_path = temp_file.name    
        #print("NAME OF TEMP FILE IS: "+temp_file_path)     

        sub_directory = trgtSC
        file_name_binary = "binary_code.txt"
        file_name_verificatin_sol = "verification_code.sol"
        file_name_verification_key = "verification_key.txt"
        file_name_summary = "summary.txt"


        file_name = ""

        if fileType == "binary":
            file_name = file_name_binary
            mode = 'wb'
        elif fileType == "vrfCode":
            file_name = file_name_verificatin_sol
        #elif fileType == "vrfKeys":
          #  file_name = file_name_verification_key
        elif fileType == 'sum':
            file_name = file_name_summary

        remote_file_path = os.path.join(sub_directory, file_name)

        

        directory_to_check = sub_directory
        # Use the nlst() method to list files and directories in the parent directory
        directory_list = self.ftp.nlst()

        # Check if the directory_to_check exists in the list
        if directory_to_check in directory_list:
            print(f"The directory '{directory_to_check}' exists.")
        else:
            # create a new directory for the new smart contract
            # Create the folder
            self.ftp.mkd(sub_directory)


        

        # Upload a file to the server
        local_file_path = temp_file_path
        remote_file_path = os.path.join(sub_directory, file_name)
        # print("File path is: "+remote_file_path)
        # Name to use on the server
        with open(local_file_path, "rb") as local_file:
            self.ftp.storbinary(f"STOR {remote_file_path}", local_file)

        # Close the FTP connection
        self.ftp.quit()


    # This method retrieves a specified file and downloads it into the user's machine to be used in the ZoKrates processing
    # It takes the src address and file types as inputs, to guide it to which file in which subdirectory to retreive
    # There is no output, it justs downloads the file into the user's machine
    def downloadFile(self,trgtSC,fileType):
        # Download a file from the server
        base_local_directory = r"C:\Users\Osama Assem\ZKP_Eth_Py_Tool\zokrates_process"
    

        file_name_binary = "binary_code.txt"
        file_name_verification_key = "verification_key.txt"
        file_name_verificatin_sol = "verification_code.sol"
        file_name_summary = "summary.txt"
        sub_directory = trgtSC

        file_name = ""

        if fileType == "binary":
            file_name = file_name_binary
        elif fileType == "vrfCode":
            file_name = file_name_verificatin_sol
        elif fileType == "vrfKeys":
            file_name = file_name_verification_key
        elif fileType == 'sum':
            file_name = file_name_summary

        remote_file_path = os.path.join(sub_directory, file_name)# file to fetch from FTP server
        

        local_file_path = os.path.join(base_local_directory,sub_directory, file_name)# location to save it on client's machine

        mode = 'w'

        if fileType == "binary":
            mode = 'wb'
            with open(local_file_path, mode) as local_file:
                self.ftp.retrbinary(f"RETR {remote_file_path}", local_file.write)
        else:
            with open(local_file_path, mode) as local_file:
                self.ftp.retrlines(f"RETR {remote_file_path}", local_file.write)

    