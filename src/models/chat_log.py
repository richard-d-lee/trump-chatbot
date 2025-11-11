from src.models.user import db
from datetime import datetime

class ChatLog(db.Model):
    """
    Model to store chat logs for analytics and monitoring.
    Logs are automatically deleted after 7 days.
    """
    __tablename__ = 'chat_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # Nullable for guest users
    
    # Message content
    user_message = db.Column(db.Text, nullable=False)
    bot_response = db.Column(db.Text, nullable=False)
    
    # Location data
    ip_address = db.Column(db.String(45), nullable=True)  # IPv4 or IPv6
    country = db.Column(db.String(100), nullable=True)
    region = db.Column(db.String(100), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    
    # Response metadata
    response_source = db.Column(db.String(20), nullable=False)  # 'openai' or 'fallback'
    
    # Timestamp
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def to_dict(self):
        """Convert log entry to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user_message': self.user_message,
            'bot_response': self.bot_response,
            'ip_address': self.ip_address,
            'country': self.country,
            'region': self.region,
            'city': self.city,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'response_source': self.response_source,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
