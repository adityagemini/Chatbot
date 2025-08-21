import os
import random
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Pre-created small talk responses
RESPONSES = {
    "greetings": [
        "Hello! How are you doing today?",
        "Hi there! Nice to meet you!",
        "Hey! What's up?",
        "Greetings! How can I help you today?",
        "Hello! Hope you're having a great day!"
    ],
    "how_are_you": [
        "I'm doing great, thank you for asking!",
        "I'm fantastic! How about you?",
        "I'm doing well, thanks! What about yourself?",
        "All good here! How are things with you?",
        "I'm wonderful! Thanks for asking!"
    ],
    "weather": [
        "I don't have access to current weather data, but I hope it's nice where you are!",
        "Weather can be so unpredictable! What's it like outside for you?",
        "I wish I could check the weather for you, but I hope it's pleasant!",
        "Is the weather nice where you are today?"
    ],
    "hobbies": [
        "I love chatting with people! What hobbies do you enjoy?",
        "That's interesting! I enjoy learning about different topics. What about you?",
        "Hobbies are great! I'm curious about what you like to do in your free time.",
        "Tell me more about your interests!"
    ],
    "default": [
        "That's interesting! Tell me more.",
        "I see! What else would you like to talk about?",
        "Hmm, that's a good point. What do you think about that?",
        "Interesting perspective! Can you elaborate?",
        "I'd love to hear more about that!",
        "That sounds fascinating! What's your take on it?",
        "Cool! What made you think of that?",
        "I appreciate you sharing that with me!",
        "That's worth thinking about. What's your experience with that?",
        "Thanks for sharing! What else is on your mind?"
    ],
    "goodbye": [
        "Goodbye! It was nice chatting with you!",
        "See you later! Have a wonderful day!",
        "Take care! Hope to chat again soon!",
        "Bye! Thanks for the conversation!",
        "Farewell! Wishing you all the best!"
    ]
}

def get_response(message):
    """Generate a response based on the user message"""
    message_lower = message.lower()
    
    # Check for greetings
    if any(word in message_lower for word in ['hello', 'hi', 'hey', 'greetings']):
        return random.choice(RESPONSES["greetings"])
    
    # Check for "how are you" type questions
    if any(phrase in message_lower for phrase in ['how are you', 'how do you do', 'how\'s it going']):
        return random.choice(RESPONSES["how_are_you"])
    
    # Check for weather talk
    if any(word in message_lower for word in ['weather', 'sunny', 'rainy', 'cold', 'hot', 'temperature']):
        return random.choice(RESPONSES["weather"])
    
    # Check for hobby/interest questions
    if any(word in message_lower for word in ['hobby', 'hobbies', 'interest', 'like to do', 'free time']):
        return random.choice(RESPONSES["hobbies"])
    
    # Check for goodbyes
    if any(word in message_lower for word in ['bye', 'goodbye', 'see you', 'farewell', 'take care']):
        return random.choice(RESPONSES["goodbye"])
    
    # Default response
    return random.choice(RESPONSES["default"])

@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')
    
    if not user_message:
        return jsonify({'error': 'Message is required.'}), 400
    
    try:
        response_text = get_response(user_message)
        return jsonify({'response': response_text})
    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)