#!/home/mslim/.conda/envs/py36/bin/python3.6

from model import foward_simulation
import timeit
import numpy as np
import subprocess
import os

env = os.environ.copy()
# focus to print the tree output first
def generate_command(grid_size,node_pop):
    ssm = foward_simulation(grid_size)
    ssm.pop_mig([np.random.randint(grid_size) for i in range(3)])
    total_sample = str(node_pop*grid_size**3)
    command = ['ms', total_sample, '1', '-T', '-t', '1', '-I', str(grid_size ** 3)]
    layout = [str(node_pop) for i in range(grid_size ** 3)]
    return ' '.join(command + layout + ssm.migration_param)

print('size\tduration\tduration(ms)')
for i in range(30):
    print('{}\t{}\t{}'.format(i+3, 
        timeit.timeit(lambda: generate_command(i+3, 15), number=10),
        timeit.timeit(lambda: subprocess.run(generate_command(i+3, 15), shell=True, env=env, stderr=subprocess.STDOUT, stdout=subprocess.DEVNULL), number=10)))
    #print(str(len(generate_command(i+3,15)))+'\n')
