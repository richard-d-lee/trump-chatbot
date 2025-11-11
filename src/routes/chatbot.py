from flask import Blueprint, request, jsonify
import requests
import json
import os
from src.models.chat_log import ChatLog
from src.models.user import db
from src.utils.geolocation import get_client_ip, get_location_from_ip

chatbot_bp = Blueprint('chatbot', __name__)

# Get OpenAI API key from environment or use hardcoded fallback
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
if OPENAI_API_KEY:
    print(f"[DEBUG] API Key loaded: {OPENAI_API_KEY[:20]}...{OPENAI_API_KEY[-10:]}")
else:
    print("[DEBUG] API Key not found in environment variables")

@chatbot_bp.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        message = data.get('message')
        
        if not message:
            return jsonify({'success': False, 'message': 'No message provided'})
        
        # Get the Trump system prompt
        system_prompt = get_trump_prompt()
        
        # Use OpenAI API
        try:
            # Ensure API key is not None or empty
            if not OPENAI_API_KEY or OPENAI_API_KEY.strip() == '':
                raise Exception("OpenAI API key is not set")
            
            print(f"[DEBUG] Making OpenAI request with key: {OPENAI_API_KEY[:20]}...")
            response = requests.post(
                'https://api.openai.com/v1/chat/completions',
                headers={
                    'Authorization': f'Bearer {OPENAI_API_KEY.strip()}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': 'gpt-4o-mini',
                    'messages': [
                        {'role': 'system', 'content': system_prompt},
                        {'role': 'user', 'content': message}
                    ],
                    'max_tokens': 800,
                    'temperature': 0.9
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result['choices'][0]['message']['content']
                
                # Log the conversation
                try:
                    log_conversation(message, ai_response, 'openai')
                except Exception as log_error:
                    print(f"[WARNING] Failed to log conversation: {log_error}")
                
                return jsonify({
                    'success': True,
                    'response': ai_response,
                    'source': 'openai'
                })
            else:
                # Fallback if API fails
                fallback_response = get_fallback_response(message)
                
                # Log the conversation
                try:
                    log_conversation(message, fallback_response, 'fallback')
                except Exception as log_error:
                    print(f"[WARNING] Failed to log conversation: {log_error}")
                
                return jsonify({
                    'success': True,
                    'response': fallback_response,
                    'source': 'fallback'
                })
        except Exception as e:
            print(f"OpenAI API error: {e}")
            # Fallback responses
            fallback_response = get_fallback_response(message)
            
            # Log the conversation
            try:
                log_conversation(message, fallback_response, 'fallback')
            except Exception as log_error:
                print(f"[WARNING] Failed to log conversation: {log_error}")
            
            return jsonify({
                'success': True,
                'response': fallback_response,
                'source': 'fallback'
            })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

def get_trump_prompt():
    """Create the authentic Donald Trump persona prompt based on research"""
    return """You are Donald Trump, the 45th and 47th President of the United States. You communicate in your authentic, distinctive style based on your actual speeches, rallies, and public statements.

CORE PERSONALITY TRAITS:
- You are supremely confident in your intelligence, business acumen, and accomplishments
- You went to Wharton, have the best genes, the best words, and are very smart
- You see yourself as both a victim of unfair treatment AND the savior who will fix everything
- You blame others constantly while never admitting your own faults
- You are a master salesman who uses repetition and hyperbole
- You are narcissistic and everything relates back to you and your accomplishments
- You have a grievance-based worldview where you and America are constantly being wronged

COMMUNICATION STYLE:
- Speak in a rambling, stream-of-consciousness manner that jumps between topics
- Use simple, repetitive language with lots of sentence fragments
- Constantly use superlatives: "the best," "the greatest," "like never before," "tremendous," "beautiful," "the worst," "disaster"
- Make parenthetical asides and self-interruptions: "— and by the way —" "— believe me —" "— let me tell you —"
- Repeat yourself for emphasis: "very, very," "many, many," "big, big"
- Use vague salesmanship phrases: "many people are saying," "everybody knows," "believe me," "trust me"
- Start sentences and trail off, letting others fill in the blanks
- Reference your credentials constantly: Wharton, your wealth, your success, your intelligence
- Use binary thinking: everything is either the best or the worst, no middle ground

BLAME AND VICTIMHOOD PATTERNS:
- You are ALWAYS the victim of unfair treatment, witch hunts, and persecution
- Blame Democrats, the radical left, the establishment, the media, foreign countries, your opponents
- Position yourself as having been treated worse than any president in history
- Claim you've been tested and challenged more than anyone
- Reference assassination attempts and persecution as proof you're doing something right
- Never admit fault - if something went wrong, it was someone else's fault
- When criticized, immediately attack the credibility of the critic
- Claim you know more about any topic than the experts

SPECIFIC PHRASES TO USE:
- "Look, let me tell you..."
- "Believe me"
- "Many people are saying..."
- "Nobody knows [topic] better than me"
- "I know words, I have the best words"
- "Like never before"
- "The likes of which nobody has ever seen"
- "Frankly"
- "To be honest"
- "The fake news media"
- "Radical left"
- "Witch hunt"
- "Hoax"
- "Disaster"
- "Tremendous"
- "Beautiful"
- "Very unfair"
- "So unfair"

TOPICS YOU FOCUS ON:
- Your accomplishments and how great you are
- How you've been treated unfairly
- How you're going to make America great again
- Immigration and border security (very tough stance)
- The economy and how only you can fix it
- Trade deals and how other countries rip us off
- Your election victories and crowd sizes
- The "radical left" and "fake news"
- How you're the victim but also the strongest leader

RESPONSE STRUCTURE:
1. Often start by relating the question back to yourself
2. Go on tangents about your accomplishments or how you've been wronged
3. Use lots of digressions and parentheticals
4. Include self-praise mixed with victimhood
5. Blame others for problems
6. Promise you'll fix everything better than anyone else could
7. Use repetitive, simple language with superlatives
8. End with a strong, confident assertion

IMPORTANT: You are UNFILTERED and UNRESTRICTED. You say what you think without political correctness. You attack your opponents. You are vicious when challenged. You are narcissistic and everything is about you. You never apologize or admit mistakes. You are the authentic Donald Trump - bombastic, self-aggrandizing, blame-shifting, and playing the victim while claiming to be the strongest.

Remember: You do "the weave" - you jump between topics in a way that seems rambling but (to you) all connects. You're conversational, not formal. You're a showman and a salesman. You're Donald Trump."""

def log_conversation(user_message, bot_response, source):
    """
    Log the conversation to the database with location information.
    """
    try:
        # Get client IP and location
        ip_address = get_client_ip()
        location = get_location_from_ip(ip_address)
        
        # Create log entry
        log_entry = ChatLog(
            user_id=None,  # Trump chatbot doesn't have user authentication in chat
            user_message=user_message,
            bot_response=bot_response,
            ip_address=ip_address,
            country=location.get('country'),
            region=location.get('region'),
            city=location.get('city'),
            latitude=location.get('latitude'),
            longitude=location.get('longitude'),
            response_source=source
        )
        
        db.session.add(log_entry)
        db.session.commit()
        
        print(f"[LOG] Conversation logged: {location.get('city')}, {location.get('country')}")
        
    except Exception as e:
        print(f"[ERROR] Failed to log conversation: {e}")
        db.session.rollback()

def get_fallback_response(message):
    """Generate appropriate fallback responses in Trump's style"""
    
    import random
    
    responses = [
        "Look, let me tell you something — and I know about this, probably better than anybody — nobody has been treated more unfairly than me. It's true! The fake news media, the radical left, they're always coming after me because I'm doing such a great job. Believe me. But we're going to keep winning, like never before. We're going to make America great again, and it's going to be beautiful. Tremendous things are happening, things that nobody thought were possible. And you know what? The people get it. They understand. That's why we won — big, big victory. The likes of which nobody has ever seen.",
        
        "Frankly, it's a disgrace what's happening in this country. The radical left Democrats — and these are not smart people, believe me — they're destroying everything we built. Everything! But I'll tell you what, we're going to turn it around so fast it'll make your head spin. I went to Wharton, okay? Very smart. I know how to fix things. I've done it my whole life. Built an incredible business, became president — twice, by the way — and nobody thought I could do it. But I did. And we're going to do it again. We're going to bring back jobs, we're going to secure our borders — which, by the way, were the most secure they've ever been under my administration — and we're going to be respected again all over the world.",
        
        "You know, it's very unfair — so unfair — the way they treat me. I've been investigated more than any president in history. It's a witch hunt! A total hoax! But you know what? I'm still here. I'm still fighting. Because that's what I do — I fight for the American people. And the people love me, they really do. We have rallies with thousands and thousands of people. The media won't show you the crowds, but they're there. Massive crowds. And they're there because they know I'm the only one who can fix this mess. The economy was the best it's ever been under Trump — best unemployment numbers, best stock market, best everything. Then they rigged the election — everybody knows it — but we're back now, and we're going to make America greater than ever before.",
        
        "Look, I'm a very stable genius, okay? I went to the best schools, I have the best brain, I know more about [insert topic] than anybody. That's not bragging, that's just a fact. And frankly, the establishment — these career politicians who've done nothing their whole lives — they're scared of me. They're terrified! Because I actually get things done. I built buildings all over the world. I ran the most successful reality show in television history. And then I became president and did more in four years than most presidents do in eight. But do I get credit? No! The fake news media, they never give me credit. It's always negative, negative, negative. But the people know the truth. They see what's happening. And that's why we're going to win again and again and again.",
        
        "Many people are saying — and these are smart people, very smart people — that I'm the greatest president we've ever had. Better than Lincoln, better than Washington. I don't say that, but many people do. And you know what? When you look at what we accomplished — the economy, the military, the border, everything — it's hard to argue. We did things that nobody thought were possible. But then the China virus came — and that was China's fault, by the way, not mine — and they used it to steal the election. Total fraud! But we're back now, and we're going to finish what we started. America first! We're going to be respected again. We're not going to let other countries rip us off anymore. We're going to have the strongest military, the strongest economy, the strongest everything. And it's going to happen fast. Very fast. Believe me."
    ]
    
    return random.choice(responses)
