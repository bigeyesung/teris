from source.grid import Grid
from source.draw import draw
from source.tetris import Tetris
from multiprocessing import Pool
import numpy as np
import pandas as pd
import functools
import os
import sys


def run_tetris(line):
    tetris=Tetris()
    height=tetris.set_height(line) #tweak the height so it doesn't take too much memory
    #create the grid world
    grid_maker=Grid(x=10,y=height)
    for pattern in line:
        brick=tetris.get_brick(pattern)
        #check if this brick is ready to put (all brick cells are empty and cell to top is empty)
        is_this_brick_available, update_brick=tetris.brick_is_available(grid_maker, brick)
        if is_this_brick_available:
            for x,y in update_brick:
                #need to check: 
                grid_maker.grid[x][y]=True
            tetris.add_brick(update_brick)
            #check any row(horizontal) is full: yes-> clean, update grid, no->do nothing
            tetris.check_full_row(grid_maker, update_brick)
        else:
            print('game over')
            ## !! update the current height???????
    #visual check
    space=np.zeros((0,2))
    bricks=np.zeros((0,2))
    for x in range(grid_maker.width):
        for y in range(grid_maker.height):
            data=np.array([[x,y]])
            if grid_maker.grid[x][y]==True:
                bricks=np.vstack((bricks,data))
            else:
                space=np.vstack((space,data))

    #To get height
    height=tetris.get_bricks_height(bricks)
    # print(f'line: {line} has height: {height}')
    # draw(bricks,space)
    return height

def main():

    lines=[]
    results=[]
    #read bricks: STDIN
    for line in sys.stdin:
        if 'q' == line.rstrip():
            break
        elif not line.isspace(): #ignore empty line
            lines.append(line.split(","))
    
    #prepare tetris grid
    run_partial_tetris=functools.partial(run_tetris)
    with Pool(os.cpu_count()) as p:
        results=p.map(run_partial_tetris, lines)
    # for line in lines:
    #     result=run_partial_tetris(line)
    #     results.append(result)
        
    ## if run exe
    with open('output.txt', 'w') as sys.stdout:
        if len(results)==0:
            print(0)
        else:
            for result in results:
                print(result)
    ## if run test
    # if len(results)==0:
    #     print(0)
    # else:
    #     for result in results:
    #         print(result)

if __name__=="__main__":
    main()
    
   