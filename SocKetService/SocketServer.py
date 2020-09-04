#!/bin/python
#-*- coding: UTF-8 -*-
#文件名：server.py
 
import socket   #导入socket模块
import re
from multiprocessing import Process #导入进程模块

 
#设置静态文件根目录
HTML_ROOT_DIR='./html'


def handle_client(client_socket):
    """处理客户端连接请求"""
    request_data=client_socket.recv(1024)
    print(request_data)
    request_lines=request_data.splitlines()
    for line in request_lines:
        print(line)
    #'GET / HTTP/1.1'
    request_start_line=request_lines[0].decode("utf-8")
 
    print("*"*10)
    print(request_start_line)
 
    #提取用户请求的文件名
    #file_name=re.match(r"\w+ +(/[^ ]*) ",str(request_start_line)).group(1)
    #if "/" == file_name:
    #file_name='/index.html'
    
    #打开文件，读取内容
    try:
        file=open("index.html","rb")

    except IOError:
        response_start_line="HTTP/1.1 404 Not Found\r\n"
        response_heads="Server: My server\r\n"
        response_body="The file not found!"
    else:
        file_data=file.read()
        file.close()
 
        response_start_line="HTTP/1.1 200 ok\r\n"
        response_heads="Server: My server\r\n"
        response_body=file_data.decode("utf-8")
    response=response_start_line+response_heads+"\r\n"+response_body
    print("response data:",response)
    client_socket.send(bytes(response,"utf-8"))
    client_socket.close()
 
if __name__=="__main__":         #如果直接运行本文件，那么__name__为__main__(此时才运行下面的程序)，否则为对应包名
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  # 创建socket对象
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    #host = socket.gethostname()  # 获取本地主机名
    port = 9527  #
    #print(host)
    s.bind(("", port))  # 绑定端口
    s.listen(5)
 
    while True:
        c,addr=s.accept()   #建立客户端连接
        print('连接地址',addr)
        handle_client_process=Process(target=handle_client,args=(c,))   #ALT+ENTER快捷键生成函数
        handle_client_process.start()
        c.close()




# @app.route('/up_photo', methods=['POST'], strict_slashes=False)
# def api_upload():
#     file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
#     if not os.path.exists(file_dir):
#         os.makedirs(file_dir)
#     f = request.files['photo']
#     if f and allowed_file(f.filename):
#         fname = secure_filename(f.filename)
#         ext = fname.rsplit('.', 1)[1]
#         new_filename = Pic_str().create_uuid() + '.' + ext
#         print new_filename
#         f.save(os.path.join(file_dir, new_filename))
#         img_url = ip+'show/'+new_filename
#         img_url_new = ip+'show/'+new_filename  #处理后的图片，假数据
 
#         return jsonify({"success": 200, "msg": "上传成功", "img_url": img_url, "img_url_new": img_url_new})
#     else:
#         return jsonify({"error": 1001, "msg": "上传失败"})