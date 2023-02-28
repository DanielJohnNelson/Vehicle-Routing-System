#Intelligent Systems Project Assignment
#Authors: Daniel Nelson, Tyler Beaumont
#Statics.py
#This file containss only colour related definitions required for gui

StartupMessage = "Intelligent Systems Assignment 1.\nAuthors: Daniel N & Tyler B.\n"

GREY = (  54,  54,  54)
BLACK= (   0,   0,   0)
WHITE= ( 255, 255, 255)
LGREY= ( 212, 212, 212)

BLUE = (  84, 131, 179)
MINT = ( 130, 255, 193)
GREEN= (  57, 143,  57)
YELLOW=( 255, 241, 120)
ORANGE=( 255, 200, 138)
PINK  =( 252, 157, 157)
RED   =( 235,  63,  63)
NIGHT =( 140, 136, 181)
PURPLE=(  68,  57, 184)
SKY   =( 168, 245, 255)
CYAN  =(   7, 186, 186)
MAGENTA=(177,  18, 201)


COLOURS = {
    'l':BLUE, #location
    'd':BLACK,#Depot
    's':MINT,  #Selected
    'np':LGREY #No package
}

COL_LIST = [MINT,GREEN,YELLOW,ORANGE,PINK,RED,NIGHT,SKY,CYAN,MAGENTA]

#node radius
R = 8