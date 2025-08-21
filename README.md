# Flask Chatbot App

A simple web-based chatbot using Flask with pre-created small talk responses.

## Features
- Clean, modern chat UI
- Pre-programmed responses for common topics like greetings, weather, hobbies
- **Incoherent text detection** - Detects and responds to incomprehensible input
- No external API dependencies - runs completely offline

## Setup
1. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
2. Run the app:
   ```sh
   python app.py
   ```
3. Open your browser at http://localhost:5000

## How it works
The chatbot uses keyword matching to detect conversation topics and responds with randomized, pre-written responses for:
- **Incomprehensible text** - Detects patterns like excessive repetition, random characters, too many special characters
- Greetings (hello, hi, hey)
- How are you questions
- Weather talk
- Hobby/interest discussions
- Goodbyes
- General conversation fallbacks

## Testing Incoherent Text Detection
Try these examples to test the new feature:
- `aaaaaaa` (excessive repetition)
- `!@#$%^&*` (too many special characters)
- `qwrtyx` (random characters with no vowels)
- `a` (too short)