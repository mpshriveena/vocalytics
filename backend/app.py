#<--------------------------imports------------------------------------>
from flask import Flask, request, jsonify,make_response, session
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies
from functools import wraps
from flask_cors import CORS
from datetime import timedelta,datetime
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, roles_required
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import os
from flask import send_from_directory
from sqlalchemy.ext.hybrid import hybrid_property
import logging
import speech_recognition as sr
import io
import wave
from pydub import AudioSegment
import whisper
import soundfile as sf
import torch
import numpy as np
import subprocess
import re
from collections import Counter
import nltk
from nltk.util import ngrams
from nltk.tokenize import word_tokenize
import spacy
from sqlalchemy import func, desc

nlp = spacy.load('en_core_web_sm')

db = SQLAlchemy()

#<-------------------------------------models----------------------------------------->

roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }


class User(db.Model):
    __tablename__ = 'user' 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=False)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String(255))
    registered_at = db.Column(db.DateTime())
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    role = db.relationship('Role', backref=db.backref('users', lazy=True))
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role.to_dict() if self.role else None,
            'last_login_at': self.last_login_at,
            'current_login_at': self.current_login_at,
            'registered_at': self.registered_at,
        }
    
class Transcriptions(db.Model):
    __tablename__ = 'transciptions' 
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    transcription = db.Column(db.String)
    language = db.Column(db.String)
    date_created = db.Column(db.DateTime())

class Frequency(db.Model):
    __tablename__ = 'frequency' 
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    word = db.Column(db.String)
    frequency = db.Column(db.Integer)

app = Flask(__name__)

CORS(app, origins='*')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vocalyticsdb.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.config['SECRET_KEY'] = 'secretkey'
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_PASSWORD_SALT'] = 'somesalt'
app.config['SECURITY_PASSWORD_HASH'] = 'bcrypt'

datastore = SQLAlchemyUserDatastore(db, User, Role)


app.config['JWT_SECRET_KEY'] = 'my-secret-key'
jwt = JWTManager(app)

def roles_required(*roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            identity = get_jwt_identity()
            if not isinstance(identity, dict):
                return jsonify({"message": "Invalid identity format"}), 401
            
            
            if identity.get('role') not in roles:
                return jsonify({"message": "Access forbidden: insufficient role"}), 403
            
            response = fn(*args, **kwargs)
    
            
            return response
        return wrapper
    return decorator

@app.before_request
def before_request_func():
    if request.method == 'OPTIONS':
        return build_cors_preflight_response()

def build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "http://localhost:5173")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE,OPTIONS")
    return response

db.init_app(app)

device = 'cuda' if torch.cuda.is_available() else 'cpu'
model = whisper.load_model("medium", device=device)
model_names = whisper.available_models()
print(f"Available models:", model_names)

#<-----------------------------------APIs---------------------------------------------------->

@app.route('/register', methods=['POST'])
def register():
    data =  request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    if not username:
        return jsonify({"message":"Username not provided"}), 400
    if not email:
        return jsonify({"message":"Email not provided"}), 400
    if not password:
        return jsonify({"message":"Password not provided"}), 400
    password = generate_password_hash(password)
    role_name = data.get('role')  

  
    role = Role.query.filter_by(name=role_name).first() 
    registered_at=datetime.now()
    new_user = User(username=username,email=email,password=password,role=role,registered_at=registered_at)
    
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    user = User.query.filter_by(email=email).first()
    if not email:
        return jsonify({"message":"Email not provided"}), 400
    if not data.get("password"):
        return jsonify({"message":"Password not provided"}), 400   
    if not user:
        return jsonify({"message":"User not found"}), 404
    if check_password_hash(user.password, data.get("password")): 
        user.last_login_at=user.current_login_at
        user.current_login_at=datetime.now()
        db.session.commit()

        access_token = create_access_token(identity={"role": user.role.name}, expires_delta = timedelta(days=1))
        user_info = {
            'user_id' : user.id,
            'username' : user.username,
            'role' :user.role.to_dict(),
            'email' : user.email,
        }
        return jsonify({'access_token':access_token, 'user': user_info}), 200   
    else:
        return jsonify({"message":"Wrong Password"}), 400

