from flask import Flask, render_template, session, redirect, url_for
from flask_cors import CORS
import os
from dotenv import load_dotenv

from routes.auth_routes import auth_bp
from routes.item_routes import item_bp
from routes.user_routes import user_bp
from routes.feedback_routes import feedback_bp


def create_app():
    # 🔥 Load environment variables
    load_dotenv()

    app = Flask(__name__)

    # 🔐 Secret Key
    app.secret_key = os.getenv("SECRET_KEY", "dev-secret")

    # 🌐 Enable CORS
    CORS(app, supports_credentials=True)

    # 🔥 Register API routes (Blueprints)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(item_bp, url_prefix='/items')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(feedback_bp, url_prefix='/feedback')  # ✅ FIXED

    # ===== FRONTEND ROUTES =====

    # 🏠 LANDING PAGE (PUBLIC)
    @app.route('/')
    def home():
        return render_template('index.html')

    # 🔐 AUTH PAGES
    @app.route('/login')
    def login():
        return render_template('login.html')

    @app.route('/register')
    def register():
        return render_template('register.html')

    # 🔒 DASHBOARD
    @app.route('/dashboard')
    def dashboard():
        if "user_id" not in session:
            return redirect(url_for("login"))
        return render_template('dashboard.html')

    # 🔒 PROFILE
    @app.route('/profile')
    def profile():
        if "user_id" not in session:
            return redirect(url_for("login"))
        return render_template('profile.html')

    # 🔒 REPORT FOUND
    @app.route('/report-found')
    def report_found():
        if "user_id" not in session:
            return redirect(url_for("login"))
        return render_template('report-found.html')

    # 🔒 REPORT LOST
    @app.route('/report-lost')
    def report_lost():
        if "user_id" not in session:
            return redirect(url_for("login"))
        return render_template('report-lost.html')

    # 🌐 PUBLIC
    @app.route('/search')
    def search():
        return render_template('search.html')

    @app.route('/view_items')
    def view_items():
        return render_template('view_items.html')

    # 🔒 EDIT ITEM
    @app.route('/edit-item')
    def edit_item():
        if "user_id" not in session:
            return redirect(url_for("login"))
        return render_template('edit-item.html')

    # 🌐 INFO PAGES
    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route('/contact')
    def contact():
        return render_template('contact.html')

    return app


# 🔥 REQUIRED FOR GUNICORN
app = create_app()


# ===== RUN LOCAL =====
if __name__ == "__main__":
    app.run(debug=True)