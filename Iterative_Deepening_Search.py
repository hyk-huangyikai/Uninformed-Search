import math
import time
import numpy as np
import sys
import pprint
sys.setrecursionlimit(10000000)  # 例如这里设置为一百万
import pygal

def draw_map(road):

    for i in range(len(road)):
        road[i] = (road[i][1],-road[i][0])

    chart = pygal.XY()
    chart.title = "迷宫路线"
    # chart.y_labels = map(str,range(0,-18,-1))
    # chart.x_labels = map(str,range(0,36))
    chart.add("road",road)
    chart.render_to_file('IDS.svg')

class Tree_Node(object):
    def __init__(self,state,parent,path_cost):
        self.state = state
        self.parent = parent
        self.path_cost = path_cost


def DFS(end_x,end_y,maze_x,maze_y,is_visited,move,maze_list,node,dst_node_list,limit):
    if (node.state[0] == end_x and node.state[1] == end_y):
        dst_node_list.append(node)
        return True

    if (limit <= 0) :
        return False

    for i in range(len(move)):
        x = node.state[0] + move[i][0]
        y = node.state[1] + move[i][1]

        if x < 0 or x >= maze_x or y < 0 or y >= maze_y:
            continue
        else:
            if is_visited[x][y] == 0 and maze_list[x][y] != '1' :
                is_visited[x][y] = 1
                state = (x,y)
                parent = node
                path_cost = node.path_cost + 1
                newNode = Tree_Node(state,parent,path_cost)
                if not DFS(end_x,end_y,maze_x,maze_y,is_visited,move,maze_list,newNode,dst_node_list,limit-1):
                    is_visited[x][y] = 0
                else :
                    return True
    return False


def depth_limit_search(start_x,start_y,end_x,end_y,maze_x,maze_y,move,maze_list,dst_node_list,limit):
    is_visited = np.zeros((maze_x,maze_y))
    is_visited[start_x][start_y] = 1
    root = Tree_Node((start_x,start_y),None,0)
    return DFS(end_x,end_y,maze_x,maze_y,is_visited,move,maze_list,root,dst_node_list,limit)

def iterative_deeping_search(start_x,start_y,end_x,end_y,maze_x,maze_y,move,maze_list,dst_node_list):
    for limit in range(1000):
        result = depth_limit_search(start_x,start_y,end_x,end_y,maze_x,maze_y,move,maze_list,dst_node_list,limit)
        if result == True:
            return True
    return False

def main():
    start = time.clock()

    file1_name = "MazeData.txt"
    with open (file1_name,'r',encoding = 'utf-8') as file1:
        maze_list = file1.readlines()

    maze_x = len(maze_list)

    for i in range(maze_x):
        maze_list[i] = maze_list[i][:-1]
        if 'S' in maze_list[i]:
            start_x = i
            start_y = maze_list[i].find('S')
        if 'E' in maze_list[i]:
            end_x = i
            end_y = maze_list[i].find('E')


    maze_y = len(maze_list[0])

    move = [[0,1],[1,0],[0,-1],[-1,0] ]

    dst_node_list = []
    if_find_road  = iterative_deeping_search(start_x,start_y,end_x,end_y,maze_x,maze_y,move,maze_list,dst_node_list)
    road = []
    step = dst_node_list[0].path_cost
    node = dst_node_list.pop(0)
    while True:
        if node == None:
            break
        x = node.state[0]
        y = node.state[1]
        road.append((x, y))
        node = node.parent

    road = list(reversed(road))
    print(road)
    if if_find_road == False:
        print("There is no road!")
    else:
        print("step: ",step)

    end = time.clock()
    print("run time: ",float(end - start)," s")
    draw_map(road)

if __name__ == "__main__":
    main()