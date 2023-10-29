from flask import Flask
from views import views
from src.libstreak.database.importer import import_data

app = Flask(__name__)
app.register_blueprint(views, url_prefix="/taknikiyaat/")


if __name__ == "__main__":
    """
    installed:
        flask
        beautifulsoup4
        requests
    """
    import_data()  # TEST commit
    app.run(debug=False, port=8000)
