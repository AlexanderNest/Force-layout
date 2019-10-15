import math
from random import randint
from tkinter import Tk, Canvas, Button

CANVAS_W, CANVAS_H = 1500, 900
NODE_R = 5


class Vec:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Node:
    def __init__(self, text):
        self.text = text
        self.targets = []
        self.vec = Vec(0, 0)

    def to(self, *nodes):
        for n in nodes:
            self.targets.append(n)
            n.targets.append(self)
        return self


class Graph:
    def __init__(self):
        self.nodes = []

    def add(self, text):
        self.nodes.append(Node(text))
        return self.nodes[-1]


class GUI:
    def __init__(self, root):
        self.canvas = Canvas(root, width=CANVAS_W, height=CANVAS_H, bg="white")
        self.draw_button = Button(root, text="Draw", command=self.draw)
        self.canvas.pack()
        self.draw_button.pack()
        self.nodes = None
        self.busy = None

    def draw_node(self, x, y, text, r=NODE_R):
        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill="MistyRose2")
        self.canvas.create_text(x, y, text=text)

    def draw_graph(self):
        for n in self.nodes:
            for t in n.targets:
                self.canvas.create_line(n.vec.x, n.vec.y, t.vec.x, t.vec.y)
        for n in self.nodes:
            self.draw_node(n.vec.x, n.vec.y, n.text)

    def draw(self):
        self.canvas.delete("all")
        if self.busy:
            root.after_cancel(self.busy)
        random_layout(self.nodes)
        self.animate()

    def animate(self):
        self.canvas.delete("all")
        force_layout(self.nodes, 10)
        self.draw_graph()
        self.busy = root.after(5, self.animate)


def random_layout(nodes):
    for n in nodes:
        n.vec.x = randint(NODE_R * 4, CANVAS_W - NODE_R * 4 - 1)
        n.vec.y = randint(NODE_R * 4, CANVAS_H - NODE_R * 4 - 1)


def vec_mag(v):
    return math.sqrt(v.x * v.x + v.y * v.y)


def vec_add(v1, v2):
    return Vec(v1.x + v2.x, v1.y + v2.y)


def vec_sub(v1, v2):
    return Vec(v1.x - v2.x, v1.y - v2.y) 


def vec_dist(v1, v2):
    return vec_mag(vec_sub(v1, v2))


def vec_mul(v, n):
    return Vec(v.x * n, v.y * n)


def vec_unit(v):
    m = vec_mag(v)
    return Vec(v.x / m, v.y / m) if m else Vec(0, 0)


C1, C2, C3, C4 = 2, 20, 20000, 0.1


def f_ball(v1, v2):
    return vec_mul(vec_unit(vec_sub(v1, v2)), C3/(vec_dist(v1, v2)**2))
    

def f_spring(v1, v2):
    return vec_mul(vec_unit(vec_sub(v2, v1)), C1*math.log(vec_dist(v1, v2)/C2))


def force_layout(nodes, iters):
    forces = {}
    for k in range(iters):
        for n in nodes:
            forces[n] = Vec(0, 0)
            for m in n.targets:
                forces[n] = vec_add(forces[n], f_spring(n.vec, m.vec))
            for j in nodes:
                if n != j and j not in n.targets:
                    forces[n] = vec_add(forces[n], f_ball(n.vec, j.vec))
            
        for n in nodes:
            n.vec = vec_add(n.vec, vec_mul(forces[n], C4))


g = Graph()


file = open(r'C:\Users\NDA\Desktop\Python projects\Social graph\social graph.txt', 'r')

text = file.read().split('\n')

file.close()

splittext = []

for i in text:
    splittext.append(i.split())

'''
    заполнение узлов и связей
'''
nodes = [x[0] for x in splittext]

x = 0
for i in nodes:
    nodes[x] = g.add(i)
    x += 1

x = 0

for i in splittext:
    for k in i[1:]:
        nodes[x].to(nodes[int(k)])
    x += 1


'''
    Для каждого участника найти всех не знакомых с ним людей, имеющих 1 общего друга c данным участником. 
'''

'''for i in nodes:
    for k in i.targets:
        if i not in nodes[int(k.text)].targets:
            print(i.text + ' - ', end='')
            for j in nodes[k].targets:
                print(j.text + ' ', end='')
                print()

for i in nodes:
    for k in targets:
        for j in k'''



fil = open('facebook_combined.txt')
print(fil.read())

for i in splittext:
    node = i[0]
    friends = i[1:]
    nodetocompare = None
    for k in friends:
        nodetocompare = splittext[int(k)][1:]
        for o in nodetocompare:
            if node not in splittext[int(o)][1:]:
                pass
                #fil.write(node + ' friends with ' + o + ' from ' + splittext[int(k)][0] + '\n')
                #print(node + ' friends with ' + o + ' from ' + splittext[int(k)][0])
fil.close()






'''root = Tk()
w = GUI(root)
w.nodes = g.nodes
root.mainloop()'''


