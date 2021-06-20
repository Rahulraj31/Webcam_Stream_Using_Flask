# We will be using HassCasscade XML for face and Eye Detection

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
            detector=cv2.CascadeClassifier('haarcascades\haarcascade_frontalface_default.xml')
            eye_cascade =cv2.CascadeClassifier('haarcascades\haarcascade_eye.xml')
            faces=detector.detectMultiScale(frame,1.1,7)
            gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            
            #Draw rectangle around each face
            for(x,y,w,h) in faces:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)  #2500,0,0 is color code RGB means Red only
                roi_gray=gray[y:y+h,x:x+w]  #give rectangle face in grayscale for eye detection
                roi_color=frame[y:y+h,x:x+w]
                eyes=eye_cascade.detectMultiScale(roi_gray,1.1,3)  
                for(ex,ey,ew,eh) in eyes:
                    cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)


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



