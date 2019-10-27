import socket, json, ast
from sklearn import svm
from sklearn.externals import joblib

print ("Server is starting" ) 
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('0.0.0.0', 8080))    
sock.listen(5)
letter =['C','O','L','U','M','B','I','A']
while True:
    
    cl, addr = sock.accept()

    try:    
        buf = cl.recv(4096)
        
        buf = ast.literal_eval(buf.decode('utf-8'))
        buf=list(buf)
        print(buf)
        '''
        buf = buf.split(',')
        buf = buf[:-1]
        print(buf)
        '''

        buf = [int(i) for i in buf]

        clf = joblib.load("./random_forest_model.m")
        ans = clf.predict([buf])[0]
        print(ans)
        ans= letter[ans]
        print(ans)
        cl.send(ans)
    except:
        pass
    cl.close()

