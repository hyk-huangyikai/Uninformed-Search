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
    chart.render_to_file('UCS.svg')

class Tree_Node(object):
    def __init__(self,state,parent,path_cost):
        self.state = state
        self.parent = parent
        self.path_cost = path_cost


def BFS(start_x, start_y, end_x, end_y, maze_x, maze_y, is_visited, move, maze_list):
    root = Tree_Node((start_x, start_y), None, 0)
    my_queue = []
    my_queue.append(root)
    count = 1
    while (len(my_queue) != 0):
        min = my_queue[0].path_cost
        index = 0
        #寻找最小路径代价的结点
        for i in range(len(my_queue)):
            if min > my_queue[i].path_cost:
                min = my_queue[i].path_cost
                index = i
        node = my_queue.pop(index)
        if node.state[0] == end_x and node.state[1] == end_y:
            print(count)
            return node
        is_visited[node.state[0]][node.state[1]] = 1
        for i in range(len(move)):
            x = node.state[0] + move[i][0]
            y = node.state[1] + move[i][1]
            if x < 0 or x >= maze_x or y < 0 or y >= maze_y:
                continue
            else:
                if maze_list[x][y] != '1' and is_visited[x][y] == 0:
                    path_cost = node.path_cost + 1
                    state = (x,y)
                    parent = node
                    newNode = Tree_Node(state,parent,path_cost)
                    index1 = 0
                    is_find = 0
                    for k in range(len(my_queue)):
                        if my_queue[k].state == state:
                            if my_queue[k].path_cost > path_cost:
                                index1 = k
                                is_find = 1
                                break
                            is_find = 2
                            break
                    if is_find == 1:
                        my_queue.pop(index1)
                        my_queue.append(newNode)
                    elif is_find == 2:
                        continue
                    else:
                        my_queue.append(newNode)
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