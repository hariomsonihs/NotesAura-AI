# NotesAura AI Chatbot
## Powered by Sarvam AI

### Features:
✅ Natural conversation flow
✅ Clean text responses (no *, #, special characters)
✅ Conversation history management
✅ Beautiful gradient UI
✅ Real-time typing indicator
✅ Mobile responsive

### Setup Instructions:

1. Install dependencies:
```bash
pip install -r requirements_chatbot.txt
```

2. Run the application:
```bash
python chatbot_app.py
```

3. Open browser and go to:
```
http://localhost:5001
```

### Features Implemented:

1. **Response Cleaning**: Automatically removes markdown formatting (*, #, _, `) from AI responses
2. **Conversation Management**: Maintains last 10 messages for context
3. **Natural Feel**: Clean, formatted responses that don't feel robotic
4. **Clear Chat**: Option to reset conversation
5. **Error Handling**: Proper error messages for failed requests

### File Structure:
```
P/
├── chatbot_app.py          # Flask backend
├── templates/
│   └── chatbot.html        # Web interface
└── requirements_chatbot.txt # Dependencies
```

### API Endpoints:

- `GET /` - Main chatbot interface
- `POST /chat` - Send message and get AI response
- `POST /clear` - Clear conversation history

### Notes:
- The chatbot uses Sarvam AI API
- Conversation history is stored in memory (resets on server restart)
- Port: 5001 (to avoid conflict with other services)
