from random import randint

TILE_TYPES = 9 # there will be one more tile type than this, used for initial tile

WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (200, 200, 0)
BROWN = (150, 255, 0)
DARKGREEN = (0, 180, 0)

passable = (".", "♣", "0", '"', "∩")
impassable = ("Δ", "║", "═", "╔", "╗", "╚", "╝", "█")

s = [None for _ in range(TILE_TYPES + 1)]
freq = [0 for _ in range(TILE_TYPES + 1)] # numbers must add to 100; frequencies of each tile type

s[0], freq[0] = ".........", 45 #meadow
    
s[1], freq[1] = "∩Δ∩.∩....", 12 #mountains / one side
s[2], freq[2] = "∩ΔΔ.∩Δ..∩", 9  #mountains / two sides
s[3], freq[3] = "∩ΔΔ.∩Δ∩ΔΔ", 6  #mountains / three sides
s[4], freq[4] = "ΔΔΔΔΔΔΔΔΔ", 2  #mountains / four sides
   
s[5], freq[5] = "Δ║ΔΔ█ΔΔΔΔ", 1  #spring
    
s[6], freq[6] = ".║..║..║.", 15 #river
s[7], freq[7] = "Δ║ΔΔ║ΔΔ║Δ", 2  #canyon
s[8], freq[8] = ".║..╚═...", 8  #river bend

s[9], freq[9] = "♣♣♣♣█♣♣♣♣", 0  #sacred grove

inter = [freq[0]]
for i in range(1,TILE_TYPES): inter.append(freq[i] + inter[i - 1]) # gets interval for each tile based on frequency
inter.append(0)

def get_tile(tile_id):
    t = [None for _ in range(9)]
    decor = "♣" if randint(0,1) == 0 else '"'
    for i in range(TILE_TYPES):
        if tile_id in range(inter[i-1], inter[i]): t = list(s[i][_] for _ in range(9))
    if tile_id == 100: t = list(s[TILE_TYPES][_] for _ in range(9))
    for i in range(9):
        if t[i] == "." and randint(0,1) == 0: t[i] = decor
        if t[i] == "Δ" and randint(0,100) == 0: t[i] = "0"
    return((t[0],t[1],t[2]),(t[3],t[4],t[5]),(t[6],t[7],t[8]))

def get_colors(tile):
    colors = [[None for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            colors[i][j] = WHITE #default color
            if tile[i][j] == "∩":
                colors[i][j] = BROWN
            if tile[i][j] == ".":
                colors[i][j] = BROWN
            if tile[i][j] == '"':
                colors[i][j] = BROWN
            if tile[i][j] == "0":
                colors[i][j] = GRAY
            if tile[i][j] == "Δ":
                colors[i][j] = GRAY
            if tile[i][j] == "♣":
                colors[i][j] = GREEN
            if tile[i][j] == "♠":
                colors[i][j] = DARKGREEN    
            if tile[i][j] == "║" or tile[i][j] == "═" or tile[i][j] == "╔" or tile[i][j] == "╗" or tile[i][j] == "╚" or tile[i][j] == "╝" or tile[i][j] == "█":
                colors[i][j] = BLUE
    return colors
