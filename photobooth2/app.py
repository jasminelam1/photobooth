from flask import Flask, request, render_template, Response, jsonify
from datetime import datetime
import cv2
import os
from rpi_camera import RPiCamera
from time import sleep
from imutils.video import VideoStream

app = Flask(__name__)

my_camera = None
current_frame = 0
my_effect = None

@app.route('/')
def index():
    print("welcome")
    return render_template("index.html")


#the generator, a special type of function that yields, instead of returns.
def gen(camera, effect):
    global current_frame, my_effect
    while True:
        
        """
         In this version we keep a separte jpg frame to capture before
         we convert to bytes.
        """
        if my_effect == b"gray":
            jpeg = cv2.imdecode(camera.get_frame(), cv2.IMREAD_COLOR)
            gray = cv2.cvtColor(jpeg, cv2.COLOR_BGR2GRAY)
            _,current_frame=cv2.imencode(".jpg", gray)
        elif my_effect == b"blur":
            jpeg = cv2.imdecode(camera.get_frame(), cv2.IMREAD_COLOR)
            blur = cv2.blur(jpeg,(5,5))
            _,current_frame=cv2.imencode(".jpg", blur)
        else:
            current_frame = camera.get_frame() 
        frame_to_stream =  current_frame.tobytes() 

        # Each frame is set as a jpg content type. Frame data is in bytes.
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_to_stream + b'\r\n')

@app.route('/filter', methods= ['POST', 'GET'])
def filter():
    global my_camera, my_effect
    my_effect = request.data
    print(my_effect)


    return jsonify(result={'status':200})
 #   feed = Response(gen(my_camera, 'cartoon'), mimetype='multipart/x-mixed-replace; boundary=frame')

 #   return feed
 #   global current_frame
 #   current_frame = camera.IMAGE_EFFECTS()
 #   for effect in current_frame:
 #       camera.image_effect = effect

@app.route('/capture', methods=['POST', 'GET'])
def capture():
    data = request.data
    
    now = datetime.now()
    date_time = now.strftime("%m-%d-%Y-%H:%M:%S")
    file_name = date_time + ".jpg"

    #image was encoded with cv2.encode, so we need to decode it. 
    jpeg = cv2.imdecode(current_frame, cv2.IMREAD_COLOR)

    #We will store pics in /captured_pics, found in the root folder.
    full_path = os.path.join(app.root_path, 'captured_pics', file_name)
    
    #Save the image
    cv2.imwrite(full_path , jpeg)
    
    #return full_path does nothing yet, but it could be use to display pic.
 
    return full_path

@app.route('/stream')
def stream():
    global my_camera, my_effect
    my_camera = RPiCamera()
    feed = Response(gen(my_camera, my_effect), mimetype='multipart/x-mixed-replace; boundary=frame')

    return feed

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True )