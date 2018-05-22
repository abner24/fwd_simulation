import numpy as np


# write a function to return neighbours
def main(size):

    #currently starts out with empty grid
    #in the future if random positions are populated it will be included
    class model:
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

        @classmethod
        def vaccant_nbs(self, position):
            # position is a list of length 3
            # this function should only return empty neighbours
            vaccant_deems = []
            for locations in self.populate_nbs(position):
                for checks in locations:
                    if checks > size:
                        break
                if self.space[locations] == 0:
                    vaccant_deems.append(self.space[locations])
            return vaccant_deems

        @classmethod
        def grid_chooser(self,position):
            vaccant_sites = self.vaccant_nbs(position)
            return vaccant_sites[np.random.randint(len(vaccant_sites))]

        def poisson_migration(self,position):
            choice = self.grid_chooser(position)
            if self.space[choice] == 0:
                self.space[choice] = 1
                print(self.space)
            else:
                poisson_migration(choice)

    grid = model(size)
    position  = [np.random.randint(size) for i in range(3)]
    #here is the issue!
    grid.space[position] = 1
    print(grid.space)

    grid.poisson_migration(position)

if __name__=='__main__':
    main(5)


