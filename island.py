import json
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from PIL import Image

#I = Image.open('taxi_zone_map_staten_island.jpg')
#I.save('staten_island.png')
#I.show()
'''
img = Image.open("staten_island.png")
print(img.size)
cropped = img.crop((50, 250, 2500, 3050))  # (left, upper, right, lower)
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
def island():
    staten_island=[44, 204, 5, 84, 109, 110, 172, 176, 214, 6, 221, 115, 206, 245, 156, 187, 251, 23, 118, 99]
    staten_island = [str(x) for x in staten_island]

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
        if prop[k]['objectid'] in staten_island:
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
    xlim = plt.xlim()
    ylim = plt.ylim()
    #rx0 = -73.8495
    #ry0 = 45.8505


    rx = (2500-50)/(-xlim[0]+xlim[1])
    ry = (3075-425)/(ylim[0]-ylim[1])
    Cox = [round(rx*c-rx*xlim[0]+50) for c in Cx]
    Coy = [round(ry*c-(ry*ylim[0]-3075)) for c in Cy]

    rx0 = 1275
    ry0 = 1750
    theta = 2
    for i in range(len(Cx)):
        Cox[i] = (Cox[i]-rx0) * np.cos(theta/180*np.pi) - (Coy[i]-ry0) * np.sin(theta/180*np.pi) + rx0
        Coy[i] = (Cox[i]-rx0) * np.sin(theta/180*np.pi) + (Coy[i]-ry0) * np.cos(theta/180*np.pi) + ry0
    plt.figure()
    plt.plot(Cox, Coy, 'o')
    I = mpimg.imread('staten_island.png')
    plt.imshow(I)
    '''
    plt.figure()
    plt.plot(Cox, Coy, 'o')
    plt.figure()
    Cy = [-1*c for c in Cy]
    plt.plot(Cx, Cy, 'o')
    '''
    return dicx, dicy