@app.route('/transcribe', methods=['POST'])
@jwt_required()
@roles_required('user')
def transcribe():
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        if not os.path.exists('uploads'):
            os.makedirs('uploads')
        audio_file = request.files['audio']
        user_id = request.form.get('user_id')
        print(f"user_id:",user_id)
        file_path = os.path.join('uploads', audio_file.filename)
        audio_file.save(file_path)
        result = subprocess.run(['whisper', file_path, '--task', 'translate'], capture_output=True, text=True)
        os.remove(file_path)
        language_match = re.search(r'Detected language: (\w+)', result.stdout)
        detected_language = language_match.group(1) if language_match else 'Unknown'
        transcription_lines = re.findall(r'\[.*?\] (.+)', result.stdout)
        transcription = ' '.join(transcription_lines)
        new_transcription = Transcriptions(user_id=user_id,transcription=transcription,language=detected_language,date_created=datetime.now())
        db.session.add(new_transcription)
        db.session.commit()
        return jsonify({'transcription': transcription, 'detected_language':detected_language})

    except Exception as e:
        return str(e), 500
    
@app.route('/test-transcribe', methods=['POST'])
@jwt_required()
@roles_required('admin')
def test_transcribe():
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        if not os.path.exists('uploads'):
            os.makedirs('uploads')
        audio_file = request.files['audio']
        user_id = request.form.get('user_id')
        print(f"user_id:",user_id)
        file_path = os.path.join('uploads', audio_file.filename)
        audio_file.save(file_path)
        result = subprocess.run(['whisper', file_path, '--task', 'translate'], capture_output=True, text=True)
        os.remove(file_path)
        language_match = re.search(r'Detected language: (\w+)', result.stdout)
        detected_language = language_match.group(1) if language_match else 'Unknown'
        transcription_lines = re.findall(r'\[.*?\] (.+)', result.stdout)
        transcription = ' '.join(transcription_lines)
        return jsonify({'transcription': transcription, 'detected_language':detected_language})

    except Exception as e:
        return str(e), 500

@app.route('/mytranscriptions/', methods=['GET'])
@jwt_required()
@roles_required('user')
def get_mytranscriptions():
    user_id = request.args.get('user_id')
    print(f"User_id:",user_id)
    if user_id is None:
        return jsonify({"message": "user_id parameter is required"}), 400

    mytranscriptions = db.session.query(Transcriptions).filter(Transcriptions.user_id == user_id).all()
    if not mytranscriptions:
        return jsonify({"message": "No transcriptions found for this user"}), 404
    mytranscription_list = [{'id': mytranscription.id, 'transcription': mytranscription.transcription, 'detected_language': mytranscription.language, 'date_created': mytranscription.date_created} for mytranscription in mytranscriptions]
    return jsonify({'mytranscriptions': mytranscription_list})

@app.route('/transcriptions/', methods=['GET'])
@jwt_required()
@roles_required('admin')
def get_transcriptions():
    transcriptions = db.session.query(Transcriptions).all()
    if not transcriptions:
        return jsonify({"message": "No transcriptions found"}), 404
    transcription_list = [{'id': transcription.id,'user_id': transcription.user_id, 'transcription': transcription.transcription, 'detected_language': transcription.language, 'date_created': transcription.date_created} for transcription in transcriptions]
    return jsonify({'transcriptions': transcription_list})

@app.route('/frequent-words', methods=['GET'])
def frequent_words():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "user_id parameter is required"}), 400
    transcriptions = db.session.query(Transcriptions).filter(Transcriptions.user_id == user_id).all()
    words = ' '.join([transcription.transcription for transcription in transcriptions]).split()
    word_counts = Counter(words)
    most_common_words = word_counts.most_common(10)
    return jsonify({'most_frequent_words': most_common_words}), 200

@app.route('/all-users-frequent-words', methods=['GET'])
def all_users_frequent_words():
    transcriptions = db.session.query(Transcriptions).all()
    words = ' '.join([transcription.transcription for transcription in transcriptions]).split()
    word_counts = Counter(words)
    most_common_words = word_counts.most_common(10)
    return jsonify({'all_users_frequent_words': most_common_words}), 200

