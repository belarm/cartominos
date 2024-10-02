import pygame
import tiles
import random
import math

pygame.init()
pygame.mixer.init()

GRID_WIDTH = 3 * 16     # putting these in 3 * n format so i 
GRID_HEIGHT = 3 * 9     # remember it needs to be divisible by 3 
TILE_SIZE = 3
CELL_SIZE = 18 #px
FONT_SIZE = 18 #px
PREV_FONT_SIZE = 24
KEY_FONT_SIZE = 12
SCREEN_HEIGHT = GRID_HEIGHT * CELL_SIZE + PREV_FONT_SIZE * 3 + KEY_FONT_SIZE * 12
SCREEN_WIDTH = (GRID_WIDTH * CELL_SIZE) + 336
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
DARKRED = (120, 0, 0)
YELLOW = (200, 200, 0)
BLUE = (0, 180, 255)
GREEN = (0, 200, 0)
BROWN = (200, 255, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hunt and Gather")
font = pygame.font.SysFont('monospace', FONT_SIZE)
preview_font = pygame.font.SysFont('monospace', PREV_FONT_SIZE)
key_font = pygame.font.SysFont('monospace', KEY_FONT_SIZE, bold = True)
flavor_font = pygame.font.SysFont('monospace', KEY_FONT_SIZE, bold = True, italic = True)
error_font = pygame.font.SysFont('monospace', KEY_FONT_SIZE, bold = True)
zodiac_font = pygame.font.SysFont('monospace', PREV_FONT_SIZE)
sun_font = pygame.font.SysFont('monospace', 48)
moon_font = pygame.font.SysFont('monospace', 36)

# --- Init sounds
turn_sound = pygame.mixer.Sound('sound/turn.wav')
place_sound = pygame.mixer.Sound('sound/place.wav')


def generate_tile(tile_id = 0):
    good_tile = False
    while not good_tile:
    
        #generate tile
        tile = tiles.get_tile(random.randint(0,99)) if tile_id == 0 else tiles.get_tile(tile_id)
        colors = tiles.get_colors(tile)
        
        if tile_id !=0:
            good_tile = True
            return tile, colors
        
        # return tile if and only if placeable - THIS DOESN'T WORK FOR SOME REASON
        for col in range(GRID_WIDTH):
            for row in range(GRID_HEIGHT):
                if (    can_place_tile(tile, colors, grid, row, col) or 
                        can_place_tile(rotate_tile(tile), colors, grid, row, col) or 
                        can_place_tile(rotate_tile(rotate_tile(tile)), colors, grid, row, col) or 
                        can_place_tile(rotate_tile(rotate_tile(rotate_tile(tile))), colors, grid, row, col)
                    ):
                    good_tile = True
    return tile, colors

# draw_tile is now only used to draw the preview tile
def draw_tile(tile, colors, x, y):
    for row in range(TILE_SIZE):
        for col in range(TILE_SIZE):
            char = tile[row][col]
            color = colors[row][col]
            text_surface = preview_font.render(char, True, color)
            screen.blit(text_surface, (3 + x + col * PREV_FONT_SIZE,y + row * PREV_FONT_SIZE))
            pygame.draw.rect(screen, WHITE, (x,y, 24 * 3, 24 * 3), 1)

def draw_frame(x, y, width, height):
    elbows = "╔╦╗╚╩╝╠╣╬"
    horizontal = "═"
    vertical = "║"
    top = elbows[0] + horizontal * (width - 2) + elbows[2]
    bottom = elbows[3] + horizontal * (width - 2) + elbows[5]
    top_surface = font.render(top, True, WHITE)
    bottom_surface = font.render(bottom, True, WHITE)
    screen.blit(top_surface, (x, y))
    screen.blit(bottom_surface, (x, y - 18 + 18 * height))
    for i in range(1, height - 1):
        screen.blit(font.render(vertical, True, WHITE), (x, y + i * 18))
        screen.blit(font.render(vertical, True, WHITE), (x + (width * 11) - 11, y + i * 18))

# def blit_text(surface, text, pos, font, color=pygame.Color('black')):
def blit_text(surface, text, font=key_font, color=WHITE):
    # x, y = pos
    font_height = font.get_height() - 1
    line_surfaces = []
    for line in text.splitlines():
        line_surfaces.append(font.render(line, True, color))
    max_width = 0
    total_height = font_height * len(line_surfaces)
    for line_surface in line_surfaces:
        max_width = max(max_width, line_surface.get_width())
        # total_height += line_surface.get_height()
    x = (surface.get_width() - max_width) / 2
    y = surface.get_height() - total_height
    for line_surface in line_surfaces:
        surface.blit(line_surface, (x, y))
        y += font_height
    # surface.blit(line_surface, (x, y))
    # y += font_height

def draw_controls():
    txt = ("   __   __   __           __\n"
           " ||Q |||W |||E ||       ||↑ ||\n"
           " ||__|||__|||__||       ||__||               __\n"
           " |/__\ /__\ /__\|    __ |/__\| __      _____|  ||\n"
           " ||A |||S |||D ||  ||← |||↓ |||→ ||  ||ENTER   ||\n"
           " ||__|||__|||__||  ||__|||__|||__||  ||________||\n"
           " |/__\ /__\ /__\|  |/__\ /__\ /__\|  |/________\|\n\n"
           "  _____________________________________________  \n"
           "||                    SPACE                    ||\n"
           "||_____________________________________________||\n"
           "|/_____________________________________________\|")
    blit_text(screen, txt)
    # text_surface = key_font.render(txt, True, WHITE)
    # screen.blit(text_surface, ((SCREEN_WIDTH / 2) - (text_surface.get_width() / 2), SCREEN_HEIGHT - 144))  # -170 + SCREEN_WIDTH / 2

def draw_grid(grid):
    x = 0
    y = 66
    # pygame.draw.rect(screen, WHITE, (x, y, GRID_WIDTH * CELL_SIZE + 6, GRID_HEIGHT * CELL_SIZE + 6), 3)
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            if grid[row][col]:
                cell, color = grid[row][col]
                draw_cell(cell, color, x + 3 + col * CELL_SIZE, y + 3 + row * CELL_SIZE)

def draw_cell(cell, color, x, y):
    c = (CELL_SIZE - FONT_SIZE)
    if cell == "═" or cell == "█": 
        cell *= 2
        x -= (FONT_SIZE * 11/ 36)
    text_surface = font.render(cell, True, color)
    screen.blit(text_surface, (x + 3, y)) # add 3 and subtract 1 to keep font looking centered

def can_place_tile(tile, colors, grid, row, col):

    #check if selected area is empty
    for i in range(TILE_SIZE):
        for j in range(TILE_SIZE):
            if grid[row + i][col + j] is not None:
                return False       
                
    land = [[None for _ in range(4)] for _ in range(4)]
    neighbor = [[None for _ in range(4)] for _ in range(4)]
    
    NORTH, SOUTH, EAST, WEST = range(4)
            
    land[NORTH] = tile[0][1]
    land[SOUTH] = tile[2][1]
    land[EAST] = tile[1][2]
    land[WEST] = tile[1][0]
    
    neighbor[NORTH] = grid[row-1][col+1][0] if grid[row-1][col+1] != None else None
    neighbor[SOUTH] = grid[row+3][col+1][0] if grid[row+3][col+1] != None else None
    neighbor[EAST] = grid[row+1][col+3][0] if grid[row+1][col+3] != None else None
    neighbor[WEST] = grid[row+1][col-1][0] if grid[row+1][col-1] != None else None

    # impassable lands must align, but passable lands may be adjacent to one another
    if any(land[x] != neighbor[x] and neighbor[x] != None and (land[x] in tiles.impassable or neighbor[x] in tiles.impassable) for x in range(4)):return False

    #check to be sure that there is at least one adjacent tile
    if all(neighbor[i] == None for i in range(4)): return False

    return True
    
def rotate_tile(tile):
    new_tile = [[None for _ in range(TILE_SIZE)] for _ in range(TILE_SIZE)]
    new_tile[0][0] = tile[2][0]
    new_tile[1][0] = tile[2][1]
    new_tile[2][0] = tile[2][2]
    new_tile[0][1] = tile[1][0]
    new_tile[1][1] = tile[1][1]
    new_tile[2][1] = tile[1][2]
    new_tile[0][2] = tile[0][0]
    new_tile[1][2] = tile[0][1]
    new_tile[2][2] = tile[0][2]
    #then rotate river segments
    for i in range(TILE_SIZE):
        for j in range(TILE_SIZE):
            if new_tile[i][j] == "║":
                new_tile[i][j] = "═"
            elif new_tile[i][j] == "═":
                new_tile[i][j] = "║"
    if new_tile[1][1] == "╔":
        new_tile[1][1] = "╗"
    elif new_tile[1][1] == "╗":
        new_tile[1][1] = "╝"
    elif new_tile[1][1] == "╝":
        new_tile[1][1] = "╚"
    elif new_tile[1][1] == "╚":
        new_tile[1][1] = "╔"
    return new_tile

# Initialize game state
grid = [[None for _ in range(GRID_WIDTH+3)] for _ in range(GRID_HEIGHT+3)]
errormessage = ""

#place first tile (sacred grove)
selected_row, selected_col = int(GRID_HEIGHT / 6) * 3, int(GRID_WIDTH / 6) * 3
current_tile, current_colors = generate_tile(tile_id = 100)
for i in range(TILE_SIZE):
    for j in range(TILE_SIZE):
        grid[selected_row+i][selected_col+j] = (current_tile[i][j], current_colors[i][j])

errormessage = ""
placing_tile = True
selected_row = int(GRID_HEIGHT / 6) * 3
selected_col = int(GRID_WIDTH / 6) * 3
current_tile, current_colors = generate_tile()
x = 3
y = 69
delay = 250 
show = True
change_time = pygame.time.get_ticks() + delay
while placing_tile:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            errormessage = ""
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                selected_row = (selected_row - TILE_SIZE) % GRID_HEIGHT
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                selected_row = (selected_row + TILE_SIZE) % GRID_HEIGHT
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                selected_col = (selected_col - TILE_SIZE) % GRID_WIDTH
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                selected_col = (selected_col + TILE_SIZE) % GRID_WIDTH
            elif event.key == pygame.K_e:
                pygame.mixer.Sound.play(turn_sound)
                current_tile = rotate_tile(current_tile)
                current_colors = rotate_tile(current_colors)
            elif event.key == pygame.K_q:
                pygame.mixer.Sound.play(turn_sound)
                current_tile = rotate_tile(current_tile)
                current_tile = rotate_tile(current_tile)
                current_tile = rotate_tile(current_tile) #this is a sad solution but whatever
                current_colors = rotate_tile(current_colors)
                current_colors = rotate_tile(current_colors)
                current_colors = rotate_tile(current_colors)
            elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                if can_place_tile(current_tile, current_colors, grid, selected_row, selected_col):
                    for i in range(TILE_SIZE):
                        for j in range(TILE_SIZE):
                            grid[selected_row+i][selected_col+j] = (current_tile[i][j], current_colors[i][j])
                    current_tile, current_colors = generate_tile()
                else:
                    errormessage = "tile must match adjacent tiles"
    #update display
    screen.fill(BLACK)
    
    legend = [['. " .', (150, 255, 0), "grassland"],
      ["♣ ♣ ♣", (0, 255, 0), "forest"],
      ["Δ 0 Δ", (150, 150, 150), "cave"],
      ["∩ ∩ ∩", (150, 255, 0), "foothills"],
      ["Δ Δ Δ", (150, 150, 150), "mountains"],
      [". ║ .", (0, 0, 255), "river"],
      [". █ .", (0, 0, 255), "lake"]]

    for item in legend:
        xx = GRID_WIDTH * CELL_SIZE + 24
        yy = 270
        txt = item[0]
        text_surface = preview_font.render(txt, True, item[1])
        screen.blit(text_surface, (xx, yy + legend.index(item) * 24))
        txt = item[2]
        text_surface = key_font.render(txt, True, WHITE)
        screen.blit(text_surface, (xx + 161, yy + legend.index(item) * 24))
    
    draw_grid(grid)
    draw_frame(GRID_WIDTH * CELL_SIZE + 6, 58, 30, 28)
    draw_controls()
    current_time = pygame.time.get_ticks()
    if current_time >= change_time:
        change_time = current_time + delay
        show = not show
    if show:
        pygame.draw.rect(screen, RED, (x + selected_col * CELL_SIZE - 1, y + selected_row * CELL_SIZE + 1, TILE_SIZE * CELL_SIZE, TILE_SIZE * CELL_SIZE), 2, border_radius = 3)
    else:
        pygame.draw.rect(screen, DARKRED, (x + selected_col * CELL_SIZE - 1, y + selected_row * CELL_SIZE + 1, TILE_SIZE * CELL_SIZE, TILE_SIZE * CELL_SIZE), 1, border_radius = 3)
    if grid[selected_row][selected_col] == None:
        for i in range(TILE_SIZE):
            for j in range(TILE_SIZE):
                if can_place_tile(current_tile, current_colors, grid, selected_row, selected_col):
                    cell, color = current_tile[i][j], current_colors[i][j]
                else:
                    cell, color = current_tile[i][j], DARKRED
                if not show: color = tuple(n/2 for n in color)
                draw_cell(cell, color, x + (selected_col + j) * CELL_SIZE, y + (selected_row + i) * CELL_SIZE)
    else:
        if errormessage != "":
            errormessage = "cannot place over existing tile"
    draw_tile(current_tile, current_colors, GRID_WIDTH * CELL_SIZE + 133, 76 + 48)
    # screen.blit(text_surface, (GRID_WIDTH * CELL_SIZE + 169 - text_surface.get_width() / 2, 76 + 48 + 3 * PREV_FONT_SIZE))
    txt = errormessage
    text_surface = error_font.render(txt + " " * (43 - len(txt)), True, BLACK, RED)
    if txt != "": 
        screen.blit(text_surface,(GRID_WIDTH * CELL_SIZE + 17, 76 + 92 + 66))
    pygame.display.flip()


        
pygame.quit()
