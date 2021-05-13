import json
import os
import json
from datetime import datetime
import time


# application settings



def transformData(data:dict):
  newdata = []
  l = 0
  keysOfData = list(data.keys())
  for i in data:
    if not data[i]['countReacheable'] == 0:
      succRate = round(data[i]['countReacheable']/data[i]['countTotal']*100, 1)
    else:
      succRate = 0
    newdata.append({
      'ip':keysOfData[l],
      'succ':data[i]['countReacheable'],
      'unsucc':data[i]['countUnreacheable'],
      'total':data[i]['countTotal'],
      'LastAttempt':data[i]['LastAttempt'],
      'succRate':succRate
    })
    l+=1
  return newdata


def writeToFile(data:dict):
  newdata = transformData(data)
  newdataoutput = str(newdata)
  with open("/output/out.html", "w") as f:
      page = '''<!DOCTYPE html>
      <html>
      <head>
      <meta http-equiv="refresh" content="10">
        <link href="https://fonts.googleapis.com/css?family=Roboto:100,300,400,500,700,900" rel="stylesheet">
        <link href="https://cdn.jsdelivr.net/npm/@mdi/font@4.x/css/materialdesignicons.min.css" rel="stylesheet">
        <link href="https://cdn.jsdelivr.net/npm/vuetify@2.x/dist/vuetify.min.css" rel="stylesheet">
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, minimal-ui">
      </head>
      <body>
      <h1>Network Monitoring Tool</h1>
        <div id="app">
          <v-app>
            <v-main>
      <template>
        <v-data-table
          :headers="headers"
          :items="pings"
          :items-per-page="5"
          class="elevation-1"
          :hide-default-footer="true"
        ></v-data-table>
      </template>
            </v-main>
          </v-app>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/vue@2.x/dist/vue.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/vuetify@2.x/dist/vuetify.js"></script>
          <script>
          new Vue({
            el: '#app',
            vuetify: new Vuetify(),
            data: {
              headers: [
                {
                  align: 'start',
                  sortable: false,
                  value: 'name',
                  
                },
                { text: 'Ip addres', value: 'ip' },
                { text: 'End point is reachable', value: 'succ' },
                { text: 'End point is not reachable', value: 'unsucc' },
                { text: 'timestamp', value: 'LastAttempt' },
                { text: 'Failure rate (%)', value: 'succRate' },
                { text: 'Number of pings', value: 'total' },
              ],
              pings:'''+ newdataoutput +'''
            }
          },
      )
        </script>
            </body>
            </html>'''
     
      f.write(page)


def getTimeNow():
  now = datetime.now().strftime("%Y/%m/%d/ %H:%M:%S")
  return now


def main():
  with open('input.json') as f:
    data = json.load(f)

    dataIp={
      'countReacheable'   : 0,
      'countUnreacheable' : 0,
      'countTotal'        : 0,
      'LastAttempt'       : 0,
      }
    outputstatus= {} 


  while(True):
    for i in data['ipAddress']:
      r = os.system('ping -c 1 ' + i )
      if not outputstatus.get(i):
        outputstatus[i] = {}
      if not outputstatus[i].get('countTotal'):
        outputstatus[i] = {
                          'countReacheable'   : 0,
                          'countUnreacheable' : 0,
                          'countTotal'        : 0,
                          'LastAttempt'       : 0,
                          }
      outputstatus[i]['countTotal'] +=1
      outputstatus[i]['LastAttempt'] = getTimeNow()
      if r ==0 :
        outputstatus[i]['countReacheable'] +=1
      else:
        outputstatus[i]['countUnreacheable'] +=1
    # print(outputstatus)
    writeToFile(outputstatus)
    time.sleep(10)    




if __name__ == "__main__":
    main()