import os
import random
import re
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
    ],
    "incomprehensible": [
        "Can't understand",
        "I'm sorry, I can't understand what you're trying to say.",
        "That doesn't seem to make sense to me. Can you try rephrasing?",
        "I'm having trouble understanding that. Could you clarify?"
    ]
}

def is_incomprehensible(message):
    """Check if the message is incoherent or incomprehensible"""
    # Remove whitespace and convert to lowercase
    cleaned_message = message.strip().lower()
    
    # Check if message is too short (less than 2 characters)
    if len(cleaned_message) < 2:
        return True
    
    # Check if message is mostly special characters or numbers
    alphanumeric_chars = re.findall(r'[a-zA-Z0-9]', cleaned_message)
    if len(alphanumeric_chars) / len(cleaned_message) < 0.3:
        return True
    
    # Check for excessive repetition of characters (like "aaaaaaa" or "hehehehe")
    if re.search(r'(.)\1{4,}', cleaned_message):
        return True
    
    # Check for random character sequences (no vowels in a long word)
    words = re.findall(r'[a-zA-Z]+', cleaned_message)
    for word in words:
        if len(word) > 4 and not re.search(r'[aeiouAEIOU]', word):
            return True
    
    # Check for excessive special characters
    special_char_count = len(re.findall(r'[^\w\s]', cleaned_message))
    if special_char_count > len(cleaned_message) * 0.5:
        return True
    
    return False

def get_response(message):
    """Generate a response based on the user message"""
    message_lower = message.lower()
    
    # First check if the message is incomprehensible
    if is_incomprehensible(message):
        return random.choice(RESPONSES["incomprehensible"])
    
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