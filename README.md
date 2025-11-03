# Donald Trump AI Chatbot

An AI chatbot featuring an authentic Donald Trump persona, powered by OpenAI's GPT-4.

## Features

- **Authentic Trump Persona**: Based on actual speeches, rallies, and communication patterns
- **Unfiltered Responses**: Captures Trump's distinctive speaking style including:
  - Rambling, stream-of-consciousness communication
  - Heavy use of superlatives and hyperbole
  - Blame-shifting and victimhood rhetoric
  - Self-aggrandizement and narcissistic elements
  - "The weave" - jumping between topics
  - Simple, repetitive language with catchphrases
- **Conversation History**: Save and continue your conversations
- **Mobile Responsive**: Beautiful interface on all screen sizes

## Quick Start

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for complete deployment instructions.

### Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `.env` file:
```bash
OPENAI_API_KEY=your_openai_api_key_here
SECRET_KEY=your_secret_key_here
```

3. Run the application:
```bash
python src/main.py
```

4. Open http://localhost:5000 in your browser

## Deployment

This application is ready to deploy to:
- **Render** (recommended) - See deployment guide
- **Railway** - See deployment guide
- **Heroku** - Use included Procfile

## Technology Stack

- **Backend**: Flask (Python)
- **AI**: OpenAI GPT-4o-mini
- **Database**: SQLite (default) or PostgreSQL
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Authentication**: Flask-Login with SQLAlchemy

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key | Yes |
| `SECRET_KEY` | Flask session secret | No (auto-generated) |
| `DATABASE_URL` | Database connection string | No (defaults to SQLite) |
| `PORT` | Server port | No (defaults to 5000) |

## About the Persona

This chatbot uses an authentic Donald Trump persona based on extensive research of his:
- Inaugural addresses and formal speeches
- Campaign rally transcripts
- Social media posts (Twitter/Truth Social)
- Linguistic analysis by professional linguists
- Communication patterns including victimhood rhetoric and blame-shifting

The AI captures Trump's distinctive characteristics:
- "The weave" - rambling between topics
- Constant self-reference and credential-touting
- Victim-to-avenger narrative
- Binary thinking (everything is best or worst)
- Salesmanship phrases ("believe me," "many people are saying")
- No content restrictions - authentic and unfiltered

## License

Free to use for educational and entertainment purposes.

---

*"Look, I'm the best at chatbots. Nobody does chatbots better than me, believe me!"*
