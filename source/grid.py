import numpy as np
class Grid:
    def __init__(self, x, y):# width and height
        self.width=x
        self.height=y
        self.grid=np.zeros((x,y),dtype=bool)

    def check_brick_in_grid(self, brick):
        grid_width=len(self.grid)-1
        grid_height=len(self.grid[0])-1
        filter = np.where(((brick[:,0]<=grid_width) & (brick[:,0]>=0) & (brick[:,1]<=grid_height) & (brick[:,1]>=0)),False, True)
        xy_filter=brick[filter]
        if xy_filter:
            return False
        else:
            # print("check_brick_in_grid=True")
            return True
    
    def check_brick_in_empty_cell(self, brick):
        for x,y in brick:
            if self.grid[x][y]:
                return False
        # print("check_brick_in_empty_cell=True")
        return True
    
    def check_brick_top_isempty(self,brick):
        xy_seen={}
        for x,y in brick:
            if xy_seen.get(x)==None:
                xy_seen[x]=y
            else:
                xy_seen[x]=max(y,xy_seen[x]) ##!!!!change to numpy?
        #for each x: select the top y
        for x in xy_seen:
            top_x=x
            top_y=xy_seen[x]
            if any (self.grid[top_x][top_y+1:]):
                return False
        # print("check_brick_top_isempty=True")
        return True
