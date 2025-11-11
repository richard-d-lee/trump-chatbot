import threading
import time
from datetime import datetime, timedelta
from src.models.chat_log import ChatLog
from src.models.user import db

def cleanup_old_logs():
    """
    Delete chat logs older than 7 days.
    This function is called by the scheduler.
    """
    try:
        week_ago = datetime.utcnow() - timedelta(days=7)
        deleted_count = ChatLog.query.filter(ChatLog.created_at < week_ago).delete()
        db.session.commit()
        
        print(f"[SCHEDULER] Cleaned up {deleted_count} old log entries")
        return deleted_count
        
    except Exception as e:
        print(f"[SCHEDULER ERROR] Failed to cleanup logs: {e}")
        db.session.rollback()
        return 0

def schedule_cleanup(app):
    """
    Schedule automatic cleanup of old logs.
    Runs once per day at midnight UTC.
    """
    def run_scheduler():
        with app.app_context():
            while True:
                try:
                    # Calculate time until next midnight UTC
                    now = datetime.utcnow()
                    tomorrow = now + timedelta(days=1)
                    next_midnight = datetime(tomorrow.year, tomorrow.month, tomorrow.day, 0, 0, 0)
                    seconds_until_midnight = (next_midnight - now).total_seconds()
                    
                    print(f"[SCHEDULER] Next cleanup scheduled in {seconds_until_midnight / 3600:.1f} hours")
                    
                    # Wait until midnight
                    time.sleep(seconds_until_midnight)
                    
                    # Run cleanup
                    cleanup_old_logs()
                    
                except Exception as e:
                    print(f"[SCHEDULER ERROR] Scheduler error: {e}")
                    # Wait 1 hour before retrying
                    time.sleep(3600)
    
    # Start scheduler in background thread
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    print("[SCHEDULER] Log cleanup scheduler started")
