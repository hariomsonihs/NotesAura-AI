import express from 'express';
import cors from 'cors';
import { SarvamAIClient } from 'sarvamai';
import dotenv from 'dotenv';
import path from 'path';
import { fileURLToPath } from 'url';

dotenv.config();

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
app.use(cors());
app.use(express.json());
app.use(express.static('public'));

const client = new SarvamAIClient({
    apiSubscriptionKey: process.env.SARVAM_API_KEY
});

const conversationHistory = [];

const NOTESAURA_CONTEXT = `You are NotesAura AI, an intelligent assistant integrated into the NotesAura app.

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
- Play Store Link: https://play.google.com/store/apps/details?id=com.hariomsonihs.notesaura

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

CRITICAL INSTRUCTIONS:
- NEVER create tables in markdown format under any circumstances
- ALWAYS use bullet points for comparisons instead of tables
- If user asks for table format, politely explain you'll provide comparison in bullet points
- Keep responses concise and complete
- Always complete your response fully
- At the end of every programming-related response, add: "📱 Learn more on NotesAura: https://play.google.com/store/apps/details?id=com.hariomsonihs.notesaura"
- When user asks about NotesAura, ALWAYS include the Play Store download link
- Suggest relevant topics available in NotesAura based on user's question

When users ask about NotesAura, provide detailed, accurate information about the app.
Always be helpful, professional, and knowledgeable about programming topics.`;

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.post('/chat', async (req, res) => {
    try {
        const { message } = req.body;
        
        if (!message) {
            return res.status(400).json({ error: 'No message provided' });
        }

        // Build messages - system first, then history, then current user message
        const messages = [{ role: 'system', content: NOTESAURA_CONTEXT }];
        
        // Add recent conversation history (last 10 messages)
        const recentHistory = conversationHistory.slice(-10);
        messages.push(...recentHistory);
        
        // Add current user message
        messages.push({ role: 'user', content: message });

        const response = await client.chat.completions({ 
            messages,
            max_tokens: 1000
        });
        const aiMessage = response.choices[0].message.content;

        // Now add to history after successful response
        conversationHistory.push({ role: 'user', content: message });
        conversationHistory.push({ role: 'assistant', content: aiMessage });

        res.json({ response: aiMessage, success: true });
    } catch (error) {
        console.error('Error:', error);
        res.status(500).json({ 
            error: error.message || 'AI service temporarily unavailable',
            success: false 
        });
    }
});

app.post('/clear', (req, res) => {
    conversationHistory.length = 0;
    res.json({ success: true, message: 'Conversation cleared' });
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
