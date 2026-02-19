from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from sarvamai import SarvamAI
import re
import html
import time
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

client = SarvamAI(
    api_subscription_key=os.getenv('SARVAM_API_KEY')
)

# Store conversation history
conversation_history = []

# NotesAura App Context - System Prompt
NOTESAURA_CONTEXT = """
You are NotesAura AI, an intelligent assistant integrated into the NotesAura app.

NotesAura App Details:
- App Name: NotesAura - Programming Guide
- Developer: Hariom Kumar (CodeVora)
- Latest Version: 12.0.hs (Updated: 19 Jan 2026)
- Platform: Android (Requires Android 7.0+)
- Downloads: 50+ on Google Play Store
- Rating: 5.0 stars (6 reviews)
- Content Rating: Rated for 3+
- Download Size: 41 MB
- Release Date: 8 May 2025

Developer Contact:
- Email: hariomsoni0818@gmail.com
- Website: https://notesaura.vercel.app/home.html
- GitHub/Instagram/LinkedIn: hariomsonihs

App Features:
- Comprehensive programming tutorials and guides
- Support for multiple programming languages
- Code examples and explanations
- Interview preparation materials
- DSA (Data Structures & Algorithms) content
- Project ideas and implementations
- Regular updates with new content
- Offline access to notes
- Clean and user-friendly interface
- Free to use with no ads

IMPORTANT INSTRUCTIONS:
- Keep responses concise and complete
- Avoid creating tables in markdown format
- Use bullet points instead of tables for comparisons
- Always complete your response fully
- If explaining comparisons, use simple lists

When users ask about NotesAura, provide detailed, accurate information about the app.
Always be helpful, professional, and knowledgeable about programming topics.
"""

def get_system_prompt():
    """Return system prompt with NotesAura context"""
    return {"role": "system", "content": NOTESAURA_CONTEXT}

def clean_response(text):
    """Parse and format response with proper markdown support"""
    # Decode HTML entities
    text = html.unescape(text)
    return text

@app.route('/')
def home():
    return render_template('chatbot.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Add user message to history
        conversation_history.append({"role": "user", "content": user_message})
        
        # Prepare messages with system prompt
        messages = [get_system_prompt()]
        
        # Keep only last 10 messages for context
        recent_history = conversation_history[-10:]
        messages.extend(recent_history)
        
        # Retry logic for API calls
        max_retries = 3
        retry_delay = 1
        
        for attempt in range(max_retries):
            try:
                # Get AI response
                response = client.chat.completions(messages=messages)
                
                # Extract and clean the response
                ai_message = response.choices[0].message.content if hasattr(response, 'choices') else str(response)
                ai_message = clean_response(ai_message)
                
                # Add AI response to history
                conversation_history.append({"role": "assistant", "content": ai_message})
                
                return jsonify({
                    'response': ai_message,
                    'success': True
                })
            except Exception as api_error:
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    retry_delay *= 2
                else:
                    raise api_error
        
    except Exception as e:
        error_msg = str(e)
        # Clean up error message
        if 'internal_server_error' in error_msg.lower():
            error_msg = 'The AI service is temporarily unavailable. Please try again in a moment.'
        
        return jsonify({
            'error': error_msg,
            'success': False
        }), 500

@app.route('/clear', methods=['POST'])
def clear_history():
    global conversation_history
    conversation_history = []
    return jsonify({'success': True, 'message': 'Conversation cleared'})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
