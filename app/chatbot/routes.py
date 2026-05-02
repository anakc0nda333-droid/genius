from flask import Blueprint, request, redirect, render_template, session, jsonify
from app.supabase_client import supabase
import requests


chatbot = Blueprint('chatbot', __name__)

##### ROUTE CHAT ###
@chatbot.route('/chat/<int:chatbot_id>')
def chat_page(chatbot_id):
    return render_template('chat.html', chatbot_id=chatbot_id)

##### LOGIC SEND MESSAGE & TERIMA MESSAGE #####
@chatbot.route('/send-message', methods=['POST'])
def send_message():
    data = request.json

    message = data.get('message')
    chatbot_id = data.get('chatbot_id')

    N8N_WEBHOOK = "https://anakcon.app.n8n.cloud/webhook/9c84e37f-d7f0-4862-9709-be08bc289d9c"

    response = requests.post(N8N_WEBHOOK, json={
        "message": message,
        "chatbot_id": chatbot_id
    })

    try:
        result = response.json()
    except:
        print("RAW RESPONSE:", response.text)
        result = {"reply": response.text}

    return jsonify({
        "reply": result.get("reply", "Tidak ada respon")
    })

##### LOGIC BUAT CHATBOT #####
@chatbot.route('/create-chatbot', methods=['GET', 'POST'])
def create_chatbot():
    user_id = session.get('user_id')

    if not user_id:
        return redirect('/auth/login')

    if request.method == 'GET':
        return render_template('create_chatbot.html') 

    # POST
    nama_chatbot = request.form.get('nama_chatbot')
    user_id = session.get('user_id')

    if not user_id:
        return redirect('/auth/login')

    res = supabase.table('chatbots').insert({
        "nama_chatbot": nama_chatbot,
        "user_id": user_id
    }).execute()

    if not res.data:
        return "Gagal membuat chatbot"

    chatbot_id = res.data[0]['chatbot_id']

    return redirect(f'/auth/create-chatbot-detail/{chatbot_id}')

##### LOGIC DETAIL BUAT CHATBOT #####
@chatbot.route('/create-chatbot-detail/<int:chatbot_id>', methods=['GET', 'POST'])
def create_chatbot_detail(chatbot_id):

    user_id = session.get('user_id')

    if not user_id:
        return redirect('/auth/login')
    
    if request.method == 'GET':
        return render_template('create_chatbot_detail.html', chatbot_id=chatbot_id)

    data = request.form
    file = request.files.get('file_knowledge')
    file_url = None

    if file and file.filename != "":
        file_path = f"{chatbot_id}/{file.filename}"

        supabase.storage.from_("chatbot-files").upload(
            file_path,
            file.read(),
            {"content-type": file.content_type}
        )

        file_url = supabase.storage.from_("chatbot-files").get_public_url(file_path)

    supabase.table('form_chatbot').insert({
        "id_chatbot": chatbot_id,
        "nama_usaha": data.get('nama_usaha'),
        "deskripsi_usaha": data.get('deskripsi_usaha'),
        "alur_usaha": data.get('alur_usaha'),
        "tujuan_chatbot": data.get('tujuan_chatbot'),
        "batasan_behavior": data.get('batasan_behavior'),
        "file_knowledge": file_url
    }).execute()

    
    webhook_url = "https://anakcon.app.n8n.cloud/webhook/53d52cb1-ba91-488e-ab49-ec2552705f7a"

    data_payload = {
            "chatbot_id": chatbot_id,
            "nama_usaha": data.get('nama_usaha'),
            "deskripsi_usaha": data.get('deskripsi_usaha'),
            "alur_usaha": data.get('alur_usaha'),
            "tujuan_chatbot": data.get('tujuan_chatbot'),
            "persona": data.get('persona'),
            "batasan_behavior": data.get('batasan_behavior'),
            "file_url": file_url
        }

    try:
            response = requests.post(
                webhook_url,
                data=data_payload
            )
            print("STATUS:", response.status_code)
            print("RESPONSE:", response.text)
    except Exception as e:
        print("ERROR N8N:", e)
        
    return redirect('/auth/dashboard')