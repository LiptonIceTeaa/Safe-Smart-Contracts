import requests

class client:

    def __init__(self, srcCode, trgtAddress):

        # Define the API endpoint (replace with the actual URL if hosted irl remotely on an external server)
        self.api_url1 = 'http://127.0.0.1:5000/convert-solidity-to-zok'
        self.api_url2 = 'http://127.0.0.1:5000/getSoliditySummary'
        self.srcCode = srcCode
        self.trgtAddress = trgtAddress

 

    # This function is responsible for calling the server side (SafeSC off-chain solution) ChatGPT API script.
    # It send the source coude of the smart contract requested.
    # It returns the generated ZoKrates DSL code
    def convert(self):
        try:
            # Send a POST request to the API
            response = requests.post(self.api_url1, data={'solidity_code': self.srcCode})

            # Check if the request was successful
            if response.status_code == 200:
                # Extract the ZoKrates DSL code from the response
                zokrates_dsl = response.json()['zokrates_dsl']
                
                # Save the ZoKrates DSL code to a .zok file
                # here we can rename the .zok file to have the address of smart contract
                #with open('output_'+self.trgtAddress+'.zok', 'w') as zok_file:
                   # zok_file.write(zokrates_dsl)
                #print('ZoKrates DSL code was generated and saved into saved to output.zok')
                return zokrates_dsl
            else:
                print(f'[-] API request failed with status code: {response.status_code}')
                return None
        except Exception as e:
            print(f'[-] An error occurred: {str(e)}')
            return None
    
    def briefSummary(self):
        try:
            # Send a POST request to the API
            response = requests.post(self.api_url2, data={'solidity_code': self.srcCode})

            # Check if the request was successful
            if response.status_code == 200:
                # Extract the ZoKrates DSL code from the response
                summary = response.json()['zokrates_dsl']
                
                return summary
            else:
                print(f'[-] Brief summary API request failed with status code: {response.status_code}')
                return None
        except Exception as e:
            print(f'[-] An error occurred: {str(e)}')
            return None