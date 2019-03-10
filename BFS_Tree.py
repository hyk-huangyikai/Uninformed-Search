import math
import sys
import time
import numpy as np
import pygal

def draw_map(road):

    for i in range(len(road)):
        road[i] = (road[i][1],-road[i][0])

    chart = pygal.XY()
    chart.title = "迷宫路线"
    # chart.y_labels = map(str,range(0,-18,-1))
    # chart.x_labels = map(str,range(0,36))
    chart.add("road",road)
    chart.render_to_file('BFS.svg')

class Tree_Node(object):
    def __init__(self,state,parent,path_cost):
        self.state = state #结点状态，二维坐标
        self.parent = parent #父结点
        self.path_cost = path_cost #从起始点到当前结点的路径代价


def BFS(start_x, start_y, end_x, end_y, maze_x, maze_y, is_visited, move, maze_list):
    root = Tree_Node((start_x, start_y), None, 0) #初始化起始点
    my_queue = []
    my_queue.append(root)  #入队
    count = 1
    while (len(my_queue) != 0): #遍历直到队列为空
        node = my_queue.pop(0) #从队列头取出结点
        #到达终点，返回
        if node.state[0] == end_x and node.state[1] == end_y:
            print(count)
            return node
        #检测各个运动方向
        for i in range(len(move)):
            x = node.state[0] + move[i][0] #更新状态坐标
            y = node.state[1] + move[i][1]
            #如果越界，不进行扩展
            if x < 0 or x >= maze_x or y < 0 or y >= maze_y:
                continue
            else:
                #如果没有访问而且不是墙，进行扩展
                if is_visited[x][y] == 0 and maze_list[x][y] != '1':
                    path_cost = node.path_cost + 1 #更新路径代价
                    is_visited[x][y] = 1 #更新访问集
                    state = (x,y) #更新状态
                    parent = node #设置父结点
                    #创建新结点
                    newNode = Tree_Node(state,parent,path_cost)
                    my_queue.append(newNode) #入队
                    count += 1
    return None

def main():
    start = time.clock()

    file1_name = "MazeData.txt"
    with open(file1_name, 'r', encoding='utf-8') as file1:
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

    is_visited = np.zeros((maze_x, maze_y))
    is_visited[start_x][start_y] = 1

    move = [[1, 0], [0, -1], [-1, 0], [0, 1]]

    dst_node = BFS(start_x, start_y, end_x, end_y, maze_x, maze_y, is_visited, move, maze_list)
    min_road = []
    step = dst_node.path_cost
    node = dst_node
    while True:
        if node == None:
            break
        x = node.state[0]
        y = node.state[1]
        min_road.append((x,y))
        node = node.parent

    min_road = list(reversed(min_road))
    print(min_road)
    if dst_node == None:
        print("There is no road!")
    else:
        print("min step: ", step)

    end = time.clock()
    print("run time: ", float(end - start), " s")
    draw_map(min_road)

if __name__ == "__main__":
    main()