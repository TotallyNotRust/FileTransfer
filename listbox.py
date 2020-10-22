from tkinter import *
from tkinter import filedialog, dnd
from tkinter.dnd import DndHandler
import re, windnd

data = []
dataLocations = []

def insert():
    lb.delete(0, len(data))
    for ind, _ in enumerate(data):
        lb.insert(END, data[ind])

def selector(ind):
    data[ind] = data[ind].split(" <")[0]
    data[current] += " <"
    insert()

def findAmount(od, d="", c=1):
    d = od+" [{}]".format(str(c))
    return d if not d in data else findAmount(od, d, c+1)

current = 0

def select(event):
    global current
    last = current
    current = lb.nearest(event.y)
    selector(last)
    print("Current changed to", current)

def move(event):
    global current
    element = lb.nearest(event.y)
    try:
        if element != current:
            From = data[current]
            To = data[element]
            FromL = dataLocations[current]
            ToL = dataLocations[element]
            print("{} -> {}".format(From[:-2], To))
            data[current] = To
            data[element] = From
            print("{} -> {}".format(FromL, ToL))
            dataLocations[current] = ToL
            dataLocations[element] = FromL
            print(dataLocations)
            insert()
            current = element
    except Exception as e: print(e)


def add(file = None):
    global data
    global dataLocations
    if not file: d = [filedialog.askopenfilename()]
    else: d = file
    for i in d:
        print(i)
        if i in data:
            i = findAmount(d)
        data += [i.split("/")[-1].split("\\")[-1]]
        dataLocations += [i]
    insert()


def init(name=None):
    global lb
    root = Tk()
    master = Frame()
    master.grid(row=0,column=0,columnspan=2)

    if name:
        root.title = name

    lb = Listbox(master, selectmode=EXTENDED)
    lb.pack()

    Button(root, text="Add", command=lambda: add()).grid(row=1,column=0)
    Button(root, text="Open", command=lambda: root.quit()).grid(row=1, column=1)

    windnd.hook_dropfiles(master, add, force_unicode=True)

    lb.bind('<B1-Motion>', move)
    lb.bind('<Button-1>', select)

    root.mainloop()
    return dataLocations

if __name__ == "__main__":
    print(init())
    input()