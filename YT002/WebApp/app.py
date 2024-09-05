from flask import Flask, Response, render_template, request, redirect, url_for, session, flash, jsonify
from Systems.Camera import VideoStream
import sys, signal

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize VideoStream
video_stream = VideoStream(overlay_path='./Files/Crosshair.svg')

@app.route('/')
def home():
    return redirect(url_for('signin'))

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == 'admin' and password in ['secret', 'deadman', 'mykingdom', 'AliveAndWell']:
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('intrude.html')
    
    return render_template('signin.html')

@app.route('/camera_off', methods=['POST'])
def camera_off():
    video_stream.stop()  # Stop the video stream
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('signin'))
    return render_template('dashboard.html', username=session['user'])

@app.route('/signout', methods=['POST'])
def signout():
    session.pop('user', None)
    return redirect(url_for('signin'))

@app.route('/video_feed')
def video_feed():
    return Response(video_stream.generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/zoom_in', methods=['POST'])
def zoom_in():
    video_stream.set_zoom(video_stream.zoom_factor * 1.2)  # Increase zoom by 20%
    return jsonify({'zoom_factor': video_stream.zoom_factor})

@app.route('/zoom_out', methods=['POST'])
def zoom_out():
    video_stream.set_zoom(max(video_stream.zoom_factor / 1.2, 1.0))  # Decrease zoom by 20%, with minimum zoom factor of 1.0
    return jsonify({'zoom_factor': video_stream.zoom_factor})

@app.route('/battery', methods=['POST'])
def battery():
    # Add your battery-related functionality here
    return jsonify({'status': 'Battery function not implemented'})

@app.route('/gun', methods=['POST'])
def gun():
    # Add your gun-related functionality here
    return jsonify({'status': 'Gun function not implemented'})

@app.route('/fire', methods=['POST'])
def fire():
    # Add your fire-related functionality here
    return jsonify({'status': 'Fire function not implemented'})

@app.route('/light', methods=['POST'])
def light():
    # Add your light-related functionality here
    return jsonify({'status': 'Light function not implemented'})

def shutdown_server(signal, frame):
    sys.exit(0)

if __name__ == '__main__':
    app.run(debug=True)
