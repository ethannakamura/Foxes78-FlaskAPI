# if using a run.py file for your shell context processor - change your FLASK_APP .env variable to run.py

from app import app
from app.models import db, Player

@app.shell_context_processor
def shell_context():
    return {'db': db, 'Player': Player}
