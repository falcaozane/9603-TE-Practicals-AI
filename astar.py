# importing stuff required
import pygame
import math
from queue import PriorityQueue

width = 800
surface = pygame.display.set_mode((width,width))
pygame.display.set_caption("A Star Pathfinding visualizer" )

img = pygame.image.load(r'C:/Users/AIDEN SAMUEL/Downloads/path1.jfif')

# Set image as icon
pygame.display.set_icon(img)

#defining colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE= (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Cell:
    def __init__(self,row,col,width, total_rows):
        self.row=row
        self.col=col
        self.width= width
        self.total_rows=total_rows
        self.x= row* width
        self.y=col * width
        self.color= WHITE
        self.neighbours=[]
    def get_pos(self):
        return self.row,self.col
    def is_start(self):
        return self.color == YELLOW
    def is_end(self):
        return self.color == PURPLE
    def is_wall(self):
        return self.color == BLACK
    def is_open(self):
        return self.color == TURQUOISE
    def is_close(self):             # main color everywhere
        return self.color == BLUE
    def reset(self):
        self.color = WHITE
    def make_start(self):
        self.color = YELLOW
    def make_end(self):
        self.color = PURPLE
    def make_wall(self):
        self.color = BLACK
    def make_open(self):
        self.color = TURQUOISE
    def make_close(self):             # main color everywhere
        self.color = BLUE
    def make_path(self):
        self.color= GREEN
    def draw(self,surface):
        pygame.draw.rect(surface,self.color,(self.x,self.y,self.width,self.width))
        # pygame.draw.rect()
    def update_neighbours(self,grid):
        if self.row<self.total_rows-1 and not grid[self.row+1][self.col].is_wall():  #down
            self.neighbours.append(grid[self.row+1][self.col])
        if self.row>0 and not grid[self.row-1][self.col].is_wall():  #Upp
            self.neighbours.append(grid[self.row-1][self.col])

        if self.col<self.total_rows-1 and not grid[self.row][self.col+1].is_wall():  #right
            self.neighbours.append(grid[self.row][self.col+1])
        if self.col>0 and not grid[self.row][self.col-1].is_wall():  #left
            self.neighbours.append(grid[self.row][self.col-1])
    def __lt__(self, other):
        return False
        # less than is lt
# cell=Cell()
#heuristic func
def h(p1,p2):
    x1,y1=p1
    x2,y2=p2
    return abs(x1-x2) + abs(y1-y2)

def reconstruct_path(came_from , current, draw1):
    while current in came_from:
        current= came_from[current]
        current.make_path()
        draw1()

#algorithm func
def algorithm(draw1,grid,start,end):
    count=0
    open_set= PriorityQueue() # a queue to get the smallest element out of a queue
    open_set.put((0,count,start))
    came_from= {}
    g_score= {cell: float("inf") for row in grid for cell in row}
    g_score[start]=0  # at start we initialize all to infinity that's what inf means then we say g score at start is 0
    f_score = {cell: float("inf") for row in grid for cell in row}
    f_score[start]=h(start.get_pos(),end.get_pos())#f score is the sum of g and h score since g is 0 at start f score will be h_score thro h()


    open_set_hash={start}   # to see if something is there in open_set
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = open_set.get()[2] # to get the node associated with the minimum element see line 84
        open_set_hash.remove(current)

        if current==end:
            reconstruct_path(came_from,end,draw1)
            start.make_start()
            end.make_end()
            return True
        for neighbour in current.neighbours:
            t_g_score=g_score[current]+1

            if t_g_score< g_score[neighbour]:
                came_from[neighbour]= current
                g_score[neighbour] =t_g_score
                f_score[neighbour] = t_g_score + h(neighbour.get_pos(),end.get_pos())
                if neighbour not in open_set_hash:
                    open_set.put((f_score[neighbour],count, neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.make_open()

        draw1()
        if current!=start:
            current.make_close()
    return False


def make_grid(r,c):
    grid=[]
    cube= c//r
    for i in range(r):
        grid.append([])
        for j in range(r):
            cell=Cell(i,j,cube,r)
            grid[i].append(cell)
    return grid

def draw_line(surface,rows,c):
    cube=c//rows
    for i in range(rows):
        pygame.draw.line(surface,GREY,(0,i*cube),(c,i*cube)) #till the last row
        for j in range(c):
            pygame.draw.line(surface,GREY,(j*cube,0),(j*cube,c))


def draw1(surface,grid,rows,width):
    surface.fill(WHITE)
    for row in grid:
        for cell in row:
            cell.draw(surface)

    draw_line(surface,rows,width)
    pygame.display.update()
def get_clickpos(pos,rows,width):
    cube= width//rows
    y,x=pos
    row=y//cube
    col=x//cube
    return row, col



def main(surface,width):
    rows=40
    grid= make_grid(rows,width)
    start=None
    end=None

    run=True
    while run:
        draw1(surface,grid,rows,width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False

            #left mouse button
            if pygame.mouse.get_pressed()[0]:
                pos= pygame.mouse.get_pos()
                row, col = get_clickpos(pos,rows,width)
                cell=grid[row][col]
                if not start and cell!=start:
                    start=cell
                    start.make_start()
                elif not end and cell!=start:
                    end=cell
                    end.make_end()
                elif cell!=start and cell!=end:
                    cell.make_wall()
            #right mouse button
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clickpos(pos, rows, width)
                cell = grid[row][col]
                cell.reset()
                if cell== start: #for drawing start and end again after being erased
                    start=None
                elif cell== end:
                    end= None
            # in the algo func lambda func is used so that we can pass another func in it
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for cell in row:
                            cell.update_neighbours(grid)
                    algorithm(lambda: draw1(surface,grid,rows,width),grid,start,end)

                if event.key == pygame.K_c:
                    start=None
                    end= None
                    grid= make_grid(rows,width)




    pygame.quit()
main(surface,width)