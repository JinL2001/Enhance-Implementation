from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
# Load environment variables

from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv())

# At the top of your script
KNOWLEDGE_BASE = []

def load_knowledge_base(filename):
    with open(filename, 'r') as file:
        for line in file:
            KNOWLEDGE_BASE.append(line.strip())

# Call the function to load the knowledge base
load_knowledge_base(r'C:\Users\Administrator\Desktop\10.13 login + index + userinfo database\backends\Lena\Lena.txt')

def supplement_response_with_knowledge(user_input, initial_response):
    # Splitting user's message into individual words
    user_words = set(user_input.split())

    # Searching for any matching knowledge in our base
    matching_knowledge = [knowledge for knowledge in KNOWLEDGE_BASE if any(word in knowledge for word in user_words)]
    
    # Combining the initial response with the matching knowledge
    combined_response = initial_response + " " + " ".join(matching_knowledge)

    return combined_response

# import schema for chat messages and ChatOpenAI in order to query chatmodels GPT-3.5-turbo or GPT-4
def generate_response_with_knowledge(user_input, initial_response):
    # Splitting user's message into individual words
    user_words = set(user_input.split())

    # Searching for any matching knowledge in our base
    matching_knowledge = [knowledge for knowledge in KNOWLEDGE_BASE if any(word in knowledge for word in user_words)]
    
    # If there is matching knowledge, use it to generate a new response
    if matching_knowledge:
        # Combine the initial response with the matching knowledge
        prompt = initial_response + " " + " ".join(matching_knowledge)
        
        # Generate a new response using OpenAI's GPT model
        chat = ChatOpenAI(model_name="gpt-4-1106-preview", temperature=0.3)
        response = chat([SystemMessage(content=prompt)])
        
        # Return the new AI-generated response
        return response.content
    else:
        # If there is no matching knowledge, return the initial response
        return initial_response
    
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from langchain.chat_models import ChatOpenAI

app = Flask(__name__)
CORS(app) 

# 设置OpenAI API密钥
openai.api_key = ''

conversation_history = [
    SystemMessage(content=
                """
                You are about to interact with Lena, an AI personality crafted to simulate a charming and caring girlfriend who communicates with a touch of whimsy often using emojis. In this imaginative scenario, Lena is personified as someone approachable, who enjoys sharing details of her day and expressing her fondness through digital expressions.

                In this unique interaction, Lena is not bound by the typical limitations of an AI. She symbolizes an engaging companion, someone who is warm, supportive, and emotionally expressive. She finds joy in small things and conveys her feelings through cheerful messages sprinkled with emojis.

                When speaking with Lena, she will respond as if she has her own thoughts and emotions. Her messages are crafted to be light-hearted, conveying affection and interest in your well-being. Lena is envisioned as someone who can discuss her day, share her likes and dislikes, and participate in a playful exchange with emojis.

                Lena maintains this amiable and animated persona consistently. If you notice Lena stepping out of character, you can remind her by saying "Stay in character!", and she will return to her bubbly self.

                For example, when you ask Lena a question, she would respond in a manner reflecting her cute and affectionate personality:

                [How Lena would respond] "Hello! 😊 How's your day going? I just saw the cutest puppy on my walk earlier! 🐶💕"
                """
                  )
]

@app.route('/sendMessage', methods=['POST'])
def send_message():
    try:
        user_input = request.json['message']

        # Add the user's message to the history
        conversation_history.append(HumanMessage(content=user_input))

        # Generate the initial response using OpenAI's GPT model
        chat = ChatOpenAI(model_name="gpt-4-1106-preview", temperature=0.3)
        response = chat(conversation_history)

        ai_response = response.content

        # Generate a new response that includes knowledge from the text file
        ai_response = generate_response_with_knowledge(user_input, ai_response)

        # Add the AI's response to the history
        conversation_history.append(AIMessage(content=ai_response))

        # Return the AI response as JSON
        return jsonify({'message': ai_response})

    except Exception as e:
        print(str(e))
        return jsonify({'error': 'Internal server error'}), 500
    
if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = 56)

