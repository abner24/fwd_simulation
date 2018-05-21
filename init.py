import scipy as *

size([random(size) for index in range(3)]) = 1

# write a function to return neighbours
def main():

    #currently starts out with empty grid
    #in the future if random positions are populated it will be included
    class model:

        def __init__(self,size):
            self.space = array([size for i in range(3)])


        def populate_nbs(position):
            neighbour =  [[position[0]+1,position[1],position[2]],[position[0]-1,position[1],position[2]],[position[0],position[1]+1,position[2]],[position[0],position[1]-1,position[2]],[position[0],position[1],position[2]+1],[position[0],position[1],position[2]-1]]
            for index,item in enumerate(position):
                if item == 0:



            @classmethod
        def vaccant_nbs(self,position):
            # position is a list of length 3
            # this function should only return empty neighbours
            vaccant_deems = []
            for i in populate_nbs(position):
                if self.space[i] == 1:
                vaccant_deems.append(self.space[i])
        return vaccant_deems

    grid = model(100)






















