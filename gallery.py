# routes/gallery.py
from flask import Blueprint, request, redirect, url_for, render_template
from flask_login import login_required, current_user

from app import db                     
from app.models import Gallery         

gallery_bp = Blueprint('gallery', __name__, url_prefix='')

@gallery_bp.route('/galleries', methods=['GET', 'POST'])
@login_required
def galleries():
    if request.method == 'POST':
        name = request.form['name'].strip()
        g = Gallery(name=name, user=current_user)
        db.session.add(g)
        db.session.commit()
        return redirect(url_for('gallery.view_gallery', id=g.id))

    # GET → list this user’s galleries
    galleries = current_user.galleries
    return render_template(
        'galleries/index.html',
        galleries=galleries
    )

# routes/gallery.py (or wherever you define routes)
from flask import abort, send_from_directory, current_app
from flask_login import login_required, current_user
from pathlib import Path

@app.route("/uploads/<int:user_id>/<int:gallery_id>/<filename>")
@login_required
def uploaded_file(user_id, gallery_id, filename):
    if user_id != current_user.id:
        abort(403)

    UPLOAD_ROOT = Path(current_app.config.get("UPLOAD_FOLDER", "uploads"))
    directory = UPLOAD_ROOT / str(user_id) / str(gallery_id)
    return send_from_directory(directory, filename)

from app.utils import save_photo

@gallery_bp.route('/galleries/<int:gallery_id>/photos', methods=['POST'])
@login_required
def upload_photo(gallery_id):
    gallery = Gallery.query.filter_by(id=gallery_id, user_id=current_user.id).first_or_404()
    
    file = request.files.get('photo')
    if not file:
        # handle missing file error
    
    filename = save_photo(file, gallery)
    
    photo = Photo(filename=filename, gallery=gallery)
    db.session.add(photo)
    db.session.commit()
    
    return redirect(url_for('gallery.view_gallery', id=gallery.id))
