'''
Created on Feb 13, 2011

@author: mattf
'''
import Tkinter as Tk


class Graph2D(Tk.Frame):
    
    def __init__(self, master, xMax, yMax, windowWidth = 600, windowHeight = 600):
        Tk.Frame.__init__(self)
        self.grid()

        self.width = windowWidth
        self.height = windowHeight
        self.xMax = xMax
        self.yMax = yMax
        self.xBump = 4
        
        self.can = Tk.Canvas(self, bg = 'white', width = self.width, height = self.height)
        self.can.grid()

        
    def addPoint(self, point):
        (xi,yi) = point.getCoordinates()
        x = 1. * xi * self.width / self.xMax + self.xBump
        y = 1. * (self.height / self.yMax) * (self.yMax - yi)
        self.can.create_oval(x - 1, y - 1, x + 1, y + 1, width = 2, outline = 'red')
        


        