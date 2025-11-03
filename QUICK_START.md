# Quick Start Guide - Trump AI Chatbot

## Instant Deployment (Recommended)

### Option 1: Deploy with Manus (Easiest)
```bash
# Extract the package
unzip trump-chatbot.zip

# Deploy to public URL
service_deploy_backend flask trump-chatbot/
```
✅ **Done!** Your app will be live at a public URL.

### Option 2: Local Development
```bash
# Extract and setup
unzip trump-chatbot.zip
cd trump-chatbot
pip install -r requirements.txt

# Create .env file
echo "OPENAI_API_KEY=your-key-here" > .env
echo "SECRET_KEY=random-secret" >> .env

# Run locally
python src/main.py
```
✅ **Access at:** http://localhost:5000

## What You Get

🇺🇸 **Authentic Trump Persona:**
- Based on real speeches and communication patterns
- Rambling, stream-of-consciousness responses
- Heavy use of superlatives and hyperbole
- Blame-shifting and victimhood rhetoric
- Self-aggrandizement and narcissistic elements
- "The weave" - jumping between topics
- No content restrictions - unfiltered Trump

🔧 **Features:**
- User login/register system
- Guest access (no account needed)
- OpenAI GPT-4o-mini powered responses
- Fallback responses if API fails
- Mobile responsive design
- Patriotic red, white, and blue color scheme

## File Structure
```
trump-chatbot/
├── README.md              # Full documentation
├── DEPLOYMENT_GUIDE.md    # Deployment guide
├── QUICK_START.md         # This file
├── TRUMP_CHATBOT_GUIDE.md # Complete guide
├── requirements.txt       # Python dependencies
└── src/
    ├── main.py           # Flask app
    ├── models/           # Database models
    ├── routes/           # API endpoints
    │   └── chatbot.py   # Trump persona logic
    └── static/           # Frontend files
        ├── index.html
        ├── script.js
        ├── styles.css
        └── images/       # Add trump.png here
```

## First Time Setup

1. **Extract:** `unzip trump-chatbot.zip`
2. **Install:** `pip install -r requirements.txt`
3. **Configure:** Create `.env` file with your OpenAI API key
4. **Run:** `python src/main.py`
5. **Test:** Open http://localhost:5000 and chat!

## Environment Setup

Create a `.env` file in the project root:

```
OPENAI_API_KEY=sk-your-openai-api-key-here
SECRET_KEY=any-random-string-here
```

**Get OpenAI API Key:**
1. Go to https://platform.openai.com/
2. Sign up or log in
3. Go to API Keys section
4. Create new secret key
5. Copy to `.env` file

## Need Help?

- Check `README.md` for full documentation
- Check `DEPLOYMENT_GUIDE.md` for deployment to Render/Railway
- Check `TRUMP_CHATBOT_GUIDE.md` for complete details
- Check `SETUP_INSTRUCTIONS.md` for troubleshooting

## Customization

- Edit `src/static/script.js` for frontend changes
- Edit `src/routes/chatbot.py` for Trump persona tweaks
- Add `trump.png` to `src/static/images/` for header image
- Modify `src/static/styles.css` for styling changes
- Adjust temperature in `chatbot.py` for more/less rambling

## Testing the Persona

Try these prompts to see authentic Trump responses:

1. "What do you think about the media?"
2. "Tell me about your accomplishments"
3. "How would you fix the economy?"
4. "What's your opinion on immigration?"
5. "Why should people support you?"

You should see:
- Rambling responses with tangents
- Heavy use of "tremendous," "beautiful," "disaster"
- Blame-shifting to Democrats/media/establishment
- Self-praise and credential-touting
- Victimhood claims mixed with strength assertions

**Ready to Make Chatbots Great Again!** 🚀🇺🇸
