import math
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from Analyzor import VertexAnalyzor
from mpl_toolkits.mplot3d import Axes3D


cols = ['Event','trackID','E','x','y','z','eloss','px','py','pz']

with open('trialExtract.dat','r') as f:
    df = pd.DataFrame((l.rstrip().split() for l in f),columns=cols,dtype='float')

stepper = 36

dist = []

while stepper < 200:
    mask = (df['Event']==np.float64(stepper)) | (df['Event']==np.float64(stepper+1))
    df_sort = df[mask]

    x = np.array(df_sort['z'])
    y = np.array(df_sort['y'])

    image = np.zeros([300,600])

    # scale the values to fit into matrix
    scale_x = max(x)/300
    scale_y = max(y)/30

    # check to make sure not dividing by 0
    # if scale_x == 0:
    #     stepper += 2
    #     continue
    # elif scale_y == 0:
    #     stepper += 2
    #     continue

    x = x/scale_x
    y = y/scale_y


    # length = len(x)

    for _ in range(len(x)):

        new_x = int(x[_])+189+ int(np.random.uniform(0,3))
        new_y = int(y[_])+167 + int(np.random.uniform(0,3))

        # print('\n',[new_x,new_y],'\n')
        # if abs(new_x) > 599:
        #     continue
        # elif abs(new_y) > 299:
        #     continue

        if new_y < 167:
            continue
        # give the tracks a thickness
        image[new_y][new_x] = 255
        image[new_y-1][new_x-1] = 255
        image[new_y+1][new_x+1] = 255
        image[new_y][new_x] = 255

    image = image.astype(np.uint8)

    # dff = pd.DataFrame(image)
    # dff.to_csv("check1.csv",index=False,header=False)
    # break

    try:
        points,(xc,yc) = VertexAnalyzor.GetEventPositions(image,1) ## 1 for debug mode and plots, 0 for just running
        print(points,(xc,yc))
        xc,yc = (xc-150)*scale_x, (yc-75)*scale_y
        points = [(float((x-150)*scale_x),float((y-75)*scale_y)) for x,y in points]+[(xc,yc)]
        dist.append({'eventID':stepper//2,'data':points})
    except:
        print('Failed')
        pass

    print('Iteration:',stepper//2)
    break
    stepper += 2

# print(dist)
print("Writing to 'geant.dat' file")
# with open('geant.dat','w') as f:
#     json.dump(dist,f,indent=4)
