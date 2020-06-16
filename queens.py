import json
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from PIL import Image

#I = Image.open('taxi_zone_map_staten_island.jpg')
#I.save('staten_island.png')
#I.show()
'''
img = Image.open("queens.png")
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
def queens():
    queens=[27, 201, 117, 86, 2, 30, 124, 132, 219, 203, 180, 216, 10, 215, 205, 218, 219, 139,
            38, 258, 197, 130, 122, 191, 19, 175, 64, 101, 15, 16, 252, 53, 253, 92, 171, 73, 9,
            192, 121, 98, 131, 28, 135, 93, 134, 95, 96, 102, 57, 56, 196, 160, 198, 173, 70, 138,
            157, 82, 83, 129, 226, 260, 207, 223, 7, 8, 145, 146, 193, 179, 8]
    queens = [str(x) for x in queens]

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
        if prop[k]['objectid'] in queens:
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


    rx = (2500-100)/(-xlim[0]+xlim[1])
    ry = (3500-225)/(ylim[0]-ylim[1])
    Cox = [round(rx*c-rx*xlim[0]+100) for c in Cx]
    Coy = [round(ry*c-(ry*ylim[0]-3500)) for c in Cy]

    rx0 = 1300
    ry0 = 1862.5
    for i in range(len(Cx)):
        Cox[i] = (Cox[i]-rx0) * np.cos(8/180*np.pi) - (Coy[i]-ry0) * np.sin(8/180*np.pi) + rx0
        Coy[i] = (Cox[i]-rx0) * np.sin(8/180*np.pi) + (Coy[i]-ry0) * np.cos(8/180*np.pi) + ry0
    plt.figure()
    plt.plot(Cox, Coy, 'o')
    I = mpimg.imread('queens.png')
    plt.imshow(I)
    '''
    plt.figure()
    plt.plot(Cox, Coy, 'o')
    plt.figure()
    Cy = [-1*c for c in Cy]
    plt.plot(Cx, Cy, 'o')
    '''
    return dicx, dicy