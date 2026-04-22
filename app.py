from flask import Flask, render_template
from flask_cors import CORS
import os
from dotenv import load_dotenv

from routes.auth_routes import auth_bp
from routes.item_routes import item_bp
from routes.user_routes import user_bp


def create_app():
    # Load environment variables
    load_dotenv()

    app = Flask(__name__)

    # 🔐 Secret Key (IMPORTANT)
    app.secret_key = os.getenv("SECRET_KEY")

    CORS(app)

    # 🔥 Register API routes
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(item_bp, url_prefix='/items')
    app.register_blueprint(user_bp, url_prefix='/user')

    # 🔥 Page Routes (Frontend)

    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/login')
    def login():
        return render_template('login.html')

    @app.route('/register')
    def register():
        return render_template('register.html')

    @app.route('/dashboard')
    def dashboard():
        return render_template('dashboard.html')

    @app.route('/report-found')
    def report_found():
        return render_template('report-found.html')

    @app.route('/report-lost')
    def report_lost():
        return render_template('report-lost.html')

    @app.route('/search')
    def search():
        return render_template('search.html')

    @app.route('/view_items')
    def view_items():
        return render_template('view_items.html')

    @app.route('/edit-item')
    def edit_item():
        return render_template('edit-items.html')

    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route('/contact')
    def contact():
        return render_template('contact.html')

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)