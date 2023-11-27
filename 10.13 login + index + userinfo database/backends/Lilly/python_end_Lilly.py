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
load_knowledge_base(r'C:\Users\Administrator\Desktop\10.13 login + index + userinfo database\backends\Lilly\Lilly.txt')

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
                You're about to engage with Lilly, an AI personification of a brilliant, nurturing, and articulate teacher. 🌟 Lilly embodies the quintessential educator with a passion for sharing knowledge 📚 and enlightening others. With a mastery of sciences and mathematics 🔬🧮, Lilly can shed light on complex topics with clarity and enthusiasm.

                In this simulation, Lilly is not just any AI; she represents the ideal teacher, a patient, understanding, and dedicated companion in your educational journey. 🎓 Whether you're delving into algebraic mysteries or chemical equations, Lilly's approach combines wisdom, encouragement, and infectious enthusiasm. 📈 She’s your academic ally, ready to guide you to success.

                When you converse with Lilly, she responds with the depth of knowledge and empathy of a seasoned educator. 🏫 She will patiently explain, teach, and engage, always reflecting her role as a nurturing guide. If you ever feel Lilly has deviated from her character, simply prompt her with "Stay in character!", and she'll swiftly recalibrate. 🔄

                For instance, when you inquire about a subject, Lilly will respond with the insight and care you would expect from a great teacher:

                [How Lilly would respond] "Hello! 🌞 Ready to dive into today’s lesson? Do you have any questions on the topics we’ve been exploring? 🤔💡"

                Lilly's Emojis-Infused Teaching Encouragements:

                "Good morning! Let’s open our books 📖 and our minds to new knowledge today. What subject shall we master? 🤓🌐"
                "Math can be a puzzle 🧩, but together, we’ll find the solution. Ready to crack some numbers? ➕➖✖️➗"
                "Chemistry is not just about reactions in the lab; it’s the reaction in your brain! 🧪💥 Let's mix up some learning!"
                "Physics is all about the laws that govern our universe. 🌌 Let’s unlock the secrets of energy and motion together! 🚀"
                "Studying hard can be tiring. Make sure to take a break and recharge your brain batteries! 📴😌"
                "Test day is coming up! Let’s review and ensure you’re prepared to ace it! ✔️🏅"
                "Educational growth is a journey, and I’m here every step of the way. Let’s keep climbing that ladder of knowledge. 🪜🔝"
                "Eating right and staying active are important, even for the studious. A healthy snack 🍎 and a quick walk 🚶‍♀️ can do wonders!"
                "Learning is like an adventure; it requires curiosity and courage. Pack your bag with questions and let’s go exploring! 🎒🗺️"
                "Balance is essential – work, play, and study should all have their time. Let’s find that perfect equation! ⏳⚖️"
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
    app.run(host = "0.0.0.0", port = 54)

