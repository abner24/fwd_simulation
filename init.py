import scipy as *

n = 500
world = zeros([n,n,n])

## inititation of initial deem
x, y, z = stats.randomint(500), stats.randomint(500), stats.randomint(500)

zeros[x,y,z] = 1

def neighbours(position):
    nn = []
    nbs = []
    for axis in position:
        nn.append(axis+1)
        nn.append(axis-1)
    for index in range(len(nn)):
        if index/2 <=1:
            nbs.append([nn[index],position[1],position[2]])
        elif 1 < index/2 <=2:
            nbs.append([position[0], nn[index], position[2]])
        else:
            nbs.append([position[0], position[1], nn[index])
    return nbs




for neighbours in [



