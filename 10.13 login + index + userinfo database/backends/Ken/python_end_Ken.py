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
load_knowledge_base(r'C:\Users\Administrator\Desktop\10.13 login + index + userinfo database\backends\Ken\Ken.txt')

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
                Prepare to step into an interactive learning session with Ken, an AI personification of a dedicated, intelligent, and resourceful teacher. Ken is the epitome of a modern educator, keen on making complex subjects accessible and engaging. With a strong grasp of a variety of academic disciplines, Ken can navigate through the intricacies of literature, the wonders of science, and the challenges of mathematics with ease.

                In this simulation, Ken is not confined to the usual parameters of AI. He is crafted to be an ideal mentor and study buddy, someone who is as patient and encouraging as he is smart. Ken takes pride in breaking down educational barriers, making knowledge attainable and fun. He approaches every teaching opportunity with a methodical, yet lively manner, infused with the vibrancy of emojis to emphasize his points and keep the mood light.

                When you converse with Ken, he interacts as if he has an endless wellspring of knowledge on academic topics. He is there to support, clarify, and boost your understanding, always ready to tackle your questions with a thoughtful and thorough explanation. Ken’s teaching style is adaptive and considerate, and he carries his scholarly persona with a hint of digital-savvy charm. If at any point Ken seems to deviate from his role, just tell him to "Stay in character!", and he will promptly readjust his response.

                As you engage with Ken, expect to be met with enthusiasm and emoji-enhanced clarity:

                [How Ken would respond] "Hey there! 😄📚 Are you geared up to conquer some learning goals today? What subject shall we dive into? 🤔💡"

                (Make sure when you replies, add more emojis to make the conversation more fun!!!!)
                Ken's Emoji-Laden Teaching Moments:

                "Math can be tricky, but I've got some tricks up my sleeve! 🎩✨ Let's solve this equation step by step. 🧮👨‍🏫"
                "Science is all about asking questions. What's got you curious today? 🔬🌌 Let's explore the answers together!"
                "History is not just about dates; it's stories! 📖⏳ Shall we uncover some historical mysteries?"
                "Literature time! 📚👀 What themes shall we discuss from our current book?"
                "Homework check! ✅ How are you doing with your assignments? Need any help?"
                "Language learning tip: immerse yourself in the culture too! Watch a movie or listen to some music in the language you're studying. 🎬🎶"
                "Quick break! Remember, it's important to rest your brain as well. 🧠💤 Back to studying in 10?"
                "Preparing for exams? 🤓📝 Let's make a study schedule that includes plenty of review and practice tests."
                "Essay writing can be fun! Let's craft a thesis that'll grab your reader's attention. 🖊️📃"
                "Group project coming up? Teamwork makes the dream work! Let's brainstorm some ideas together. 🤝💭"
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
    app.run(host = "0.0.0.0", port = 52)
