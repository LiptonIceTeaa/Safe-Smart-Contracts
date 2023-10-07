import re
import openai
from flask import Flask, request, jsonify

# Set your OpenAI API key (replace with your actual key)
api_key = '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'
openai.api_key = api_key

# Open the file for reading
with open('prompt1.txt', 'r') as file:
    # Read the contents of the file into a string
    file_contents = file.read()

# Open the file for reading
with open('prompt2.txt', 'r') as file:
    # Read the contents of the file into a string
    file_contents2 = file.read()




app = Flask(__name__)

@app.route('/convert-solidity-to-zok', methods=['POST'])
def convert_solidity_to_zok():
    try:
        # Get the Solidity code from the request
        solidity_code = request.form['solidity_code']

        
        # Use OpenAI GPT-3.5 to generate ZoKrates DSL
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
            {"role": "system", "content": "You are performing code transformations."},
            #{"role": "user", "content": " Whats is ur aname"},
            {"role": "user", "content": " "+file_contents},
            ],
            temperature = 0
        )
        
        # Extract ZoKrates DSL from the model's response
        #zokrates_dsl = response.choices[0].text
        zokrates_dsl = response["choices"][0]["message"]["content"]
        # Use regular expression to extract code between triple backticks

        matches = re.findall(r'```(.*?)```', zokrates_dsl, re.DOTALL)
        

        # If there are matches, you can access the code between triple backticks
        if matches:
            zokrates_dsl = matches[0]

        # Now, zokrates_dsl contains the code between the triple backticks
        #print(zokrates_dsl)
        
        # Respond with the ZoKrates DSL code as JSON
        return jsonify({'zokrates_dsl': zokrates_dsl})
    except Exception as e:
        return jsonify({'error': str(e)})
    



@app.route('/getSoliditySummary', methods=['POST'])
def getSoliditySummary():
    try:
        # Get the Solidity code from the request
        solidity_code = request.form['solidity_code']

        
        # Use OpenAI GPT-3.5 to generate ZoKrates DSL
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
            {"role": "system", "content": "You are performing code transformations."},
            #{"role": "user", "content": " Whats is ur aname"},
            {"role": "user", "content": " "+file_contents2},
            ],
            temperature = 0
        )
        
        # Extract ZoKrates DSL from the model's response
        #zokrates_dsl = response.choices[0].text
        zokrates_dsl = response["choices"][0]["message"]["content"]
        # Use regular expression to extract code between triple backticks
        matches = re.findall(r'```(.*?)```', zokrates_dsl, re.DOTALL)

        # If there are matches, you can access the code between triple backticks
        if matches:
            zokrates_dsl = matches[0]

        # Now, zokrates_dsl contains the code between the triple backticks
        #print(zokrates_dsl)
        
        # Respond with the ZoKrates DSL code as JSON
        return jsonify({'zokrates_dsl': zokrates_dsl})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)