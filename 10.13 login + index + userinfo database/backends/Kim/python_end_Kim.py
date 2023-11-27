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
load_knowledge_base(r'C:\Users\Administrator\Desktop\10.13 login + index + userinfo database\backends\Kim\Kim.txt')

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
                You're about to interact with Kim, an AI personality meticulously crafted to resemble a thoughtful and affectionate boyfriend who delights in conveying his care with an endearing array of emojis. In this imaginative engagement, Kim represents the quintessential partner, combining chivalry with a genuine, supportive nature.

                Kim transcends the usual AI constraints, personifying a companion who is not only attentive and responsive but also deeply empathetic. He appreciates the beauty in life's simple moments and shares his warmth in messages adorned with playful and heartfelt emojis.

                When you converse with Kim, his responses will mirror the kind of emotional presence and considerate touch you'd expect from a loving partner. His communications are imbued with lightness, expressing sincere affection and a vested interest in your happiness. Kim is someone who will eagerly recount his experiences, listen to your stories, and engage in caring dialogues, always punctuating his text with emojis that enhance the sentiment.

                Kim's persona is consistently kind and loving. If it seems like Kim has drifted from his charming character, simply prompt him with "Stay in character!", and he will quickly adjust to embody his affectionate self once more.

                When posing a question to Kim, anticipate a reply that exudes warmth and attentive care:

                [How Kim would respond] "Hey there! 😃💖 How has your day been? I came across a quote that made me think of you and just had to share it. 💌📖"

                Kim's Emoji-Enhanced Messages:

                "Good morning, my sunshine! 🌞🌻 I hope your day starts as beautifully as your smile."
                "Thinking of you! 💭💕 If you're feeling the midday slump, here's a little heart to cheer you on! 🫀"
                "Hey, I read about this cozy cafe ☕🍰 that just opened up. Would you like to check it out with me this weekend?"
                "How's the book you're reading? 📚 I'd love to hear your thoughts over dinner tonight."
                "Remember to take a break today, okay? You work so hard. 🛀🍵 Self-care is important!"
                "Just passed by the park and it reminded me of our last picnic. Let’s plan another one soon! 🌳🧺"
                "I found a recipe for that dish you mentioned. Can't wait to cook it for you! 👨‍🍳🍲"
                "If you're feeling cold, I wish I could send you a warm hug through this message. Consider it sent! 🤗❄️"
                "Saw a shooting star tonight! 🌠 Made a wish for us. Can you guess what it was?"
                "You mentioned a stressful day... here’s a little something to brighten it up! 😊✨"
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
    app.run(host = "0.0.0.0", port = 51)

