from flask import Flask, render_template, request, redirect, url_for, flash, send_file, abort
from werkzeug.utils import secure_filename
from config import Config
from models import db, Upload
import io

class FileUploadApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config.from_object(Config)
        
        db.init_app(self.app)
        self.register_routes()
    
    def register_routes(self):
        @self.app.route('/', methods=['GET', 'POST'])
        def index():
            if request.method == 'POST':
                if 'file' not in request.files:
                    flash('No file part')
                    return redirect(request.url)
                    
                file = request.files['file']
                password = request.form.get('password')
                
                if file.filename == '':
                    flash('No selected file')
                    return redirect(request.url)
                    
                if not password:
                    flash('Password is required')
                    return redirect(request.url)
                
                if file:
                    filename = secure_filename(file.filename)
                    file_data = file.read()
                    
                    upload = Upload.create(filename, file_data, password)
                    
                    db.session.add(upload)
                    db.session.commit()
                    
                    file_url = url_for('get_file', uuid=upload.uuid, _external=True)
                    return render_template('success.html', file_url=file_url)
            
            return render_template('index.html')
        
        @self.app.route('/get-file/<uuid>', methods=['GET', 'POST'])
        def get_file(uuid):
            if request.method == 'POST':
                password = request.form.get('password')
                
                if not password:
                    flash('Password is required')
                    return redirect(url_for('get_file', uuid=uuid))
                
                upload = Upload.query.filter_by(uuid=uuid).first()
                
                if not upload:
                    abort(404)
                    
                if upload.check_password(password):
                    return send_file(
                        io.BytesIO(upload.file_data),
                        download_name=upload.filename,
                        as_attachment=True
                    )
                else:
                    flash('Incorrect password')
                    return redirect(url_for('get_file', uuid=uuid))
            
            upload = Upload.query.filter_by(uuid=uuid).first()
            if not upload:
                abort(404)
            
            return render_template('get_file.html', uuid=uuid)
    
    def create_tables(self):
        with self.app.app_context():
            db.create_all()
    
    def run(self, debug=True):
        self.app.run(debug=debug)

if __name__ == '__main__':
    app = FileUploadApp()
    app.create_tables()
    app.run()