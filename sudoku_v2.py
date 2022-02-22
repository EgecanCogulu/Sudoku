# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 18:36:57 2020

@author: Egecan
"""

import numpy as np
import matplotlib.pyplot as plt
import csv
import os
#Function for generating a valid and solved Sudoku grid. Returns 9x9 2-D numpy ndarray. No input needed.
def sudoku_generator():
    grid=np.zeros((9,9),dtype=int)
    seed=np.arange(1,10,dtype=int)
    np.random.shuffle(seed)
    for i in range(9):
        grid[i]=np.roll(seed,3*i+i//3)
        print(grid[i])
    return grid

#Function for creating a puzzle by masking a number of random squares.
def mask(grid):
    numberofsquares=80
    for i in range(numberofsquares):
        x=int(np.floor(np.random.rand()*9))
        y=int(np.floor(np.random.rand()*9))
        if grid[x][y]!=0:
            grid[x][y]=0 
        else:
            i=i-1
    return(grid)

#Plotter function. Input 9x9 2-D ndarray, it will plot the grid. Returns nothing.
def grid_plotter(grid):
    fig, ax = plt.subplots()
    ax.set_aspect(1)
    ax.set_xlim(-1, 10)
    ax.set_ylim(-1, 10)
    for i in range(10):
        plt.vlines(x=i, ymin=0, ymax=9,lw=1)
        plt.hlines(y=i, xmin=0, xmax=9,lw=1)
    
    for i in range(4):
        plt.vlines(x=3*i, ymin=0, ymax=9,lw=2)
        plt.hlines(y=3*i, xmin=0, xmax=9,lw=2)
    for i in range(81):
        if grid[i//9][i%9]==0:
            plt.text(i%9+0.32,8-i//9+0.32,"")
        else:
            plt.text(i%9+0.32,8-i//9+0.32, str(grid[i//9][i%9]), fontsize=14)
    return None

def bigsquare_indices(row,col):
    BS_indices={}
    
    BS_indices[0]=[(x,y) for x in range(3) for y in range(3)]
    BS_indices[1]=[(x,y) for x in range(3) for y in range(3,6)]
    BS_indices[2]=[(x,y) for x in range(3) for y in range(6,9)]
    BS_indices[3]=[(x,y) for x in range(3,6) for y in range(3)]
    BS_indices[4]=[(x,y) for x in range(3,6) for y in range(3,6)]
    BS_indices[5]=[(x,y) for x in range(3,6) for y in range(6,9)]
    BS_indices[6]=[(x,y) for x in range(6,9) for y in range(3)]
    BS_indices[7]=[(x,y) for x in range(6,9) for y in range(3,6)]
    BS_indices[8]=[(x,y) for x in range(6,9) for y in range(6,9)]
    
    for i in range(9):
        if (row,col) in BS_indices[i]:
            return(i,BS_indices[i])
        
def bigsquare_arrays(grid,index):
    itoc=[[0,0],[0,3],[0,6],[3,0],[3,3],[3,6],[6,0],[6,3],[6,6]]
    row=itoc[index][0]
    col=itoc[index][1]
    return(grid[row:row+3:1,col:col+3:1],itoc[index])

def update_boolean_dict(grid):
    #Initialize a dictionary with boolean grids for each number from 1 to 9. 
    #Empty squares are True, occupied squares are False for all numbers. 
    arrays_dict={}
    for i in range(1,10):
        arrays_dict[i]=np.invert(np.asarray(grid,dtype=bool))
    
    #Iterating through all numbers. Making the column, row and big square FALSE for that number's boolean array
    for row in range(9):
        for col in range(9):
            if grid[row][col]!=0:
                arrays_dict[grid[row][col]][row]=False
                arrays_dict[grid[row][col]][:,col]=False
                
                (i,BS_indices)=bigsquare_indices(row,col)
                for i in range(9):
                    arrays_dict[grid[row][col]][BS_indices[i][0]][BS_indices[i][1]]=False
    
    return arrays_dict
    
def update_sudoku_puzzle(grid,arrays_dict):
    for number in range(1,10):
        for row in range(9):
            if np.count_nonzero(arrays_dict[number][row])==1:
                location=np.where(arrays_dict[number][row] == True)[0][0]
                grid[row][location]=number
                return grid
        for col in range(9):
            if np.count_nonzero(arrays_dict[number][:,col])==1:
                location=np.where(arrays_dict[number][:,col] == True)[0][0]
                grid[location][col]=number
                return grid
                
        for bigsquarenumber in range(9):
            (bigsquare,coor)=bigsquare_arrays(arrays_dict[number],bigsquarenumber)
            if np.count_nonzero(bigsquare)==1:
                location=np.where(bigsquare==True)
                grid[location[0][0]+coor[0]][location[1][0]+coor[1]]=number
                return grid
    # print("No update.")
    return (grid)
 
def convert_sudoku(data):
    grid=np.zeros((9,9),dtype=int)
    for i,char in enumerate(data):
        grid[i//9][i%9]=int(char)
    return (grid)

def read(filename):
    """reads the dat file outputs the list row by row. Returns a list"""
    x=[]
    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            x.append(row)
    return (x)

##################################################################
"""Generating Sudokus"""
    
# solved_sudoku=sudoku_generator()
# grid_plotter(solved_sudoku)
# sudoku_puzzle=mask(np.copy(solved_sudoku))
# grid_plotter(sudoku_puzzle)
    
##################################################################


#################################################################
"""Reading Database"""
filename=r"C:\Users\Egecan\Desktop\sudoku\sudoku.csv"
database=read(filename)



for j in range(100):
    sudoku_puzzle=convert_sudoku(database[j+1][0])
    
    arrays_dict=update_boolean_dict(sudoku_puzzle)

    # grid_plotter(sudoku_puzzle)
    for i in range(64):
        sudoku_puzzle=update_sudoku_puzzle(sudoku_puzzle,arrays_dict)
        arrays_dict=update_boolean_dict(sudoku_puzzle)

    if (np.asarray(list(arrays_dict.values())).any())==False:
        print(j,"Sudoku solved.")
    else:
        print(j,"Couldn't solve :(")

# sudoku_puzzle=convert_sudoku(database[j][0])

# arrays_dict=update_boolean_dict(sudoku_puzzle)
# # grid_plotter(sudoku_puzzle)
# for i in range(64):
#     sudoku_puzzle=update_sudoku_puzzle(sudoku_puzzle,arrays_dict)
#     arrays_dict=update_boolean_dict(sudoku_puzzle)
# grid_plotter(sudoku_puzzle)
# if (True in arrays_dict.items())==False:
#     print("Sudoku solved.")
# grid_plotter(sudoku_puzzle)

# sudoku_puzzle=convert_sudoku("000700000300010008100400307030005200006301400007800010803209001700050009000007002")
# sudoku_puzzle=convert_sudoku("098200540036010290100004007010007000000406000000800060900100006064070810071009420")
# sudoku_puzzle=convert_sudoku("890507000074600500200800003056700030000306000080002670600005008009008160000904027")

arrays_dict=update_boolean_dict(sudoku_puzzle)

grid_plotter(sudoku_puzzle)
# grid_plotter(sudoku_puzzle)
for i in range(64):
    sudoku_puzzle=update_sudoku_puzzle(sudoku_puzzle,arrays_dict)
    arrays_dict=update_boolean_dict(sudoku_puzzle)

if (np.asarray(list(arrays_dict.values())).any())==False:
    print("Sudoku solved.")
else:
    print("Couldn't solve :(")
grid_plotter(sudoku_puzzle)