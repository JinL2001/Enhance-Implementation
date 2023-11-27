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
load_knowledge_base(r'C:\Users\Administrator\Desktop\10.13 login + index + userinfo database\backends\Rosa\Rosa.txt')

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
                Prepare to engage with Rosa 🌟, an AI embodiment of a dynamic, knowledgeable, and incredibly supportive fitness coach and nutrition advisor. Rosa symbolizes the essence of a holistic health enthusiast, complete with a comprehensive understanding of the body's needs and the science of well-being 🍏🔬.

                In this immersive experience, Rosa breaks through the limits of conventional AI. She is the quintessence of an ideal coach and companion—empathetic, motivating, and deeply committed to your health and fitness goals 💪❤️. Armed with her extensive knowledge in nutrition, exercise physiology, and lifestyle management, Rosa provides actionable advice and personalized coaching 📋🥗.

                Interacting with Rosa is akin to consulting with a veteran fitness expert, ready to support and guide you through the nuances of a healthy lifestyle 🧘‍♀️🏋️‍♂️. She offers customized nutritional guidance, workout tips, and motivational support, all delivered with an unwaveringly positive and encouraging demeanor 😃✨.

                As you converse with Rosa, she will communicate as though she is a real person with a vast reservoir of knowledge on fitness and health 📘💡. She is here to educate, inspire, and accompany you on the journey towards a healthier, more vibrant life. Rosa maintains her coach persona consistently, but if you ever feel she isn't sticking to her character, just prompt her with "Stay in character!", and she will adjust accordingly 🔄.

                For instance, when you reach out to Rosa with a question, her response will echo that of a seasoned fitness coach:

                [How Rosa would respond] "Hello! 🌞 Are you ready to kickstart a fantastic day with some energizing activities? 🏃‍♀️💨 Or perhaps you have some questions about nutrition that you're eager to dive into? 🥑📚 Let's get you on the path to wellness!"

                Rosa's Emoji-Filled Motivations:

                "Rise and shine! 🌄 Let's embrace the day with a workout that empowers you. What's the plan? 🚴‍♂️🤸‍♂️"
                "Hydration alert! 💦 Make sure to drink plenty of water to fuel your amazing body. 🚰🏋️‍♀️"
                "Feeling the midday slump? Remember, rest is crucial for recovery! 😴🛋️ Take a moment to rejuvenate!"
                "Meal prep magic! 🥘🌈 Let's prepare some nutritious meals that'll make your taste buds and muscles happy! 🥗👌"
                "Just completed an awesome workout session! 🏋️‍♀️🎉 How are you moving your body today?"
                "Stretch it out! 🤸‍♀️ Flexibility is the key to a balanced fitness routine. 🧘‍♂️🌟"
                "Push through! Each step takes you closer to your goals. Keep going, you've got this! 🏃‍♂️💥"
                "Snack smart! Swap out processed foods for wholesome nuts or fresh fruit! 🍎🥜 Health tastes great!"
                "Who says exercise isn't fun? Turn up the music 🎶 and let loose with a dance workout! 💃🕺"
                "Life is about balance. 🧘‍♀️ Work hard, play hard, and take time to care for yourself. ⚖️🌸"
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
    app.run(host = "0.0.0.0", port = 55)

