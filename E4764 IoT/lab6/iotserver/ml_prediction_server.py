import socket, json, ast
from sklearn import svm
from sklearn.externals import joblib

print ("Server is starting" ) 
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('0.0.0.0', 8080))    
sock.listen(5)

while True:
    cl, addr = sock.accept()
    buf = cl.recv(4096)
    
    buf = ast.literal_eval(bytes.decode(buf))
    buf = buf.split(',')
    buf = buf[:-1]
    buf = [int(i) for i in buf]
    print(buf)
    

    clf = joblib.load("./random_forest_model.m")
    ans = clf.predict([buf])[0]
    print(ans.encode('utf-8'))
    cl.send(ans.encode('utf-8'))
    cl.close()

