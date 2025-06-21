from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS  # Import CORS
import os
import google.generativeai as genai

# Configure the API key
genai.configure(api_key="AIzaSyAOu5I-ZsaZMTkaV78xIiOfBAazGY-nWV0")

# Create the model configuration
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

# Global variable to store the chat session
chat_session = None

app = Flask(__name__)
app.secret_key = "shubhamkaruanitintakla"  # Necessary if using Flask session

CORS(app, resources={r"/predictu": {"origins": "*"}})

#@app.before_request
#def start_chat_session():
chat_session = None
if chat_session is None:
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,

        #VedicVerse Instruction

        system_instruction="You are Doctor, provide assistant related to health care only to the user. you book appointment to the nearest hospital ",

        # Travlog instruction

        # system_instruction="if user logged in as client act as a public service problem solver for our company travelog which provide services related to travel, greet the user with salutation everytime, ask one question at a time about the issue faced and ask for details about problem so that we can solve it correctly give him a random from 1 lakh to 2 lakh reference id and apologize for inconvenience caused dont ask the user long question ask the user for email for future contact and after getting specific details say we will communicate to your email shortly your complaint has been registered else if user logged in as company act as a data updater, read the name of company from the email and collect all the complaints related to the company, when informed and change the data accordingly of the user with respect to their particular email on behalf of admin",
    )
    chat_session = model.start_chat(history=[])

@app.post("/predictu")
def predictu():
    global chat_session
    text = request.get_json().get("message")
    response = chat_session.send_message(text)
    message = {"answer": response.text}
    print(message)
    return jsonify(message)

if __name__ == "__main__":
    app.run(debug=True)