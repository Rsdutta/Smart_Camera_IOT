from flask import Flask, render_template, Response, request, session

from smart_camera import smart_camera

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_processed_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(smart_camera(session['cam1_val'], 0)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/video_feed2')
def video_feed2():
    return Response(gen(smart_camera(session['cam2_val'], 2)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/stream', methods=['GET', 'POST'])
def test():
    session['cam1_val'] = request.form['cam1']
    session['cam2_val'] = request.form['cam2']
    print session['cam1_val'], session['cam2_val']
    return render_template('video.html')

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.run(host='0.0.0.0', port =80, debug=True, threaded=True)