import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation

# write a function to return neighbours
def main(size):

    #currently starts out with empty grid
    #in the future if random positions are populated it will be included
    class Model(object):
        prob = 100
        timeout = 0
        def __init__(self,size):
            self.size = size
            self.space = np.zeros([size for i in range(3)])
            self.pointx = []
            self.pointy = []
            self.pointz = []
            self.level = []
            self.counter = 0
            #for poisson processes
            self.timestamp = []
        @staticmethod
        def populate_nbs(position):
            neighbour =  ([[position[0]+1,position[1],position[2]],
                           [position[0]-1,position[1],position[2]],
                           [position[0],position[1]+1,position[2]],
                           [position[0],position[1]-1,position[2]],
                           [position[0],position[1],position[2]+1],
                           [position[0],position[1],position[2]-1]])
            return neighbour

        def vaccant_nbs(self, position):
            # position is a list of length 3
            # this function should only return empty neighbours
            vaccant_deems = []
            for locations in self.populate_nbs(position):
                if max(locations)==size or min(locations)<0:
                    continue
                if self.space[tuple(locations)] == 0:
                    vaccant_deems.append(locations)
            return vaccant_deems

        def grid_chooser(self,position):
            vaccant_sites = self.vaccant_nbs(position)
            if len(vaccant_sites) > 0:
                return vaccant_sites[np.random.randint(len(vaccant_sites))]

        def poisson_migration(self,position,depth=0):
            self.level.append(depth)
            if len(self.timestamp) <= depth:
                self.timestamp.append(0)
            while len(self.vaccant_nbs(position))>0:
            #for i in range(10):
                choice = self.grid_chooser(position)
                interval = np.random.exponential(self.prob)
                print(self.timestamp)
                print(len(self.timestamp))
                if choice == None:
                    return 0
                if self.space[tuple(choice)] == 0:
                    if interval >= self.timestamp[depth]:
                        self.timestamp[depth]+=interval
                        self.space[tuple(choice)] = 1
                        self.pointx.append(choice[0])
                        self.pointy.append(choice[1])
                        self.pointz.append(choice[2])
                        if np.sum(self.space)<(size**3-1):
                            self.poisson_migration(choice,depth=depth+1)
                    else:
                        if self.timeout < 1000:
                            self.timeout+=1
                        else:
                            return 0 
                else:
                    self.poisson_migration(choice,depth=depth+1)
                #z, x, y = self.space.nonzero()
                #self.pointx.append(x)
                #self.pointy.append(y)
                #self.pointz.append(z)

      #  def update_graph(self,status):
      #      ax = p3.Axes3D(self.fig)
      #      ax.set_xlim3d([0, size])
      #      ax.set_xlabel('X')
      #      ax.set_ylim3d([0, size])
      #      ax.set_ylabel('Y')
      #      ax.set_zlim3d([0, size])
      #      ax.set_zlabel('Z')
      #      z, x, y = status.nonzero()
      #      graph=self.ax.scatter(x, y, z)
      #      return(graph)

    grid = Model(size)
    position  = [np.random.randint(size) for i in range(3)]
    grid.space[tuple(position)] = 1
    # Creating the Animation object
    grid.poisson_migration(position)
    fig = plt.figure()
    ax = p3.Axes3D(fig)
    ax.set_xlim(0, size)
    ax.set_ylim(0, size)
    ax.set_zlim(0, size)
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')

    index_sets = [np.argwhere(i==grid.level) for i in np.unique(grid.level)]
    #print(index_sets)
    print(index_sets[1][0])
    for num in range(len(index_sets)):
        print('{}\t{}\t{}'.format([grid.pointx[i] for i in index_sets[num][:,0]],
                                  [grid.pointy[i] for i in index_sets[num][:,0]],
                                  [grid.pointz[i] for i in index_sets[num][:,0]]))
    def update(num):
        return ax.scatter(([grid.pointx[i] for i in index_sets[num][:,0]]),
                          ([grid.pointy[i] for i in index_sets[num][:,0]]),
                          ([grid.pointz[i] for i in index_sets[num][:,0]]),
                          s=50, marker = '*', c = 'orange')

    #ax.scatter(grid.pointx[num],grid.pointy[num], grid.pointz[num], marker = (5,2),s=5)
    #ax.scatter([grid.pointx[i] for i in index_sets[1][:,0]],
    #            [grid.pointy[i] for i in index_sets[1][:,0]],
    #            [grid.pointz[i] for i in index_sets[1][:,0]])
    animate = animation.FuncAnimation(fig, update, np.arange(0,len(index_sets)), interval = 50)
    animate.save("trial1.mp4", writer="ffmpeg")
    plt.show()
if __name__=='__main__':
    main(7)



