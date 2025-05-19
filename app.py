import os
from flask import (Flask, render_template, redirect, url_for, request, flash, send_from_directory, abort)
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Gallery, Photo, Comment

# App Initialization
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['UPLOAD_FOLDER'] = 'uploads'    # !!! new
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Upload folder 

UPLOAD_FOLDER = 'uploads' 

# Database Initialization
db.init_app(app)
with app.app_context():
    db.create_all()

# Login Manager Setup
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Helpers
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
#!!! new
from pathlib import Path
import uuid

def save_photo(file_storage_obj, gallery):
    """Save the uploaded file in uploads/<user>/<gallery>/ and return filename"""
    root = Path(app.config['UPLOAD_FOLDER'])
    gpath = root / str(gallery.user_id) / str(gallery.id)
    gpath.mkdir(parents=True, exist_ok=True)

    ext = Path(file_storage_obj.filename).suffix.lower()
    filename = f"{uuid.uuid4().hex}{ext}"
    file_storage_obj.save(gpath / filename)
    return filename
# !!!!

# Routes
@app.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if not user:
            flash('Account isn’t registered.', 'error')
            return redirect(url_for('login'))

        if not check_password_hash(user.password, password):
            flash('Incorrect password.', 'error')
            return redirect(url_for('login'))

        login_user(user)
        flash(f'Welcome, {user.username}!', 'success')
        return redirect(url_for('index'))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'error')
            return redirect(url_for('register'))

        new_user = User(
            username=username,
            password=generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        )
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        flash(f'Welcome, {new_user.username}!', 'success')
        return redirect(url_for('index'))

    return render_template('register.html')

@app.route('/index')
@login_required
def index():
    galleries = current_user.galleries  # fetch logged-in user’s galleries
    return render_template('index.html', galleries=galleries)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/display/<filename>')
def display_file(filename):
    return render_template('upload.html', filename=filename)

@app.route('/upload', methods=['GET', 'POST'])  # check if needs deletion
@login_required
def upload_file():
    if request.method == 'POST':
        file = request.files.get('file')

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            flash('File uploaded successfully!', 'success')
            return redirect(url_for('display_file', filename=filename))
        else:
            flash('Invalid file type.', 'error')
            return redirect(url_for('upload_file'))

    return render_template('upload.html')  # create an upload.html form
# !!! new 
@app.route('/galleries', methods=['POST'])
@login_required
def new_gallery():
    name = request.form.get('name', '').strip()
    if not name:
        flash('Gallery name required', 'error')
        return redirect(url_for('index'))

    g = Gallery(name=name, user=current_user)
    db.session.add(g); db.session.commit()
    flash('Gallery created!', 'success')
    return redirect(url_for('view_gallery', id=g.id))

@app.route('/galleries/<int:id>')
@login_required
def view_gallery(id):
    gallery = Gallery.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    return render_template('gallery_view.html', gallery=gallery, photos=gallery.photos)

@app.route('/galleries/<int:id>/photos', methods=['POST'])
@login_required
def upload_to_gallery(id):
    gallery = Gallery.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    file = request.files.get('file')
    if not (file and allowed_file(file.filename)):
        flash('Invalid file', 'error')
        return redirect(url_for('view_gallery', id=id))

    filename = save_photo(file, gallery)
    photo = Photo(filename=filename, gallery=gallery)
    db.session.add(photo); db.session.commit()
    flash('Photo uploaded!', 'success')
    return redirect(url_for('view_gallery', id=id))

@app.route('/uploads/<int:user_id>/<int:gallery_id>/<filename>')
@login_required
def uploaded_file(user_id, gallery_id, filename):
    if user_id != current_user.id:
        abort(403)
    directory = os.path.join(app.config['UPLOAD_FOLDER'], str(user_id), str(gallery_id))
    return send_from_directory(directory, filename)


# !! 
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Main
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)

