import requests, json

def get_list():
  url = 'http://18.218.34.7:8080/get'
  r = requests.get(url)
  co = json.loads(r.text)['result']

  rst = []
  cur = []
  idx = 0


  while idx < len(co):
      temp = []
      xco = co[idx]['xcoordinate']
      yco = co[idx]['ycoordinate']
      temp.append(xco)
      temp.append(yco)
      cur.append(temp)
      idx += 1



  rst.append(cur)
  print("-------------------")
  print(rst)
  print(len(rst))

get_list()
