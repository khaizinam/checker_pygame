from Client import *
from Player import *
from gamebot import *
from Button import *
from config import *
from Graphic import *
from Board import *
import pygame
import pickle
import os

class SaveLoadSystem:
    def __init__(self, file_extension, save_folder):
        self.fileExtension = file_extension
        self.saveFolder = save_folder
    def saveData(self, data, name):
        dataFile = open(self.saveFolder+"/"+name+self.fileExtension,"wb")
        pickle.dump(data,dataFile)
    def loadFile(self, name):
        dataFile = open(self.saveFolder + "/"+name + self.fileExtension, "rb")
        data = pickle.load(dataFile)
        return data
    def checkFile(self, name):
        return os.path.exists(self.saveFolder + "/"+name + self.fileExtension)