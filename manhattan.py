import json
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from PIL import Image

#I = Image.open('taxi_zone_map_staten_island.jpg')
#I.save('staten_island.png')
#I.show()
'''
img = Image.open("manhattan.png")
print(img.size)
cropped = img.crop((0, 0, 2500, 3200))  # (left, upper, right, lower)
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
def manhattan():
    manhattan=[153, 128, 127, 243, 244, 120, 116, 42, 152, 166, 41, 74, 194, 24, 151, 43, 238, 239, 143, 142,
               75, 236, 237, 263, 141, 140, 262, 202, 50, 48, 230, 163, 161, 162, 229, 233, 170, 100, 164, 186,
               68, 246, 90, 234, 107, 224, 137, 158, 249, 113, 114, 79, 4, 125, 211, 144, 148, 232, 231, 45, 13, 261, 12, 88, 87, 209, 45, 103, 104, 105]
    manhattan = [str(x) for x in manhattan]

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
        if prop[k]['objectid'] in manhattan:
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

    rx0 = -73.9656
    ry0 = 40.782
    for i in range(len(Cx)):
        Cx[i] = (Cx[i]-rx0) * np.cos(-5/180*np.pi) - (Cy[i]-ry0) * np.sin(-5/180*np.pi) + rx0
        Cy[i] = (Cx[i]-rx0) * np.sin(-5/180*np.pi) + (Cy[i]-ry0) * np.cos(-5/180*np.pi) + ry0
    #plt.figure()
    #plt.plot(Cx, Cy, 'o')


    rx = (2550-75)/(74.06-73.886)
    ry = (3150-150)/(40.694-40.87)
    Cox = [round(rx*c+rx*74.06+75) for c in Cx]
    Coy = [round(ry*c-(ry*40.694-3150)) for c in Cy]

    #rx0 = 1200
    #ry0 = 1700
    #for i in range(len(Cx)):
    #    Cox[i] = (Cox[i]-rx0) * np.cos(2/180*np.pi) - (Coy[i]-ry0) * np.sin(2/180*np.pi) + rx0
    #    Coy[i] = (Cox[i]-rx0) * np.sin(2/180*np.pi) + (Coy[i]-ry0) * np.cos(2/180*np.pi) + ry0
    plt.figure()
    plt.plot(Cox, Coy, 'o')
    I = mpimg.imread('manhattan.png')
    plt.imshow(I)
    '''
    plt.figure()
    plt.plot(Cox, Coy, 'o')
    plt.figure()
    Cy = [-1*c for c in Cy]
    plt.plot(Cx, Cy, 'o')
    '''
    return dicx, dicy