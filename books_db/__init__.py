from flask import Flask

from .models import db
from .views import books_db

app = Flask(__name__)
app.config.from_object('config')


# Add the `constants` variable to all Jinja templates.
@app.context_processor
def provide_constants():
    return {"constants": {"TUTORIAL_PART": 1}}

db.init_app(app)

app.register_blueprint(books_db)