@app.route('/top-phrases', methods=['GET'])
def get_top_phrases():
    user_id = request.args.get('user_id')
    if user_id is None:
        return jsonify({"message": "user_id parameter is required"}), 400
    transcriptions = db.session.query(Transcriptions).filter(Transcriptions.user_id == user_id).all()
    if not transcriptions:
        return jsonify({"message": "No transcriptions found for this user"}), 404
    text = " ".join(t.transcription for t in transcriptions)
    doc = nlp(text)
    tokens = [token.text for token in doc if not token.is_punct and not token.is_stop]
    n = 3  
    phrases = ngrams(tokens, n)
    phrase_freq = Counter([' '.join(phrase) for phrase in phrases])
    top_phrases = phrase_freq.most_common(3)  # Top 3 unique phrases
    return jsonify({'top_phrases': top_phrases}), 200

@app.route('/top-phrasesa', methods=['GET'])
def get_top_phrasesa():
    user_id = request.args.get('user_id')
    if user_id is None:
        return jsonify({"message": "user_id parameter is required"}), 400
    transcriptions = db.session.query(Transcriptions).all()
    if not transcriptions:
        return jsonify({"message": "No transcriptions found for this user"}), 404
    text = " ".join(t.transcription for t in transcriptions)
    doc = nlp(text)
    tokens = [token.text for token in doc if not token.is_punct and not token.is_stop]
    n = 3  
    phrases = ngrams(tokens, n)
    phrase_freq = Counter([' '.join(phrase) for phrase in phrases])
    top_phrases = phrase_freq.most_common(3)  # Top 3 unique phrases
    return jsonify({'top_phrases': top_phrases}), 200

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        data = request.get_json()
        field = data.get('field')
        search = data.get('search')
        user_id = data.get('user_id')
        if field == 'transcription':
            transcriptions = Transcriptions.query.filter(
                Transcriptions.transcription.like('%' + search + '%')
                                ).filter(
                Transcriptions.user_id == user_id
                ).all()
            if not transcriptions:
                return jsonify({'field': field, 'search': search,'transcriptions': []})
            transcription_list = [{'id': transcription.id,'transcription': transcription.transcription, 'detected_language': transcription.language, 'date_created': transcription.date_created} for transcription in transcriptions]
            return jsonify({'field': field, 'search': search,'transcriptions': transcription_list})
        if field == 'language':
            transcriptions = Transcriptions.query.filter(
                Transcriptions.language.like('%' + search + '%')
                                ).filter(
                Transcriptions.user_id == user_id
                ).all()
            if not transcriptions:
                return jsonify({'field': field, 'search': search,'transcriptions': []})
            transcription_list = [{'id': transcription.id,'transcription': transcription.transcription, 'detected_language': transcription.language, 'date_created': transcription.date_created} for transcription in transcriptions]
            return jsonify({'field': field, 'search': search,'transcriptions': transcription_list})
    elif request.method == 'GET':
        search_results = session.get('search_results')
        if search_results:
            return jsonify(search_results)
        return jsonify({'field': field, 'search': search,'transcriptions': []})

@app.route('/top-users', methods=['GET'])
def get_top_users():
    user_role = Role.query.filter_by(name='user').first()
    users = User.query.filter_by(role_id=user_role.id).all()
    user_transcriptions = []
    for user in users:
        transcription_count = Transcriptions.query.filter_by(user_id=user.id).count()
        user_transcriptions.append({
            'username': user.username,
            'transcription_count': transcription_count
        })
    top_users = sorted(user_transcriptions, key=lambda x: x['transcription_count'], reverse=True)[:10]
    return jsonify({'top_users':top_users})

@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    response = jsonify({'message':'Logged out successfully'})
    unset_jwt_cookies(response)
    return response,200

with app.app_context():
    db.create_all()

#<----------------------Creating Roles and Admin------------------------------------>

    datastore.find_or_create_role(name="admin")
    datastore.find_or_create_role(name="user")
    db.session.commit()
    if not User.query.filter_by(username="admin").first():
        admin = User(
                username="admin",
                email="21f3001238@ds.study.iitm.ac.in",
                password=generate_password_hash('admin'),
                role = Role.query.filter_by(name='admin').first(),
                registered_at = datetime.now(),
            )
        db.session.add(admin)
        db.session.commit()

if __name__ == '__main__':
    app.run(debug = True)

#<-----------------------------Completed------------------------------------->
