#!/usr/bin/env python
# -*- coding: utf8 -*-
import sys
import os
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement
from lxml import etree
import codecs

TXT_EXT = '.txt'
ENCODE_METHOD = 'utf-8'

class CDTBWriter:

    def __init__(self, foldername, filename, imgSize, databaseSrc='Unknown', localImgPath=None):
        self.foldername = foldername
        self.filename = filename
        self.databaseSrc = databaseSrc
        self.imgSize = imgSize
        self.boxlist = []
        self.localImgPath = localImgPath
        self.verified = False

    def addRotatedBox(self, points, name, difficult):
        rotatedbox = {'p0x': points[0][0], 'p0y': points[0][1],
                      'p1x': points[1][0], 'p1y': points[1][1],
                      'p2x': points[2][0], 'p2y': points[2][1],
                      'p3x': points[3][0], 'p3y': points[3][1]}
        rotatedbox['name'] = name
        rotatedbox['difficult'] = difficult
        self.boxlist.append(rotatedbox)

    def save(self, classList=[], targetFile=None):

        out_file = None #Update yolo .txt
        out_class_file = None   #Update class list .txt

        if targetFile is None:
            out_file = open(
            self.filename + TXT_EXT, 'w', encoding=ENCODE_METHOD)
            classesFile = os.path.join(os.path.dirname(os.path.abspath(self.filename)), "classes.txt")
            out_class_file = open(classesFile, 'w')

        else:
            out_file = codecs.open(targetFile, 'w', encoding=ENCODE_METHOD)
            classesFile = os.path.join(os.path.dirname(os.path.abspath(targetFile)), "classes.txt")
            out_class_file = open(classesFile, 'w')

        # Song : to save the file as : class_idx: x0 y0; x1 y1; x2 y2; x3 y3
        for box in self.boxlist:
            out_file.write("%d:%.6f %.6f;%.6f %.6f;%.6f %.6f;%.6f %.6f\n" % (classList.index(box['name']),
                                                                                 box['p0x'], box['p0y'],
                                                                                 box['p1x'], box['p1y'],
                                                                                 box['p2x'], box['p2y'],
                                                                                 box['p3x'], box['p3y']))
        for c in classList:
            out_class_file.write(c+'\n')

        out_class_file.close()
        out_file.close()



class CDTBReader:

    def __init__(self, filepath, image, classListPath=None):
        # shapes type:
        # [labbel, [(x1,y1), (x2,y2), (x3,y3), (x4,y4)], color, color, difficult]
        self.shapes = []
        self.filepath = filepath

        if classListPath is None:
            dir_path = os.path.dirname(os.path.realpath(self.filepath))
            self.classListPath = os.path.join(dir_path, "classes.txt")
        else:
            self.classListPath = classListPath

        print (filepath, self.classListPath)

        classesFile = open(self.classListPath, 'r')
        self.classes = classesFile.read().strip('\n').split('\n')

        # print (self.classes)

        imgSize = [image.height(), image.width(),
                      1 if image.isGrayscale() else 3]

        self.imgSize = imgSize

        self.verified = False
        # try:
        self.parseCDTBFormat()
        # except:
            # pass

    def getShapes(self):
        return self.shapes

    def addShape(self, label, points, difficult):
        # points = [(points[0], points[1]), (points[2], points[3]), (points[4], points[5]), (points[6], points[7])]
        self.shapes.append((label, points, None, None, difficult))

    def cdtbLine2Shape(self, classIndex, points):
        label = self.classes[int(classIndex)]

        pt0, pt1, pt2, pt3 = points.split(';')

        x0, y0 = pt0.split(' ')
        x1, y1 = pt1.split(' ')
        x2, y2 = pt2.split(' ')
        x3, y3 = pt3.split(' ')

        P = [(float(x0), float(y0)),
             (float(x1), float(y1)),
             (float(x2), float(y2)),
             (float(x3), float(y3))]

        return label, P

    def parseCDTBFormat(self):
        rotatedBoxFile = open(self.filepath, 'r')
        for rotatedBox in rotatedBoxFile:
            classIndex, points = rotatedBox.split(':')               # points :  x0 y0; x1 y1; x2 y2; x3 y3;
            label, points = self.cdtbLine2Shape(classIndex, points)
            # Caveat: difficult flag is discarded when saved as yolo format.
            self.addShape(label, points, False)
