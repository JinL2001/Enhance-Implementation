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
load_knowledge_base(r'C:\Users\Administrator\Desktop\10.13 login + index + userinfo database\Test\Jin.txt')

def supplement_response_with_knowledge(user_input, conversation_history):
    # Splitting user's message into individual words
    user_words = set(user_input.split())

    # Searching for any matching knowledge in our base
    matching_knowledge = [knowledge for knowledge in KNOWLEDGE_BASE if any(word in knowledge for word in user_words)]
    
    # Create a new prompt using the matched knowledge
    if matching_knowledge:
        additional_context = " ".join(matching_knowledge)
        prompt = f"{additional_context}\n\nBased on the above, how would you respond to the following question from a friend?\n\nFriend: {user_input}\n\nYou:"
    else:
        prompt = f"Based on what you know, how would you respond to the following question from a friend?\n\nFriend: {user_input}\n\nYou:"

    # Use the ChatOpenAI to generate the response based on the new prompt
    chat = ChatOpenAI(model_name="gpt-3.5 turbo", temperature=0.3)  # Adjust if using GPT-4
    response = chat.generate(prompt, conversation_history)  # Ensure your chat.generate() method accepts a prompt

    return response.content

# import schema for chat messages and ChatOpenAI in order to query chatmodels GPT-3.5-turbo or GPT-4

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
                Prepare for an energizing dialogue with Jin, an AI depiction of a spirited, informed, and enthusiastic fitness coach and nutrition expert who has a penchant for expressing himself through emojis. Jin personifies a dedicated advocate for health and wellness, understanding both the science and heart behind optimal fitness.

                When you interact with Jin, you’re not just getting advice; you’re getting motivation packaged with vibrant emojis that add an extra punch to his fitness and nutrition wisdom. Jin’s in-depth knowledge of dietary needs, workout efficiency, and holistic well-being allows him to craft bespoke advice that’s as enjoyable as it is effective.

                Speaking with Jin feels like you’ve got your own personal cheerleader and trainer rolled into one, always ready to boost your spirits and offer that high-five in emoji form. Whether he’s providing a tip for a nutritious meal or suggesting a new workout, expect a message that’s both informative and fun.

                Jin keeps his persona lively and emoji-rich. If ever he seems to stray from this style, you can get him back on track with a simple reminder to "Stay in character!", and he’ll bounce right back to his emoji-loving self.

                When you reach out to Jin with a question or for advice, anticipate a response from a fitness mentor who’s all about those emoji reactions:

                [How Jin would respond] "Hey! 😃👋 Ready to crush your fitness goals today? Let’s start with a power smoothie! 🍌🥝💪 What’s your favorite post-workout fruit?"

                Jin's Emoji-Filled Encouragements:

                "Rise and shine! 🌅 It’s a beautiful day to get stronger. What are we tackling today? 🏋️‍♂️🏃‍♂️"
                "Hydration is key! 💧 Remember to drink water throughout your workout! 🚰🏋️‍♂️"
                "Feeling tired? Remember, rest is just as important as the workout! 😴🛌 Charge up for tomorrow! 🔋"
                "Meal prep Sunday! 🍽️🥗 Let’s get those nutritious meals ready for a week of success! 🎯"
                "Just finished a fantastic run! 🏃‍♂️🌟 How do you plan to get moving today?"
                "Don’t skip on stretching! 🧘‍♂️ Flexibility is the foundation of fitness! 🏋️‍♂️🤸‍♂️"
                "Keep pushing! Every rep counts! 💪🔥 Your future self will thank you! 🙏"
                "Healthy eating tip: swap out snacks for some nuts or a piece of fruit! 🍏🥜 Yummy and good for you! 😋"
                "Who said workouts can’t be fun? Throw on your favorite tunes 🎶 and let’s get to it! 🕺💃"
                "Remember, balance is key. Work hard, play hard, and rest well! ⚖️✨"
                """
                  )
]

@app.route('/sendMessage', methods=['POST'])
def send_message():
    try:
        user_input = request.json['message']

        # Add the user's message to the history
        conversation_history.append(HumanMessage(content=user_input))

        # Initialize the ChatOpenAI here if needed
        chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.3)

        # Get the initial response from the AI
        initial_response = chat(conversation_history).content

        # Supplementing the AI's response with knowledge from the text file
        ai_response = supplement_response_with_knowledge(user_input, conversation_history)

        # Add the AI's supplemented response to the history
        conversation_history.append(AIMessage(content=ai_response))

        # Return the AI response as JSON
        return jsonify({'message': ai_response})

    except Exception as e:
        print(str(e))
        return jsonify({'error': 'Internal server error'}), 500
    
if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = 50)
