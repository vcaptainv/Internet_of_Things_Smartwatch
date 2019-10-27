import requests, json
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn.externals import joblib
import numpy
def get_list():
  url = 'http://127.0.0.1:8080/get'
  r = requests.get(url)
  co = json.loads(r.text)['result']

  big = []
  idx = 0
  small =[] # 20 lists  
  label = []
  print(len(co))
  while idx < len(co):
    l = co[idx]['label']
    label.append(l)
    for i in range(20):
      if idx > len(co)-1:
         break
      temp = []
      xco = co[idx]['xcoordinate']
      yco = co[idx]['ycoordinate']
      temp.append(xco)
      temp.append(yco)
      small.append(temp)
      idx += 1
      #print(idx)

  
    big.append(small)
    small = []
    #print('--------')
  
  
  #print("-------------------")
  print(big)
  print(len(big))
  return big,label

def train_model(train, label):
    clf =RandomForestClassifier(n_estimators = 100)
    #clf = svm.SVC(gamma='scale', decision_function_shape='ovo')
    clf.fit(train,label)
    joblib.dump(clf,"random_forest_model.m")

if __name__ == "__main__":
    train , label = get_list()
    train = numpy.array([x for x in train])
    nsamples, nx, ny = train.shape
    train = train.reshape((nsamples,nx*ny))
    print(train)
    train_model(train, label)
