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
    
    from app.auth.routes import auth
    from app.dashboard.routes import dashboard
    from app.chatbot.routes import chatbot
    
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(dashboard, url_prefix='/dashboard')
    app.register_blueprint(chatbot, url_prefix='/chatbot')
    
    @app.route('/')
    def landing_page():
        if session.get('user_id'):
            return redirect('/dashboard/dashboard')
        return render_template('landingpage.html')
    

    return app