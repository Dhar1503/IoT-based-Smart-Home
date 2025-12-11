from flask import Flask, render_template, redirect, url_for, session
from models import db, User, Device
from api import api

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///smart_home.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secretkey'
db.init_app(app)
app.register_blueprint(api)

# ✅ Create initial data when app starts
with app.app_context():
    db.create_all()
    if not User.query.first():
        db.session.add(User(username='admin', password='admin123'))
        devices = [
            Device(name='Front Door Lock', device_type='lock', status='locked'),
            Device(name='Living Room Camera', device_type='camera', status='online'),
            Device(name='Motion Sensor', device_type='motion', status='active'),
            Device(name='Gas Sensor', device_type='gas', status='active')
        ]
        db.session.bulk_save_objects(devices)
        db.session.commit()

# ---------------- ROUTES ---------------- #

@app.route('/')
def home():
    # Always show login page first
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    # Restrict access if not logged in
    if 'user' not in session:
        return redirect('/')
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    # Clear session and go back to login
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
