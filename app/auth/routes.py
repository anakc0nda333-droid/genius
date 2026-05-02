from flask import Blueprint, request, redirect
from app.supabase_client import supabase
from flask import render_template
from flask import redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template, session, redirect
from app.supabase_client import supabase
import requests
from flask import request, jsonify
import random
from datetime import datetime, timedelta
import smtplib
import os
from email.mime.text import MIMEText
import time
from app.utils.email import send_otp_email

auth = Blueprint('auth', __name__)

@auth.route('/')
# def auth_page():
#     return render_template('auth.html')

######## REGISTER #########
@auth.route('/register', methods=['GET'])
def register_page():
    return render_template('auth.html')


@auth.route('/register', methods=['POST'])
def register():

    print("STEP 1 MASUK")
    email = request.form.get('email')
    password = request.form.get('password')
    print("REGISTER KEHIT")
    otp = generate_otp()

    session['temp_user'] = {
        "email": email,
        "password": generate_password_hash(password),
        "otp": otp,
        "expired": time.time() + 300  # 5 menit
    }
    print("STEP 1")
    send_otp_email(email, otp)
    print("STEP 2")
    return redirect('/auth/verify')

##### OTP #####
def generate_otp():
    return str(random.randint(100000, 999999))
    
##### VERIFY OTP #####
@auth.route('/verify', methods=['GET', 'POST'])
def verify():
    if request.method == 'POST':
        input_otp = request.form.get('otp')
        temp_user = session.get('temp_user')

        if not temp_user:
            return redirect('/auth/register')

        # cek expired
        if time.time() > temp_user['expired']:
            return "Kode sudah kadaluarsa!"

        # cek OTP
        if input_otp != temp_user['otp']:
            return "Kode salah!"

        # simpan ke DB
        supabase.table("users").insert({
            "email": temp_user['email'],
            "password": temp_user['password'],
            "is_verified": True
        }).execute()

        session.pop('temp_user')
        return redirect('/auth/login')

    return render_template('verify.html')

@auth.route('/resend')
def resend():
    temp_user = session.get('temp_user')

    if not temp_user:
        return "Session expired"

    new_otp = generate_otp()
    temp_user['otp'] = new_otp

    send_otp_email(temp_user['email'], new_otp)

    return "OTP dikirim ulang"
    
####### LOGIN #######
@auth.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')
@auth.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    result = supabase.table("users") \
        .select("*") \
        .eq("email", email) \
        .execute()

    
    if result.data:
        user = result.data[0]
        if not user['is_verified']:
            return "Verifikasi dulu bro!"
        if check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            return redirect('/dashboard/home')
        else:
            return "Password salah!"

    return "User tidak ditemukan!"

##### LOGOUT #####
@auth.route('/logout')
def logout():
    session.clear()
    return redirect('/')