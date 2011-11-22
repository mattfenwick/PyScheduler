'''
Created on Feb 13, 2011

@author: matt
'''
import Graph as g
import Tkinter as Tk


def displayPoints(schedule, xmax, ymax):
    frame = Tk.Tk()
    graph = g.Graph2D(frame, xmax, ymax)
    frame.title('Schedule')
    frame.geometry('700x680+150+5')
    for point in schedule.getPoints():
        graph.addPoint(point)
    frame.mainloop()
        
        