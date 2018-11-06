import json
import pandas as pd

# Load data into a pandas data frame
with open('geant.dat') as f:
    l = json.load(f)
    info = []
    for d in l:
        x = d['data']
        info.append({'eventID':d['eventID'],
               'x1':x[0][0],'y1':x[0][1],
               'x2':x[1][0],'y2':x[1][1],
               'x3':x[2][0],'y3':x[2][1],
               'xc':x[3][0],'yc':x[3][1]})

    df = pd.DataFrame(info)
