# Complete your game here

# The points.csv file is used to store the scores, False would determine that player didn't win that game.
# In the new_game() method, extra maps can be added. For now, two maps have been provided.
# Green marked scores indicate winning games.
# Gameplay: Avoid monsters and collect as many coins as possible in the shortest time.Use arrow keys to move the robot.
#           Not all the monsters around you will blink! Be careful.
#           Leaderboard is based on both points and time.
#           Only top 10 scores are stored in file.
# Hopefully everything works.

# About coordinate convention:
# For the robot's coordinate, the __get_robot_coordinate() method returns coordinate as (y, x)
# __monster_nearby(robot_coord) function takes coordinate input as tuple and in (y,x) order.
# Other functions (if they take coordinates as input) follow the (x, y) convention and take input as integers.
# The second map may require a few tries to succesfully solve with 100% completion.
# From any window, press Enter to start a random game, Esc to exit()

import pygame
from random import randint, sample
from datetime import datetime

class Wumpus:

    initialised = False #To memorise that the program has been executed, and the start_page doesn't get loaded more than once.

    def __init__(self, map_no=-1):
        pygame.init()
        if not self.initialised:
            self.__start_page()
        self.new_game(map_no)
        self.load_images()
        self.__scale_factor_x = self.__images[2].get_width()
        self.__scale_factor_y = self.__images[3].get_height()
        self.__width = len(self.__map[0]) * self.__scale_factor_x
        self.__height = len(self.__map) * self.__scale_factor_y
        self.__window = pygame.display.set_mode((self.__width,self. __height))
        font = pygame.font.SysFont("Comic Sans MS", 12)
        self.__danger = font.render("!!!BREEZE!!!", True, (255, 255, 255)).convert_alpha()
        self.__clock = pygame.time.Clock()

        self.__points = 0
        self.__alive = True

        pygame.display.set_caption("Wumpus")
        
        self.__start_time = datetime.now()
        self.__end_time = datetime.now()
        self.__main_loop()


    def load_images(self):
        self.__images = []
        for img in ["coin.png", "door.png", "monster.png", "robot.png"]:
            self.__images.append(pygame.image.load(img))
        
    def new_game(self, map_no = -1):
        self.__board1 =  [
                            [3, -1, -1, 0],
                            [0, 2, -1, 2],
                            [2, 0, -1, -1],
                            [-1, 2, 0, 2],
                            [0, -1, -1, 1]
                        ]
        
        self.__board2 = [
                            [3,-1,0,-1,2,0,-1,0,-1],
                            [0,2,-1,0,-1,0,-1,2,-1],
                            [2,0,2,-1,2,-1,0,2,0],
                            [-1,-1,0,-1,0,-1,2,0,-1],
                            [2,0,-1,-1,2,-1,0,-1,2],
                            [-1,2,0,-1,2,-1,-1,0,-1],
                            [0,-1,0,-1,-1,0,2,2,0],
                            [2,0,-1,2,0,-1,0,-1,0],
                            [0,0,0,0,2,0,0,2,1]
                        ]
        self.__board3 = [[]]

        if map_no not in [1,2]:
            #choose a map randomly
            self.__map = sample([self.__board1, self.__board2], 1)[0]
        if map_no == 1:
            self.__map = self.__board1
        
        elif map_no == 2:
            self.__map = self.__board2
        

    def __main_loop(self):
        while True:
            self.__draw_window()
            for event in pygame.event.get():

                robot_coord = self.__get_robot_coordinates()
                if event.type == pygame.QUIT:
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.__move(0, -1)
                    
                    if event.key == pygame.K_DOWN:
                        self.__move(0, 1)
                    
                    if event.key == pygame.K_LEFT:
                        self.__move(-1, 0)

                    if event.key == pygame.K_RIGHT:
                        self.__move(1, 0)
                    
                    if event.key == pygame.K_RETURN:
                        self.__init__()
                    
                    if event.key == pygame.K_1:
                        self.__init__(1)
                    
                    if event.key == pygame.K_2:
                        self.__init__(2)
                    
                    if event.key == pygame.K_ESCAPE:
                        exit()
                    

    def __moves_to_coin(self, x, y):
        robot_coord = self.__get_robot_coordinates()
        if self.__map[robot_coord[0]+y][robot_coord[1]+x] == 0:
            self.__points += 10
            return True
        return False
    
    def __move_to_monster(self, x, y):
        robot_coord = self.__get_robot_coordinates()
        if self.__map[robot_coord[0]+y][robot_coord[1]+x] == 2:
            return True
        return False
    
    def __move_to_void(self, x, y):
        robot_coord = self.__get_robot_coordinates()
        if self.__map[robot_coord[0]+y][robot_coord[1]+x] == -1:
            return True
        return False
    
    def __move_to_door(self, x, y):
        robot_coord = self.__get_robot_coordinates()
        if self.__map[robot_coord[0]+y][robot_coord[1]+x] == 1:
            return True
        return False
                
    def __move(self, x, y):
        robot_coord = self.__get_robot_coordinates()

        if self.__valid_move(x, y):

            if self.__moves_to_coin(x, y) or self.__move_to_void(x, y):
                self.__map[robot_coord[0]][robot_coord[1]] = -1
                self.__map[robot_coord[0]+y][robot_coord[1]+x] = 3 #3 for robot.png

            elif self.__move_to_monster(x, y):
                self.__alive = False #Game Over
                self.__game_over()
            
            elif self.__move_to_door(x, y):
                self.__game_won()
                pass
        
    def __valid_move(self, x, y):
        robot_coord = self.__get_robot_coordinates()

        if robot_coord[1] + x > len(self.__map[0])-1 or robot_coord[1] + x < 0:
            return False
        
        if robot_coord[0] + y > len(self.__map)-1 or robot_coord[0] + y < 0:
            return False

        return True

    def __file_manager(self):
        points_list = []
        points_list.append((self.__points, self.__alive, (self.__end_time - self.__start_time).seconds))
        try:
            with open("points.csv", 'r') as file:
                for line in file:
                    line = line.split(';')
                    points = int(line[0])
                    status = line[1].replace('\n', '')
                    time = int(line[2].replace('\n', ''))
                    temp = (points, status == 'True',time)
                    points_list.append(temp)
        except:
            pass
        points_list.sort(reverse=True)

        if len(points_list) > 10:
            points_list = points_list[0:10]
        with open("points.csv", 'w') as file:
            for points_stats in points_list:
                file.write(f"{points_stats[0]};{points_stats[1]};{points_stats[2]}\n")
        return points_list


    def __game_over(self):
        death_screen_width = 640
        death_screen_height = 480
        self.__game_over_window = pygame.display.set_mode((death_screen_width, death_screen_height))
        times_new_roman = pygame.font.SysFont("Times New Roman", 48)
        comic_sans = pygame.font.SysFont("Comic Sans MS", 24)
        title_text = times_new_roman.render("Game Over", True, (255, 0, 0))
        points = comic_sans.render(f"Your score: {self.__points}", True, (255, 0, 0))
        self.__end_time = datetime.now()

        points_list = self.__file_manager()
        
        while True:
            self.__game_over_window.fill((0,0,0))
            self.__basic_event_handle()

            self.__game_over_window.blit(title_text, (death_screen_width//6+title_text.get_width()//2, 50))
            self.__game_over_window.blit(points, (death_screen_height//6+title_text.get_width()//2+36, 100))
            for i in range(0, len(points_list)):
                times_new_roman = pygame.font.SysFont("Times New Roman", 20)
                color = (255, 0, 0) if not points_list[i][1]  else (0, 255, 0)
                text = times_new_roman.render(f"{i+1}: {points_list[i][0]}, time = {points_list[i][2]} seconds", True, color)
                self.__game_over_window.blit(text, (225, 150+20*i))
            pygame.display.flip()
        
        self.__init__()
    
    def __game_won(self):
        win_screen_width = 640
        win_screen_height = 480
        self.__game_over_window = pygame.display.set_mode((win_screen_width, win_screen_height))
        times_new_roman = pygame.font.SysFont("Times New Roman", 48)
        comic_sans = pygame.font.SysFont("Comic Sans MS", 24)
        title_text = times_new_roman.render("You won!", True, (0, 255, 0))
        points = comic_sans.render(f"Your score: {self.__points}", True, (255, 0, 0))
        self.__end_time = datetime.now()
        points_list = self.__file_manager()
        
        while True:
            self.__game_over_window.fill((0,0,0))
            self.__basic_event_handle()

            self.__game_over_window.blit(title_text, (win_screen_width//6+title_text.get_width()//2+20, 50))
            self.__game_over_window.blit(points, (win_screen_width//6+title_text.get_width()//2+36, 100))
            for i in range(0, len(points_list)):
                times_new_roman = pygame.font.SysFont("Times New Roman", 20)
                color = (255, 0, 0) if not points_list[i][1]  else (0, 255, 0)
                text = times_new_roman.render(f"{i+1}: {points_list[i][0]}, time = {points_list[i][2]} seconds", True, color)
                self.__game_over_window.blit(text, (220, 150+20*i))
                
            pygame.display.flip()
        
        self.__init__()
                
    def __get_robot_coordinates(self):
        #returing coordinates as (y, x)
        for i in range(0, len(self.__map)):
            for j in range(0, len(self.__map[0])):
                if self.__map[i][j] == 3:
                    return i, j
    
    def __start_page(self):
        start_window = pygame.display.set_mode((640, 480))
        pygame.display.set_caption("Wumpus")
        font = pygame.font.SysFont("Times New Roman", 20)
        title_card = font.render("Non-hostile Wumpus", True, (0, 255, 0))
        description_1 = font.render("Wumpus inspired game, where the player needs to collect", True, (255, 255, 255))
        description_2 = font.render("as much coin as possible before exiting the cave.", True, (255, 255, 255))
        description_3 = font.render("Avoid the monsters hidden in the dark. Sometimes they blink.", True, (255,255,255))
        start_1 = font.render("Press ENTER to start at a random cave.", True, (255, 0, 0))
        start_3 = font.render("Press 1, 2 for specific map", True, (255, 0, 0))
        start_2 = font.render("Use arrow keys to move.", True, (255, 0, 0))
        start_window.blit(title_card, (220, 75))
        start_window.blit(description_1, (50, 150))
        start_window.blit(description_2, (50, 180))
        start_window.blit(description_3, (50, 210))
        start_window.blit(start_1, (130, 250))
        start_window.blit(start_3, (130, 280))
        start_window.blit(start_2, (130, 310))
        pygame.display.flip()
        while True:
            self.__basic_event_handle()
                   
    def __basic_event_handle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYDOWN:
                self.initialised = True
                if event.key == pygame.K_RETURN:
                    self.__init__()
                
                if event.key == pygame.K_1:
                    self.__init__(1)
                
                if event.key == pygame.K_2:
                    self.__init__(2)
                
                if event.key == pygame.K_ESCAPE:
                    exit()
        
    
    def __cell_distance(self, x1, y1, x2, y2):
        return ((x1 - x2)**2 + (y1 - y2)**2)**0.5
    
    def __monster_nearby(self, robot_coord):
        try:
            if self.__valid_move(0, -1):
                if self.__map[robot_coord[0]-1][robot_coord[1]] == 2: #(x, y-1)
                    return (robot_coord[0]-1, robot_coord[1])
            if self.__valid_move(0, 1):
                if self.__map[robot_coord[0]+1][robot_coord[1]] == 2: #(x, y+1)
                    return (robot_coord[0]+1, robot_coord[1])
            if self.__valid_move(-1,0):
                if self.__map[robot_coord[0]][robot_coord[1]-1] == 2: #(x-1, y)
                    return (robot_coord[0], robot_coord[1]-1)
            if self.__valid_move(1,0):
                if self.__map[robot_coord[0]][robot_coord[1]+1] == 2: #(x+1, y)
                    return (robot_coord[0], robot_coord[1]+1)
        except:
            pass
        return (0,0)

    def __draw_window(self):
        robot_coord = self.__get_robot_coordinates()

        self.__window.fill((0,0,0))
        for i in range(0, len(self.__map)):
            for j in range(0, len(self.__map[0])):
                if self.__map[i][j] not in [-1, 2]:
                    self.__window.blit(self.__images[self.__map[i][j]], (j*self.__scale_factor_x, i*self.__scale_factor_y))

        nearby_monster_pos = self.__monster_nearby(robot_coord)
        if nearby_monster_pos != (0, 0):
            self.__window.blit(self.__danger, (robot_coord[1]*self.__scale_factor_x-10, robot_coord[0]*self.__scale_factor_y+40))

            if (datetime.now().microsecond < 100000):

                if self.__map[nearby_monster_pos[0]][nearby_monster_pos[1]] == 2:
                    self.__window.blit(self.__images[2], (nearby_monster_pos[1]*self.__scale_factor_x, nearby_monster_pos[0]*self.__scale_factor_y))

        if robot_coord[0] != 0 or robot_coord[1] != 0:
            font = pygame.font.SysFont("Times New Roman", 15)
            timer = font.render(f"{(datetime.now() - self.__start_time).seconds}", True, (255, 255, 255))
            self.__window.blit(timer, (0, 0))
        self.__window.blit(self.__images[1], (self.__width-self.__scale_factor_x, self.__height-self.__scale_factor_y))
        pygame.display.flip()

Wumpus(1)