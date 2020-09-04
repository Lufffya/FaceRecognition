#
# Flask python web框架
#

import os
import cv2
import time
import json
from datetime import timedelta
#from werkzeug import SharedDataMiddleware
from werkzeug.utils import secure_filename
from Face_Recognition_Main import FaceRecognition
from flask import Flask,jsonify,render_template,request,redirect, url_for, make_response


app = Flask(__name__)#实例化app对象
 
app.send_file_max_age_default = timedelta(seconds=1)

testInfo = {}
 
@app.route('/test_post',methods=['GET','POST'])#路由
def test_post():
    testInfo['name'] = 'xiaoming'
    testInfo['age'] = '28'
    return json.dumps(testInfo)
 
@app.route('/')
def hello_world():
    return FaceRecognition.SayHello()

 
@app.route('/index')
def index():
    return render_template('index.html')
 

# @app.route('/upload_image',methods=['GET','POST'])
# def upload_image():
#     if request.method == 'POST':
       
#         file = request.files['file']

#         if not (file and allowed_file(file.filename)):
#             return jsonify({"status": 503, "msg": "请检查上传的图片类型，仅限于png、jpg、jpeg"})
     
#         upload_path = os.path.join('Upload_Images', secure_filename(file.filename))
#         file.save(upload_path)


#         img = cv2.imread(upload_path)
#         cv2.imwrite(os.path.join(basepath, 'static/images', 'test.jpg'), img)
#         #return jsonify({"status": 200, "savePath": file.filename})
#         return render_template('index.html',userinput=user_input,val1=time.time())

#     return jsonify({"status": 503, "msg": "找不到任何上传的文件"})


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload_image', methods=['POST', 'GET'])  # 添加路由
def upload_image():
    if request.method == 'POST':
        f = request.files['file']
 
        if not (f and allowed_file(f.filename)):
            return jsonify({"error": 503, "msg": "请检查上传的图片类型，仅限于png、jpg、jpeg"})
 
        showFileName = request.form.get("name")
 
        basepath = os.path.dirname(__file__)  # 当前文件所在路径
 
        upload_path = os.path.join(basepath, 'static/images', secure_filename(f.filename))
       
        f.save(upload_path)
 
        # 使用Opencv转换一下图片格式和名称
        img = cv2.imread(upload_path)
        cv2.imwrite(os.path.join(basepath, 'static/images', f.filename), img)
 
        showFileName = f.filename

        return render_template('show_Image.html',filePath="./images/"+showFileName,userinput=showFileName,val1=time.time(),height=img.shape[0],width=img.shape[1])
 
    return render_template('upload_Image.html')


@app.route("/Find_Face",methods=["GET","POST"])
def Find_Face():

    filePath = "undefind"

    try:
        fileName = request.values.get("fileName")

        filePath = FaceRecognition.Find_Face(fileName)

    except IndexError:
        return jsonify({"status": 503, "msg": "找不到任何人脸"})

    return jsonify({"status": 200,"filePath":filePath})


@app.route("/Face_Recognition",methods=["GET","POST"])
def Face_Recognition():
    try:
        fileName = request.values.get("fileName")
        print(fileName)
        personNames = FaceRecognition.Face_Recognition(fileName)

    except IndexError:
        return jsonify({"status": 503, "msg": "找不到任何人脸"})

    return jsonify({"status": 200,"Name":json.dumps(personNames,ensure_ascii=False)})
    

@app.route("/Gender_Recognition",methods=["GET","POST"])
def Gender_Recognition():
    try:
        fileName = request.values.get("fileName")

        personGender = FaceRecognition.Gender_Recognition(fileName)

    except IndexError:
        return jsonify({"status": 503, "msg": "找不到任何人脸"})

    return jsonify({"status": 200,"gender":json.dumps(personGender,ensure_ascii=False)})


if __name__ == '__main__':
    app.run(host='127.0.0.1',#任何ip都可以访问
            port=85,#端口
            # debug=True
            )
