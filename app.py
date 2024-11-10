from flask import Flask, render_template, request, g, flash
import barcode_gen
import sqlite3
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
DATABASE = os.environ.get('DATABASE_PATH', 'database.db')

# manage db defs
def get_db(DATABASE):
    """Get database connection."""
    db = getattr(g, '_database', None)
    if db is None:
        try:
            db = g._database = sqlite3.connect(DATABASE)
            db.row_factory = sqlite3.Row
        except sqlite3.Error as e:
            logger.error(f"Database connection error: {e}")
            raise
    return db

def close_connection(exception):
    """Close database connection."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

app.teardown_appcontext(close_connection)

def add_item(name, img_link):
    """Add item to database."""
    try:
        db = get_db(DATABASE)
        db.execute('INSERT INTO items (name, img_link) VALUES (?, ?)', (name, img_link))
        db.commit()
        logger.info(f"Item added: {name}")
        return True
    except sqlite3.Error as e:
        logger.error(f"Error adding item: {e}")
        return False

def init_db():
    """Initialize database."""
    try:
        with app.app_context():
            db = get_db(DATABASE)
            db.execute('''
                CREATE TABLE IF NOT EXISTS items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    img_link TEXT NOT NULL
                );
            ''')
            db.commit()
            logger.info("Database initialized successfully")
    except sqlite3.Error as e:
        logger.error(f"Error initializing database: {e}")
        raise

def get_last_5_items():
    """Get last 5 items from database."""
    try:
        db = get_db(DATABASE)
        cursor = db.execute('SELECT * FROM items ORDER BY id DESC LIMIT 5')
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    except sqlite3.Error as e:
        logger.error(f"Error fetching items: {e}")
        return []

# app main logic
@app.route('/')
def index():
    """Main page."""
    items = get_last_5_items()
    return render_template('index.html', items=items)

@app.route('/save_barcode', methods=['POST'])
def save_barcode():
    """Save barcode endpoint."""
    barcode = request.form.get('barcode', '').strip()
    tag = request.form.get('tag', '').strip()

    # Input validation
    if not barcode or not tag:
        flash('Barcode and tag are required!', 'error')
        return render_template('index.html', items=get_last_5_items())

    try:
        barcode_path = barcode_gen.make_barcode(barcode)
        logger.info(f"Generated barcode path: {barcode_path}")

        if barcode_path:
            if add_item(tag, f'{barcode_path}.svg'):
                flash('Changes saved successfully!', 'success')
                return render_template(
                    'index.html',
                    message="Changes saved successfully!",
                    barcode_path=f'{barcode_path}.svg',
                    items=get_last_5_items()
                )
            else:
                flash('Error saving to database!', 'error')
        else:
            flash('Barcode generation failed!', 'error')
    except Exception as e:
        logger.error(f"Error generating barcode: {e}")
        flash('Error generating barcode!', 'error')

    return render_template('index.html', items=get_last_5_items())

@app.route('/health')
def health():
    """Health check endpoint."""
    return {'status': 'healthy'}, 200

# Initialize database
init_db()

if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
