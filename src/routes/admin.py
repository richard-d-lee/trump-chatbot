from flask import Blueprint, jsonify, request
from src.models.chat_log import ChatLog
from src.models.user import db
from datetime import datetime, timedelta
from functools import wraps
import os

admin_bp = Blueprint('admin', __name__)

def require_admin_key(f):
    """
    Decorator to require API key authentication for admin endpoints.
    API key should be passed in the X-Admin-Key header.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get API key from header
        provided_key = request.headers.get('X-Admin-Key')
        
        # Get expected key from environment variable
        expected_key = os.environ.get('ADMIN_API_KEY')
        
        # If no key is set in environment, deny access
        if not expected_key:
            return jsonify({
                'success': False,
                'message': 'Admin API is not configured. Please set ADMIN_API_KEY environment variable.'
            }), 500
        
        # Check if provided key matches
        if not provided_key or provided_key != expected_key:
            return jsonify({
                'success': False,
                'message': 'Unauthorized. Please provide valid X-Admin-Key header.'
            }), 401
        
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/logs', methods=['GET'])
@require_admin_key
def get_logs():
    """
    Get chat logs with optional filtering.
    Query parameters:
    - period: 'week' (default), 'all'
    - limit: number of logs to return (default: 100)
    """
    try:
        period = request.args.get('period', 'week')
        limit = int(request.args.get('limit', 100))
        
        query = ChatLog.query
        
        # Filter by time period
        if period == 'week':
            week_ago = datetime.utcnow() - timedelta(days=7)
            query = query.filter(ChatLog.created_at >= week_ago)
        
        # Order by most recent first and apply limit
        logs = query.order_by(ChatLog.created_at.desc()).limit(limit).all()
        
        return jsonify({
            'success': True,
            'count': len(logs),
            'logs': [log.to_dict() for log in logs]
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@admin_bp.route('/logs/stats', methods=['GET'])
@require_admin_key
def get_log_stats():
    """
    Get statistics about chat logs for the past week.
    """
    try:
        week_ago = datetime.utcnow() - timedelta(days=7)
        
        # Get logs from past week
        logs = ChatLog.query.filter(ChatLog.created_at >= week_ago).all()
        
        # Calculate statistics
        total_chats = len(logs)
        
        # Count by country
        by_country = {}
        for log in logs:
            country = log.country or 'Unknown'
            by_country[country] = by_country.get(country, 0) + 1
        
        # Count by response source
        by_source = {}
        for log in logs:
            source = log.response_source
            by_source[source] = by_source.get(source, 0) + 1
        
        return jsonify({
            'success': True,
            'stats': {
                'total_chats': total_chats,
                'by_country': by_country,
                'by_source': by_source
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@admin_bp.route('/logs/cleanup', methods=['POST'])
@require_admin_key
def cleanup_old_logs():
    """
    Manually trigger cleanup of logs older than 7 days.
    This is also run automatically, but can be triggered manually.
    """
    try:
        week_ago = datetime.utcnow() - timedelta(days=7)
        
        # Delete old logs
        deleted_count = ChatLog.query.filter(ChatLog.created_at < week_ago).delete()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Deleted {deleted_count} old log entries'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500
