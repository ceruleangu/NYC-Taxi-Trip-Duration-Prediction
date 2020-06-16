import json
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from PIL import Image

#I = Image.open('taxi_zone_map_staten_island.jpg')
#I.save('staten_island.png')
#I.show()
'''
img = Image.open("bronx.png")
print(img.size)
cropped = img.crop((50, 420, 2500, 2900))  # (left, upper, right, lower)
cropped.show()
cropped.save("cut.png")
'''
'''
I = mpimg.imread('bronx.png')
plt.figure()
plt.imshow(I)
plt.figure()
I1 = I[:,:,0]
plt.imshow(I1)
'''



def Bronx():
    bronx = [1, 264,265, 200, 220, 240, 241, 136, 235, 119, 247, 168, 159, 69, 167, 147, 47, 169, 59, 60, 78, 20, 31, 94,
    18, 241, 174, 259, 254, 32, 3, 81, 51, 184, 46, 183, 185, 242, 58, 208, 213, 250, 212, 248, 182, 126, 199]
    brooklyn = [112, 255, 80, 256, 36, 37, 63, 76, 77, 35, 177, 225, 61, 62, 17, 49, 97, 34, 217, 66, 65, 33,
     54, 52, 25, 195, 40, 106, 181, 189, 190, 257, 111, 228, 227, 14, 67, 11, 22, 21, 108, 55, 29, 150, 210, 154,
     123, 149, 155, 178, 165, 91, 39, 222, 71, 72, 89, 85, 26, 133, 188]
    bronx = [str(x) for x in bronx]
    brooklyn = [str(x) for x in brooklyn]

    with open('NYC_Taxi_Zones.geojson') as f:
        data = json.load(f)
    prop = []
    co = []
    plt.figure()
    k = 0
    Cx = []
    Cy = []
    dicx = {}
    dicy = {}
    for feature in data['features']:
        # print(feature['properties'])
        prop.append(feature['properties'])
        co.append(feature['geometry']['coordinates'])
    for k in range(len(co)):
        if prop[k]['objectid'] in bronx:
            if len(co[k]) > 1:
                ccx = []
                ccy = []
                cx = 0
                cy = 0
                Area = []
                for j in range(len(co[k])):
                    b = co[k][j][0]
                    x = []
                    y = []
                    A = 0
                    cx = 0
                    cy = 0
                    for i in range(len(b)):
                        x.append(b[i][0])
                        y.append(b[i][1])
                    for t in range(len(x)-1):
                        A += x[t] * y[t + 1] - x[t + 1] * y[t]
                        cx += ((x[t]+x[t+1])*(x[t]*y[t+1]-x[t+1]*y[t]))
                        cy += ((y[t]+y[t+1])*(x[t]*y[t+1]-x[t+1]*y[t]))
                    ccx.append(cx/3)
                    ccy.append(cy/3)
                    Area.append(A)
                    plt.plot(x,y,'-')

                ccx = [c / sum(Area) for c in ccx]
                ccy = [c / sum(Area) for c in ccy]
                cx = sum(ccx)
                cy = sum(ccy)
                dicx[prop[k]['objectid']] = cx
                dicy[prop[k]['objectid']] = cy
                Cx.append(cx)
                Cy.append(cy)
                plt.plot(Cx, Cy, 'o')
                plt.show()
            else:
                for j in range(len(co[k])):
                    b = co[k][j][0]
                    x = []
                    y = []
                    cx = 0
                    cy = 0
                    for i in range(len(b)):
                        A = 0
                        x.append(b[i][0])
                        y.append(b[i][1])
                    for t in range(len(x)-1):
                        cx += (x[t]+x[t+1])*(x[t]*y[t+1]-x[t+1]*y[t])
                        cy += (y[t]+y[t+1])*(x[t]*y[t+1]-x[t+1]*y[t])
                        A += x[t]*y[t+1]-x[t+1]*y[t]
                    Cx.append(cx/A/3)
                    Cy.append(cy/A/3)
                    dicx[prop[k]['objectid']] = cx/A/3
                    dicy[prop[k]['objectid']] = cy/A/3
                    plt.plot(x,y,'-')
                    plt.plot(Cx, Cy, 'o')
    plt.show()

    #rx0 = -73.8495
    #ry0 = 45.8505


    rx = (2600-50)/(73.942-73.757)
    ry = (2950-420)/(40.779-40.922)
    Cox = [round(rx*c+rx*73.942+50) for c in Cx]
    Coy = [round(ry*c-(ry*40.779-2950)) for c in Cy]

    rx0 = 1325
    ry0 = 1685
    for i in range(len(Cx)):
        Cox[i] = (Cox[i]-rx0) * np.cos(7/180*np.pi) - (Coy[i]-ry0) * np.sin(7/180*np.pi) + rx0
        Coy[i] = (Cox[i]-rx0) * np.sin(7/180*np.pi) + (Coy[i]-ry0) * np.cos(7/180*np.pi) + ry0
    plt.figure()
    plt.plot(Cox, Coy, 'o')
    I = mpimg.imread('bronx.png')
    plt.imshow(I)
    '''
    plt.figure()
    plt.plot(Cox, Coy, 'o')
    plt.figure()
    Cy = [-1*c for c in Cy]
    plt.plot(Cx, Cy, 'o')
    '''
    return dicx, dicy