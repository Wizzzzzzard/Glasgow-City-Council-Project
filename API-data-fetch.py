import http.client, urllib.request, urllib.parse, urllib.error, base64, pandas as pd
from io import BytesIO
import time

#page_num = 2
page_num = 30

headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': '62f8d7952d654af6b59958605b79a001',
}

params = urllib.parse.urlencode({
})

for i in range(0,page_num):
    try:
        conn = http.client.HTTPSConnection('gcc.azure-api.net')
        conn.request("GET", "/traffic/v1/movement/now?page={}&format=csv&%s".format(i) % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        #print(data)
        df1 = pd.read_csv(BytesIO(data))
        if i == 0:
            df = df1
        else:
            df = df.append(df1)
        df.to_csv('link_positions.csv')
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

df.columns = ['latitude', 'longitude', 'flow', 'concentration', 'site', 'lastupdateutc', 'lastupdate', 'timestamp']
#df = df.set_index('index')
df.to_csv('link_positions.csv')
print(df.site.unique())
print(df)
