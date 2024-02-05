# 1.concept
# iterate whole bricks:
#   for each brick:
#    check if it's location and above to the ceiling is empty:
#     if it is->put it in the location
#     if not: continue to move up 1 step(+y) to find empty space
#    Once brick is put, checking if current row is full or not
#     if full->clear that row, reshape all collided bricks, make sure all bricks go to their new locations or stay.
# once loop is done, calculate the maximum height and return 

# 2.coordinate in my tetris(checking images/fig1.png as an example)
## X:left to right
## Y:bottom to up

# 3.Input/Output data:
### input:each line data
### output: height for each line

# 4.How to run code
### 4-0 env setting
### $ conda create -n encord python=3.8
### $ pip install -r requirement.txt

### 4-1.build exe
### keep L68-L73, comment out L75-L79 in main.py
### $ pyinstaller -n tetris_game main.py

# 4-2. build test exe
### comment out L68-L73, keep L75-L79 in main.py
### $ pyinstaller -n tetris_test main.py

# 4-3.run exe, generate output.txt
### $ ./dist/tetris_game/tetris_game < tests/input.txt > output.txt

# 4-4.run test
### $ python tests/sample_test.py

##don consider empty file input, as this is not valid

# 5.Components
### 5-1.Tetris class: Mainly to working with game related tasks. Some key functions listed below.
### brick_is_available(): checking cells corresponding to brick are empty and on top of it is also empty.
### update_brick_move(): if brick is not stacked on other bricks, then it should go down(by gravity)
### update_all_bricks(): updating all bricks movement
### check_full_row(): checking if any row of grid is full, if it is then clear that row, and update corresponding bricks to move.

# 5-2.Grid class: Mainly to dealing with grid(Width*Height) data.
### check_brick_in_grid():checking current brick is in valid grid location
### check_brick_in_empty_cell():checking current brick is in empty grid location
### check_brick_top_isempty():checking current brick on top is all empty grid location.

# 5-3.draw: visual check 

# 6.Analysis
# 6-1.Time complexity: assuming for each line we have L possible bricks to try, each brick has 4 cell, and the grid size is M*N(width*height),Each brick needs to go through the grid,
### and for each brick cell it needs to check/move horizontally and vertically(M+N).
### The approximately time complexity is O(L*MN*4*(M+N)) 

# 6-2.Space complexity: 
### Assuming we have L possible bricks to try, and we have grid size M*N, and we have 4*L brick cells.
### The space complexity is O(MN+4L)

# 7.Improvement and future work:
# 7-1.[brick] 
### Currently for each brick, I go through each cell in a loop to do functions. Given index is provided already, it should use its index directly as parallel doing all cells at one time to save computation. 

# 7-3.[Algorithm] 
### In general rule of thumb, current algorithm is that for each brick to find empty space. In terms of scalibility, I think it can be improved. One potential solution is to use multi-processing more(which I have use in one place) or distributed system to accelerate game.
### The other idea is to use collision approach, one thing I would like to try is to use "AABB" tree collision. It is used for 2D space traversal. If we have many bricks and large tetris game, searching location would also be time-consuming. So better use other tree/ data scructures to help program run faster.


# 8.TestFiles
# tests/input.txt: test data encord provided
# tests/output_answer.txt: test data answer I provided
# tests/custom_input.txt:  custom test data I provided
# tests/custom_output.txt: custom test answer I provided
