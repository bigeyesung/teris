#iterate the blocks:
#   for each block:
#       check if location and its above to the ceiling is empty(adding one more var to keep current height for each col)
#       #every time checking if any row is full or not
#       # if full->delete that row, rearrange block above that row, to find their new location.
#   #once loop is done, calculate the maximum height and return 
from source.grid import Grid
from source.draw import draw
from source.tetris import Tetris
import numpy as np
import pandas as pd
import argparse
import functools
import os
import sys
from multiprocessing import Pool


def run_single(line):
        tetris=Tetris()
        height=tetris.set_height(line) ##tweak the height so take mem too much
        #create the grid world
        grid_maker=Grid(x=10,y=height)
        for pattern in line:
            # if pattern =="Q4":
            #     print('pause')
            brick=tetris.get_brick(pattern)
            #check this brick is ready to put (all cell empty/ cell to top empty)
            is_this_brick_available, update_brick=tetris.is_available(grid_maker,brick)
            if is_this_brick_available:
                for x,y in update_brick:
                    #need to check: 
                    grid_maker.grid[x][y]=True
                tetris.add_brick(update_brick)
                #check any row is full: yes-> clean, update grid, no->do nothing
                tetris.check_full_row(grid_maker,update_brick)
            else:
                print('game over')
                ## !! update the current height
        #visual check
        space=np.zeros((0,2))
        bricks=np.zeros((0,2))
        for x in range(len(grid_maker.grid)):
            for y in range(len(grid_maker.grid[0])):
                data=np.array([[x,y]])
                if grid_maker.grid[x][y]==True:
                    bricks=np.vstack((bricks,data))
                else:
                    space=np.vstack((space,data))

        #To get height
        height=tetris.get_bricks_height(bricks)
        
        print(f'line: {line} has height: {height}')
        return height
        # draw(bricks,space)

def main():
    #pass paras
    # parser = argparse.ArgumentParser()
    # parser.add_argument('input',  type=str, help='the input txt file')
    # # parser.add_argument('output', type=str, help='the output txt file')
    # args = parser.parse_args()

    #STDIN
    std_line=[]
    for line in sys.stdin:
        if 'q' == line.rstrip():
            break
        print(f'Input : {line}')
        std_line.append(line)
    

    #read bricks
    lines=[]
    
    # fin = open(input_filepath, "r")
    for line in std_line:
        lines.append(line.split(","))
    # fin.close()
    #prepare tetris grid
    if False: # linear
        cnt=0
        for line in lines:
            tetris=Tetris()
            height=tetris.set_height(line) ##tweak the height so take mem too much
            #create the grid world
            grid_maker=Grid(x=10,y=height)
            for pattern in line:
                # if pattern =="Q4":
                #     print('pause')
                brick=tetris.get_brick(pattern)
                #check this brick is ready to put (all cell empty/ cell to top empty)
                is_this_brick_available, update_brick=tetris.is_available(grid_maker,brick)
                if is_this_brick_available:
                    for x,y in update_brick:
                        #need to check: 
                        grid_maker.grid[x][y]=True
                    tetris.add_brick(update_brick)
                    #check any row is full: yes-> clean, update grid, no->do nothing
                    tetris.check_full_row(grid_maker,update_brick)
                else:
                    print('game over')
                    ## !! update the current height
            #visual check
            space=np.zeros((0,2))
            bricks=np.zeros((0,2))
            for x in range(len(grid_maker.grid)):
                for y in range(len(grid_maker.grid[0])):
                    data=np.array([[x,y]])
                    if grid_maker.grid[x][y]==True:
                        bricks=np.vstack((bricks,data))
                    else:
                        space=np.vstack((space,data))

            #To get height
            height=tetris.get_bricks_height(bricks)
            cnt+=1
            print(f'Q{cnt}, line: {line} has height: {height}')
            results.append(height)
            # draw(bricks,space)
    else:
        results=[]
        run_partial=functools.partial(run_single)
        with Pool(os.cpu_count()) as p:
            results=p.map(run_partial, lines)
        # for line in lines:
        #     result=run_partial(line)
        #     results.append(result)
        with open('output.txt', 'w') as sys.stdout:
            for result in results:
                print(result)


if __name__=="__main__":
    main()
    
   