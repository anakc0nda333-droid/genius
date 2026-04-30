from flask import Flask, render_template, session, redirect

# from flask_login import LoginManager
from dotenv import load_dotenv

# login_manager = LoginManager()

def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object('config.Config')

    # login_manager.init_app(app)
    # login_manager.login_view = 'auth.login'
    app.secret_key = 'secretkey123'
    # auth login & register
    
    @app.route('/')
    def landing_page():
        if session.get('user_id'):
            return redirect('/auth/dashboard')
        return render_template('landingpage.html')
    
    from app.auth.routes import auth
    app.register_blueprint(auth, url_prefix='/auth')
    
    # form
    from app.form.routes import form_bp
    app.register_blueprint(form_bp, url_prefix='/form')

    return app