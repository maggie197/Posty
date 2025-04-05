from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Configuring the secret key for form handling
app.config['SECRET_KEY'] = 'your_secret_key_here'

# Configure the upload folder and allowed extensions
app.config['UPLOADED_PHOTOS_DEST'] = 'static/uploads'

# Make sure the uploads folder exists
os.makedirs(app.config['UPLOADED_PHOTOS_DEST'], exist_ok=True)

# This will hold the list of image filenames and comments
gallery = []

@app.route('/')
def index():
    return render_template('index.html', gallery=gallery)

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' in request.files:
        image = request.files['image']
        filename = secure_filename(image.filename)
        # Save the file to the uploads folder
        image.save(os.path.join(app.config['UPLOADED_PHOTOS_DEST'], filename))
        gallery.append({'filename': filename, 'comments': []})
    return redirect(url_for('index'))

@app.route('/comment/<int:image_id>', methods=['POST'])
def add_comment(image_id):
    comment = request.form['comment']
    if 0 <= image_id < len(gallery):
        gallery[image_id]['comments'].append(comment)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
