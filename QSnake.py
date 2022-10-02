#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pygame
import time
import random
from SnakeQCAModule import *

font_options=pygame.font.get_fonts()

pygame.init()

light_green= (205, 254, 206)
pink= (255, 7, 134)    
purple = (142, 0, 103)
orange= (253, 121, 0)
red = (213, 50, 80)
darkgreen = (11, 124, 56)
green = (0, 255, 0)
mustard= (208, 255, 56)
white = (255, 255, 255)
black = (0, 0, 0)
blue = (50, 153, 213)

random_colour=(random.random()*255,random.random()*255,random.random()*255)



dis_width = 600
dis_height = 600
 
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('QSnake')
 
clock = pygame.time.Clock()
 
snake_block = 10
snake_speed = 15

stealth=0
curse=0

font_style = pygame.font.SysFont(font_options[2], 20) #bahnschrift
score_font = pygame.font.SysFont(font_options[2], 15) #bahnschrift
power_font = pygame.font.SysFont(font_options[2], 10) #bahnschrift
 
 
def Your_score(score):
    value = score_font.render("Your Score: " + str(score), True, light_green)
    value1 = power_font.render("Your Stealth: " + str(stealth), True, light_green)
    value2 = power_font.render("Your Curses: " + str(curse), True, light_green)
    dis.blit(value, [0, 0])
    dis.blit(value1, [0, 20])
    dis.blit(value2, [0, 30])
 
 
 
def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])
 
 
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 2])
 
 
def gameLoop():
    game_over = False
    game_close = False
    global stealth
    global curse
 
    x1 = dis_width / 2
    y1 = dis_height / 2
 
    x1_change = 0
    y1_change = 0
 
    snake_List = []
    Length_of_snake = 1
    
    items=send_items(snake_List)
    poison_a_x = round(list(items[0].values())[0][0]/10.0)*10.0
    poison_a_y = round(list(items[0].values())[0][1]/10.0)*10.0
    foodx = round(list(items[1].values())[0][0]/10.0)*10.0
    foody = round(list(items[1].values())[0][1]/10.0)*10.0
    poison_b_x = round(list(items[2].values())[0][0]/10.0)*10.0
    poison_b_y = round(list(items[2].values())[0][1]/10.0)*10.0
    
 
    while not game_over:
 
        while game_close == True:
            dis.fill(blue)
            #dis.fill((random.random()*255,random.random()*255,random.random()*255))
            message("You Lost! Press C-Play Again or Q-Quit", red)
            Your_score(Length_of_snake - 1)
            pygame.display.update()
 
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0
 
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)
        
        if list(items[1].keys())[0] == 'food_1':
            col_f=mustard
        elif list(items[1].keys())[0] == 'food_2':
            col_f=white
        elif list(items[1].keys())[0] == 'food_3':
            col_f=green
        elif list(items[1].keys())[0] == 'food_4':
            col_f=darkgreen
        if list(items[0].keys())[0] == 'poison_1':
            col_p_a=pink
        elif list(items[0].keys())[0] == 'poison_2':
            col_p_a=purple
        elif list(items[0].keys())[0] == 'poison_3':
            col_p_a=orange
        elif list(items[0].keys())[0] == 'poison_4':
            col_p_a=red
        if list(items[2].keys())[0] == 'poison_1':
            col_p_b=pink
        elif list(items[2].keys())[0] == 'poison_2':
            col_p_b=purple
        elif list(items[2].keys())[0] == 'poison_3':
            col_p_b=orange
        elif list(items[2].keys())[0] == 'poison_4':
            col_p_b=red
        pygame.draw.rect(dis, col_f, [foodx, foody, snake_block, snake_block])
        pygame.draw.rect(dis, col_p_a, [poison_a_x, poison_a_y, snake_block, snake_block])
        pygame.draw.rect(dis, col_p_b, [poison_b_x, poison_b_y, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]
 
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True
 
        our_snake(snake_block, snake_List)
        Your_score(Length_of_snake - 1)
 
        pygame.display.update()
        
        
        if x1 == foodx and y1 == foody:
            if curse ==0:
                if list(items[1].keys())[0] == 'food_1':
                    Length_of_snake+=1
                elif list(items[1].keys())[0] == 'food_2':
                    Length_of_snake+=1
                    if stealth==0:
                        stealth+=2
                    elif stealth==1:
                        stealth+=1
                elif list(items[1].keys())[0] == 'food_3':
                    Length_of_snake+=4
                elif list(items[1].keys())[0] == 'food_4':
                    Length_of_snake+=15
            else:
                curse-=1
            items=send_items(snake_List)
            poison_a_x = round(list(items[0].values())[0][0]/10.0)*10.0
            poison_a_y = round(list(items[0].values())[0][1]/10.0)*10.0
            foodx = round(list(items[1].values())[0][0]/10.0)*10.0
            foody = round(list(items[1].values())[0][1]/10.0)*10.0
            poison_b_x = round(list(items[2].values())[0][0]/10.0)*10.0
            poison_b_y = round(list(items[2].values())[0][1]/10.0)*10.0
                
        if x1 == poison_a_x and y1 == poison_a_y:
            if stealth ==0:
                if list(items[0].keys())[0] == 'poison_1':
                    Length_of_snake-=1
                elif list(items[0].keys())[0] == 'poison_2':
                    Length_of_snake-=1
                    if curse==0:
                        curse+=2
                    elif curse==1:
                        curse+=1
                elif list(items[0].keys())[0] == 'poison_3':
                    Length_of_snake-=4
                elif list(items[0].keys())[0] == 'poison_4':
                    game_close = True
            else:
                stealth-=1
            items=send_items(snake_List)
            poison_a_x = round(list(items[0].values())[0][0]/10.0)*10.0
            poison_a_y = round(list(items[0].values())[0][1]/10.0)*10.0
            foodx = round(list(items[1].values())[0][0]/10.0)*10.0
            foody = round(list(items[1].values())[0][1]/10.0)*10.0
            poison_b_x = round(list(items[2].values())[0][0]/10.0)*10.0
            poison_b_y = round(list(items[2].values())[0][1]/10.0)*10.0
            
        if x1 == poison_b_x and y1 == poison_b_y:
            if stealth ==0:
                if list(items[2].keys())[0] == 'poison_1':
                    Length_of_snake-=1
                elif list(items[2].keys())[0] == 'poison_2':
                    Length_of_snake-=1
                    if curse==0:
                        curse+=2
                    elif curse==1:
                        curse+=1
                elif list(items[2].keys())[0] == 'poison_3':
                    Length_of_snake-=4
                elif list(items[2].keys())[0] == 'poison_4':
                    game_close = True
            else:
                stealth-=1
            items=send_items(snake_List)
            poison_a_x = round(list(items[0].values())[0][0]/10.0)*10.0
            poison_a_y = round(list(items[0].values())[0][1]/10.0)*10.0
            foodx = round(list(items[1].values())[0][0]/10.0)*10.0
            foody = round(list(items[1].values())[0][1]/10.0)*10.0
            poison_b_x = round(list(items[2].values())[0][0]/10.0)*10.0
            poison_b_y = round(list(items[2].values())[0][1]/10.0)*10.0
 
        clock.tick(snake_speed)
 
    pygame.quit()
    quit()

gameLoop()


# In[ ]:




