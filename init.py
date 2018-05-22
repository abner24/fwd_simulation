import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation

# write a function to return neighbours
def main(size):

    #currently starts out with empty grid
    #in the future if random positions are populated it will be included
    class model(object):
        def __init__(self,size):
            self.space = np.zeros([size for i in range(3)])

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
        
        def poisson_migration(self,position):
            choice = self.grid_chooser(position)
            if choice == None:
                return 0
            print(self.space)
            if self.space[tuple(choice)] == 0:
                self.space[tuple(choice)] = 1
                if np.sum(self.space)<(size**3-1):
                    self.poisson_migration(choice)
            else:
                self.poisson_migration(choice)

        def update_graph(num):
            ax = p3.Axes3D(fig)
            ax.set_xlim3d([-5.0, size])
            ax.set_xlabel('X')
            ax.set_ylim3d([-5.0, size])
            ax.set_ylabel('Y')
            ax.set_zlim3d([-5.0, size])
            ax.set_zlabel('Z')
            title='3D Test, Time='+str(num*100)
            ax.set_title(title)
            sample=data0[data0['time']==num*100]
            x=sample.x
            y=sample.y
            z=sample.z
            graph=ax.scatter(x,y,z)
            return(graph)

        fig = plt.figure()
        ax = p3.Axes3D(fig)

        # Setting the axes properties
        ax.set_xlim3d([-5.0, 5.0])
        ax.set_xlabel('X')
        ax.set_ylim3d([-5.0, 5.0])
        ax.set_ylabel('Y')
        ax.set_zlim3d([-5.0, 5.0])
        ax.set_zlabel('Z')
        ax.set_title('3D Test')
        data=data0[data0['time']==0]
        x=data.x
        y=data.y
        z=data.z
        graph=ax.scatter(x,y,z)

        # Creating the Animation object
        line_ani = animation.FuncAnimation(fig, update_graph, 19, 
                                           interval=350, blit=False)   
    
    grid = model(size)
    position  = [np.random.randint(size) for i in range(3)]
    #here is the issue!
    grid.space[tuple(position)] = 1 
    print(grid.space)

    grid.poisson_migration(position)

if __name__=='__main__':
    main(5)



