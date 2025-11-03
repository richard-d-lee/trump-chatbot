# Trump Chatbot - Complete Guide

## Overview

This is a fully functional Donald Trump AI chatbot based on your Jesus chatbot codebase. It features an authentic Trump persona with no content restrictions, capturing his distinctive communication style including blame-shifting, victimhood rhetoric, and narcissistic elements.

## What Was Changed

### 1. Backend Changes (`src/routes/chatbot.py`)

**Removed:**
- All 6 Jesus representations (traditional, historical, african, mormon, ai, current)
- Scripture mode functionality
- Bible version selection
- Multiple system prompts

**Added:**
- Single Trump persona with comprehensive system prompt
- Authentic Trump communication patterns based on research
- Higher temperature (0.9) for more varied, rambling responses
- Increased max_tokens (800) for longer responses
- 5 fallback responses in Trump's authentic style

**Key Features of the Trump Persona:**
- Rambling, stream-of-consciousness communication
- Heavy use of superlatives ("the best," "tremendous," "beautiful")
- Constant self-praise and credential-touting
- Blame-shifting to Democrats, media, establishment, foreign countries
- Victimhood rhetoric mixed with savior complex
- "The weave" - jumping between topics
- Salesmanship phrases ("believe me," "many people are saying")
- No self-reflection or admission of fault
- Binary thinking (everything is best or worst)

### 2. Frontend Changes

**HTML (`src/static/index.html`):**
- Changed title from "Jesus Christ" to "Donald Trump AI"
- Updated header image reference from Jesus to Trump
- Changed subtitle to "45th & 47th President of the United States"
- Removed scripture mode toggle
- Removed Bible version selector
- Removed representation selection modal
- Removed donate button
- Updated initial message to Trump's voice
- Changed placeholder text to "Ask Trump anything..."

**JavaScript (`src/static/script.js`):**
- Simplified from `JesusChatbot` class to `TrumpChatbot` class
- Removed representation switching logic
- Removed scripture mode handling
- Removed Bible version handling
- Removed conversation history per representation
- Single conversation thread
- Updated message CSS classes from `jesus-message` to `trump-message`

**CSS (`src/static/styles.css`):**
- Changed color scheme from purple/pink to red/white/blue (patriotic)
- Background: Blue to red gradient
- Header: Dark blue to light blue gradient
- User messages: Blue gradient
- Trump messages: Red gradient
- Updated class names from `.header-jesus-img` to `.header-trump-img`
- Updated class names from `.jesus-message` to `.trump-message`
- White text in header for better contrast

### 3. Documentation

**README.md:**
- Updated to describe Trump chatbot features
- Listed authentic communication characteristics
- Removed religious references
- Added information about research sources

## Installation & Setup

### Prerequisites
- Python 3.8+
- OpenAI API key

### Local Development

1. **Install dependencies:**
```bash
cd trump-chatbot
pip install -r requirements.txt
```

2. **Create `.env` file:**
```bash
OPENAI_API_KEY=your_openai_api_key_here
SECRET_KEY=your_secret_key_here
```

3. **Run the application:**
```bash
python src/main.py
```

4. **Open in browser:**
```
http://localhost:5000
```

## Deployment Options

### Option 1: Render (Recommended)

1. Push code to GitHub
2. Connect to Render
3. Set environment variables:
   - `OPENAI_API_KEY`
   - `SECRET_KEY` (optional)
4. Deploy

### Option 2: Railway

1. Push code to GitHub
2. Connect to Railway
3. Set environment variables
4. Deploy

### Option 3: Heroku

1. Push code to GitHub
2. Connect to Heroku
3. Set environment variables
4. Use included `Procfile`
5. Deploy

## Trump Persona Details

### Communication Style Research

The Trump persona is based on extensive research including:

1. **Linguistic Analysis:**
   - NPR analysis of Trump's "weaving" style
   - Vox article on Trump's speaking patterns by linguists
   - Academic research on Trump's rhetoric

2. **Actual Speeches:**
   - 2025 Inaugural Address
   - Campaign rally transcripts
   - Formal addresses

3. **Communication Patterns:**
   - Strategic victimhood performance
   - Blame-shifting mechanisms
   - Victim-to-avenger narrative
   - Economic victimhood claims

### Key Characteristics Implemented

**Linguistic Patterns:**
- Rambling with false starts and parentheticals
- Sentence fragments that trail off
- Heavy repetition ("very, very," "many, many")
- Simple, low-complexity words
- Lack of hypotaxis (embedded clauses)

