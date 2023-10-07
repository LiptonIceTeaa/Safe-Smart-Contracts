Safe Smart Contracts (SafeSC)


SafeSC is a  solution that implements privacy while adhering to Ethereum's transparency principle. 
The SafeSC Python tool and off-chain solution simplify implementation and testing, allowing users to understand and verify smart contracts using zk-SNARKs without accessing the source code.

Purpose
SafeSC provides a streamlined approach to smart contract verification, enabling users to comprehend and validate a contract's integrity. 
By displaying function signatures and a concise description, SafeSC empowers users to grasp the essence of a smart contract without compromising privacy or security.

How to Run
To run SafeSC, follow these steps:

Download and Install ZoKrates:
Ensure you have ZoKrates installed on your system. ZoKrates is required for running zk-SNARKs circuits.
Installation instructions can be found at ZoKrates GitHub Repository.

Access SafeSC Through CMD:
Open Command Prompt or Terminal and navigate to the project directory.

Run SafeSC:
Use the following command to verify a smart contract:

                "python SafeSC.py -a <smart_contract_address>"
                
Replace <smart_contract_address> with the Ethereum address of the smart contract you want to verify.

Input
SafeSC takes a smart contract address as input, which is typically found on the Ethereum blockchain.

Outputs
SafeSC provides the following outputs:

Verification Result:
Displays the verification result, indicating whether the smart contract is valid or not.

Local Files:
Several files are saved locally, including a summary file that provides a brief overview of the verified smart contract.

External Software Requirement
SafeSC relies on ZoKrates for zk-SNARKs computations. Ensure ZoKrates is installed on your system before running SafeSC. ZoKrates can be installed from the official ZoKrates GitHub Repository.

Limitations
Hard-Coded File Paths:
Please note that this tool contains hard-coded file paths, which can be customized according to a specific user's system configuration.
SafeSC is a research tool developed for a thesis project, aiming to enhance smart contract verification while preserving user privacy and security.
