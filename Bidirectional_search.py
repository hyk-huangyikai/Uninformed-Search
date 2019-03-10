import math
import sys
import time
import numpy as np
import pygal

def draw_map(road1,road2):

    for i in range(len(road1)):
        road1[i] = (road1[i][1],-road1[i][0])
    for i in range(len(road2)):
        road2[i] = (road2[i][1],-road2[i][0])

    chart = pygal.XY()
    chart.title = "迷宫路线"
    # chart.y_labels = map(str,range(0,-18,-1))
    # chart.x_labels = map(str,range(0,36))
    chart.add("front",road1)
    chart.add("back",road2)
    chart.render_to_file('BS.svg')



class Tree_Node(object):
    def __init__(self,state,parent,path_cost):
        self.state = state
        self.parent = parent
        self.path_cost = path_cost


def Bidirection_BFS(start_x, start_y, end_x, end_y, maze_x, maze_y, is_visited, move, maze_list):
    start_node = Tree_Node((start_x, start_y), None, 0)
    end_node = Tree_Node((end_x,end_y),None,0)
    front_queue = []
    front_queue.append(start_node) #初始点出发的队列
    back_queue = []
    back_queue.append(end_node) #从终点出发的队列
    count = 1
    while len(front_queue) != 0 or len(back_queue) != 0:
        if len(front_queue) != 0:
            node = front_queue.pop(0)
            for i in range(len(move)):
                x = node.state[0] + move[i][0]
                y = node.state[1] + move[i][1]
                if x < 0 or x >= maze_x or y < 0 or y >= maze_y:
                    continue
                else:
                    if maze_list[x][y] != '1':
                        path_cost = node.path_cost + 1
                        state = (x, y)
                        parent = node
                        newNode = Tree_Node(state, parent, path_cost)
                        #在后端队列寻找相同结点
                        for k in range(len(back_queue)):
                            #找到说明路径连通，直接返回
                            if newNode.state == back_queue[k].state:
                                return (newNode,back_queue[k])
                    if is_visited[x][y] == 0 and maze_list[x][y] != '1':
                        is_visited[x][y] = 1
                        front_queue.append(newNode)
                        count += 1
        if len(back_queue) != 0:
            node = back_queue.pop(0)
            for i in range(len(move)):
                x = node.state[0] + move[i][0]
                y = node.state[1] + move[i][1]
                if x < 0 or x >= maze_x or y < 0 or y >= maze_y:
                    continue
                else:
                    if maze_list[x][y] != '1':
                        path_cost = node.path_cost + 1
                        state = (x, y)
                        parent = node
                        newNode = Tree_Node(state, parent, path_cost)
                        for k in range(len(front_queue)):
                            if newNode.state == front_queue[k].state:
                                return (front_queue[k],newNode)
                    if is_visited[x][y] == 0 and maze_list[x][y] != '1':
                        is_visited[x][y] = 1
                        back_queue.append(newNode)
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

    dst_node = Bidirection_BFS(start_x, start_y, end_x, end_y, maze_x, maze_y, is_visited, move, maze_list)
    if dst_node == None:
        print("There is no road!")
    else:
        node1 = dst_node[0]
        node2 = dst_node[1]
        min_road1 = []
        step = node1.path_cost + node2.path_cost
        print("Front step: ",node1.path_cost, "    Back step: ",node2.path_cost)
        node = node1
        while True:
            if node == None:
                break
            x = node.state[0]
            y = node.state[1]
            min_road1.append((x,y))
            node = node.parent

        min_road2 = []
        node = node2
        while True:
            if node == None:
                break
            x = node.state[0]
            y = node.state[1]
            min_road2.append((x,y))
            node = node.parent


        min_road1 = list(reversed(min_road1))
        min_road1.pop()
        min_road1.extend(min_road2)
        print(min_road1)
        print("min step: ", step)

    end = time.clock()
    print("run time: ", float(end - start), " s")
    draw_map(min_road1,min_road2)

if __name__ == "__main__":
    main()