**Rhetorical Devices:**
- Hyperbole and superlatives
- Binary framing (always/never)
- Vague salesmanship phrases
- Self-interruptions and asides

**Content Patterns:**
- Constant self-reference
- Credential-touting (Wharton, wealth, success)
- Victimhood claims
- Blame-shifting
- Promises of retribution
- No admission of fault

### Example Responses

The chatbot will respond in Trump's authentic style:

**User:** "What do you think about the economy?"

**Trump:** "Look, let me tell you about the economy — and I know about this, probably better than anybody, okay? I went to Wharton, very smart, best school — the economy was the BEST it's ever been under my administration. Best unemployment numbers, best stock market, best everything. Then the radical left came in and destroyed it. Total disaster! But we're going to fix it, believe me. We're going to bring back jobs, we're going to make deals like nobody's ever seen before. It's going to be tremendous. The likes of which this country has never seen. And frankly, the fake news media won't tell you this, but everybody knows it's true."

## Technical Notes

### API Configuration
- Model: `gpt-4o-mini`
- Temperature: `0.9` (high for varied, rambling responses)
- Max tokens: `800` (longer responses)
- Timeout: `30` seconds

### No Content Restrictions
The system prompt explicitly states the persona is "UNFILTERED and UNRESTRICTED" to capture Trump's authentic communication style without political correctness.

### Fallback Responses
If the API fails, the chatbot has 5 pre-written responses in Trump's style that demonstrate:
- Victimhood rhetoric
- Blame-shifting
- Self-aggrandizement
- Credential-touting
- Promises to fix everything

## Customization

### To Adjust Trump's "Intensity"

Edit `src/routes/chatbot.py`:

**More rambling:** Increase temperature to 1.0
**More focused:** Decrease temperature to 0.7
**Longer responses:** Increase max_tokens to 1000+
**Shorter responses:** Decrease max_tokens to 500

### To Add New Fallback Responses

Add to the `responses` list in `get_fallback_response()` function.

### To Modify the Persona

Edit the system prompt in `get_trump_prompt()` function. The current prompt is comprehensive and based on research, but you can adjust emphasis on different characteristics.

## File Structure

```
trump-chatbot/
├── src/
│   ├── database/
│   │   └── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── chatbot.py      # Main Trump persona logic
│   │   └── user.py
│   ├── static/
│   │   ├── images/
│   │   │   └── trump.png   # Add your Trump image here
│   │   ├── index.html      # Main UI
│   │   ├── script.js       # Frontend logic
│   │   └── styles.css      # Styling
│   └── main.py             # Flask app entry point
├── .env                    # Environment variables (create this)
├── Procfile               # For Heroku deployment
├── README.md              # Main documentation
├── TRUMP_CHATBOT_GUIDE.md # This file
├── requirements.txt       # Python dependencies
├── railway.json          # Railway config
└── render.yaml           # Render config
```

## Adding Trump Image

You'll need to add a Trump image to make the UI complete:

1. Find or create a Trump portrait image
2. Save as `src/static/images/trump.png`
3. Recommended size: 500x500px or larger
4. The CSS will automatically crop it to a circle

Alternatively, you can use a placeholder or modify the HTML to remove the image.

## Testing

### Test the Persona

Try these prompts to see the authentic Trump responses:

1. "What do you think about the media?"
2. "Tell me about your accomplishments"
3. "What happened in the 2020 election?"
4. "How would you fix immigration?"
5. "Why should people vote for you?"

You should see:
- Rambling responses that jump between topics
- Heavy use of superlatives
- Blame-shifting to Democrats/media
- Victimhood claims
- Self-praise
- Promises to fix everything

## Troubleshooting

### API Key Issues
- Make sure `OPENAI_API_KEY` is set in `.env`
- Check that the key is valid and has credits

### Responses Not Trump-like
- Check that `chatbot.py` has the correct system prompt
- Verify temperature is set to 0.9
- Make sure you're using the modified version, not the original Jesus bot

### UI Issues
- Clear browser cache
- Check that `styles.css` has the red/blue color scheme
- Verify `script.js` references `trump-message` not `jesus-message`

## License

Free to use for educational and entertainment purposes.

## Credits

Based on the Jesus chatbot by richard-d-lee (https://github.com/richard-d-lee/jesus-chatbot)

Modified to create an authentic Donald Trump AI persona based on linguistic research and analysis of his actual speeches and communication patterns.
