from source.grid import Grid
import numpy as np

class Tetris:
    def __init__(self):
        self.self_height=0
        self.brick_all=[]

    def set_height(self, line):
        height=0
        for pattern in line:
            brick=self.get_brick(pattern)
            brick_height=np.max(brick[:,1])-np.min(brick[:,1])+1
            height+=brick_height
        return int(height)
    
    def add_brick(self,brick):
        self.brick_all.append(brick)

    def brick_is_available(self, grid_maker, brick):
        #if all cell is empty and within the grid
        #for each brick:
        #   lowest pt(s) is available, if not goes up until highest hit the max height
        #   highest pt(s) go up is available
        #   mid pt(s) is available
        brick_y=max(brick[:,1])
        grid_width=len(grid_maker.grid)-1
        grid_height=len(grid_maker.grid[0])-1
        is_this_brick_available=False
        while(brick_y<=grid_height):
            #if fit below contidion: this_brick ok, break loop 
                #check brick fits in grid
                #check overlapped grid cell empty
                #check brick top to the max_height is empty 
            #else:
                #brick goes up and check again
            if grid_maker.check_brick_in_empty_cell(brick) and grid_maker.check_brick_in_grid(brick) and grid_maker.check_brick_top_isempty(brick):
                is_this_brick_available=True
                break
            else:
                brick[:,1]+=1
                brick_y=max(brick[:,1])
        return is_this_brick_available, brick
    
    def get_bricks_height(self, bricks):
        if bricks.shape[0]==0:
            return 0
        else:
            return int(max(bricks[:,1])-min(bricks[:,1])+1)
    def update_grid(self, grid_maker):
        grid_maker.grid=np.zeros((grid_maker.width,grid_maker.height),dtype=bool)
        for brick in self.brick_all:
            for x,y in brick:
                grid_maker.grid[x][y]=True

    def reset_grid(self, brick, grid_maker, loc_flag):
        for x,y in brick:
            grid_maker.grid[x][y]=loc_flag

    def update_brick_move(self, brick, grid_maker):
        size=len(grid_maker.grid[0])
        xy_seen={}
        for x,y in brick:
            if xy_seen.get(x)==None:
                xy_seen[x]=y
            else:
                xy_seen[x]=min(y,xy_seen[x]) ##!!!!change to numpy?
        min_move=size
        for x in xy_seen:
            x_bottom=x
            y_bottom=xy_seen[x]
            move=0
            for search_ind in range(y_bottom-1,-1,-1):#start from next y
                if grid_maker.grid[x_bottom][search_ind]:
                    move=y_bottom-search_ind-1
                    break
                elif search_ind==0 and not grid_maker.grid[x_bottom][search_ind]:
                    move=y_bottom-search_ind
                    break
            min_move=min(min_move,move)
        if min_move!=0:
            self.reset_grid(brick, grid_maker, False)
        brick[:,1]-=min_move
        if min_move!=0:
            self.reset_grid(brick, grid_maker, True)
        return brick

    def update_all_bricks(self, col_counter, grid_maker):
        size=len(grid_maker.grid[0])
        update_bricks=[]
        for brick in self.brick_all:
            if col_counter not in brick[:,1]:
                #check if any brick above goes down as well.
                brick=self.update_brick_move(brick,grid_maker)
                update_bricks.append(brick)
                
            else:
                #update brick shape
                mask=np.where(brick[:,1]==col_counter,False,True)
                brick=brick[mask]
                #update brick location(going down)
                if brick.shape[0]!=0:
                    brick=self.update_brick_move(brick,grid_maker)
                    update_bricks.append(brick)
        self.brick_all=update_bricks

    def check_full_row(self, grid_maker, brick):
        size=len(grid_maker.grid[0])
        col_counter=0
        while(col_counter!=size):
            #if all cell are full
            if np.all(grid_maker.grid[:,col_counter]):
                #clear full cells in grid
                grid_maker.grid[:,col_counter]=False
                #update whole bricks
                self.update_all_bricks(col_counter, grid_maker)
                #update grid based on new brick locations
                self.update_grid(grid_maker)
                #reset counter=0
                col_counter=0
            else:
                col_counter+=1
        
    
    def get_brick(self, pattern): 
        letter, pos= pattern[0],int(pattern[1])
        #starting from left, down
        if letter=='Q': 
            return np.array([[pos+0,0],[pos+1,0],[pos+0,1],[pos+1,1]])
        if letter=='Z': 
            pos+=1 #right shift one step
            return np.array([[pos+0,0],[pos+1,0],[pos+0,1],[pos+-1,1]])
        if letter=='S':
            return np.array([[pos+0,0],[pos+1,0],[pos+1,1],[pos+2,1]])
        if letter=='T':
            pos+=1 #right shift one step
            return np.array([[pos+0,0],[pos+0,1],[pos+1,1],[pos+-1,1]])
        if letter=='I':
            return np.array([[pos+0,0],[pos+1,0],[pos+2,0],[pos+3,0]])
        if letter=='L':
            return np.array([[pos+0,0],[pos+1,0],[pos+0,1],[pos+0,2]])
        if letter=='J':
            return np.array([[pos+0,0],[pos+1,0],[pos+1,1],[pos+1,2]])