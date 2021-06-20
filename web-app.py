from flask import Flask,render_template,Response
import cv2

app =Flask(__name__)
camera=cv2.VideoCapture(0)

# reading camera frame
def gen_frames():
    while True:
        sucess,frame=camera.read()
        if not sucess:
            break
        else:
            ret,buffer=cv2.imencode('.jpg',frame)  # encoding frames in jpg formate

            frame=buffer.tobytes()   #converting buffer back to bytes

        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # act as return statement but loops   





@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video')
def video():
    return Response(gen_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__=="__main__":
    app.run(debug=True)



