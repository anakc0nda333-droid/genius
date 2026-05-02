from flask import Blueprint, render_template, session, redirect
from app.supabase_client import supabase

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/home')
def home():
    user_id = session.get('user_id')

    if not user_id:
        return redirect('/auth/login')

    user = supabase.table('users')\
        .select('*')\
        .eq('id', user_id)\
        .execute().data[0]

    return render_template('landing_after_login.html', user=user)


@dashboard.route('/dashboard')
def dashboard_page():
    user_id = session.get('user_id')

    if not user_id:
        return redirect('/auth/login')
    user_res = supabase.table('users')\
        .select('*')\
        .eq('id', user_id)\
        .execute()

    user = user_res.data[0] if user_res.data else None

    response = supabase.table('chatbots')\
        .select('*')\
        .eq('user_id', user_id)\
        .execute()

    return render_template(
        'dashboard.html',
        chatbots=response.data,
        user=user
    )