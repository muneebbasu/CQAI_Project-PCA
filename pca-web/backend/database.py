# database.py
import sqlite3
import json
import os
import datetime
from pathlib import Path

class FeedbackStorage:
    def __init__(self):
        # Create necessary directories
        self.feedback_dir = Path('backend/feedback_data')
        self.backup_dir = self.feedback_dir / 'backup'
        self.feedback_dir.mkdir(exist_ok=True, parents=True)
        self.backup_dir.mkdir(exist_ok=True)
        
        # Database setup
        self.db_path = self.feedback_dir / 'feedback.db'
        self.json_path = self.feedback_dir / 'feedback_data.json'
        
        # Initialize database
        self._init_db()

    def _init_db(self):
        """Initialize SQLite database"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS feedback
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        rating REAL NOT NULL,
                        comment TEXT NOT NULL,
                        timestamp TEXT NOT NULL)''')
            conn.commit()
        except sqlite3.DatabaseError as e:
            print(f"Database error: {e}")
        finally:
            conn.close()

    def save_feedback(self, name, rating, comment):
        """Save feedback to both SQLite and JSON"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        
        # Save to SQLite
        try:
            conn = sqlite3.connect(str(self.db_path))
            c = conn.cursor()
            c.execute("INSERT INTO feedback (name, rating, comment, timestamp) VALUES (?, ?, ?, ?)",
                    (name, float(rating), comment, timestamp))
            conn.commit()
        except sqlite3.DatabaseError as e:
            print(f"Database error: {e}")
        finally:
            conn.close()

        # Save to JSON
        feedback_data = {
            "name": name,
            "rating": float(rating),
            "comment": comment,
            "timestamp": timestamp
        }

        existing_feedback = []
        if self.json_path.exists():
            with open(self.json_path, 'r') as f:
                try:
                    existing_feedback = json.load(f)
                except json.JSONDecodeError:
                    pass

        existing_feedback.append(feedback_data)
        
        with open(self.json_path, 'w') as f:
            json.dump(existing_feedback, f, indent=4)

        # Create backup
        backup_path = self.backup_dir / f'feedback_{timestamp}.json'
        with open(backup_path, 'w') as f:
            json.dump(existing_feedback, f, indent=4)

    def get_all_feedback(self):
        """Retrieve all feedback from SQLite"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            c = conn.cursor()
            c.execute("SELECT name, rating, comment, timestamp FROM feedback")
            rows = c.fetchall()
            feedback_list = [{"name": row[0], "rating": row[1], "comment": row[2], "timestamp": row[3]} for row in rows]
            return feedback_list
        except sqlite3.DatabaseError as e:
            print(f"Database error: {e}")
            return []
        finally:
            conn.close()

    def get_recent_feedback(self, limit=5):
        """Get recent feedback"""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT * FROM feedback ORDER BY timestamp DESC LIMIT ?", (limit,))
        feedback = [{
            'name': row['name'],
            'rating': row['rating'],
            'comment': row['comment'],
            'timestamp': row['timestamp']
        } for row in c.fetchall()]
        conn.close()
        return feedback

    def _create_backup(self):
        """Create backup of feedback data"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.backup_dir / f'feedback_backup_{timestamp}.json'
        
        # Copy current feedback to backup
        with open(self.json_path, 'r') as f:
            feedback_data = json.load(f)
            
        with open(backup_path, 'w') as f:
            json.dump(feedback_data, f, indent=4)

    def cleanup_old_feedback(self, days=30):
        """Remove old feedback"""
        cutoff_date = datetime.datetime.now() - datetime.timedelta(days=days)
        
        # Remove old feedback from SQLite
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()
        c.execute("DELETE FROM feedback WHERE timestamp < ?", (cutoff_date.strftime("%Y-%m-%d %H:%M:%S"),))
        conn.commit()
        conn.close()

        # Remove old feedback from JSON
        if self.json_path.exists():
            with open(self.json_path, 'r') as f:
                feedback_data = json.load(f)
            
            current_feedback = [
                feedback for feedback in feedback_data
                if datetime.datetime.strptime(feedback['timestamp'], "%Y-%m-%d %H:%M:%S") > cutoff_date
            ]
            
            with open(self.json_path, 'w') as f:
                json.dump(current_feedback, f, indent=4)