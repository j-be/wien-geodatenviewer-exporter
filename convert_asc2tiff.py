#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import os

from PyQt4.QtGui import QImage, QPainter, QColor
from PyQt4.QtCore import QSize

from qgis.core import *

def getLayer(path, name):
	print "Load ", name
	ret = QgsRasterLayer(path, name)
	if ret.isValid():
		print "    ... is valid"
		QgsMapLayerRegistry.instance().addMapLayer(ret)
	else:
		print "    ERROR: " + path

	return ret

def renderLayers(size, layers, imageFileName):
	# create image
	img = QImage(size, QImage.Format_RGB32)


	# set image's background color
	color = QColor(255,255,255)
	img.fill(color.rgb())


	# create painter
	p = QPainter()
	p.begin(img)
	p.setRenderHint(QPainter.Antialiasing)

	render = QgsMapRenderer()

	# set layer set
	render.setLayerSet(layers.keys())

	# set extent
	rect = QgsRectangle(render.fullExtent())
	render.setExtent(rect)

	# set output size
	render.setOutputSize(img.size(), img.logicalDpiX())

	print "render()"
	# do the rendering
	render.render(p)
	p.end()
	print "    ...Done"

	print "save()"
	# save image
	img.save(imageFileName)
	print "    ...Done"

def load_layers():
	ascFolder = os.getcwd() + "/asc/"
	files = os.listdir(ascFolder)
	for fileName in files:
		if fileName.endswith(".asc"):
			getLayer(ascFolder + fileName, fileName)

if __name__ == "__main__":

	print "initQgis"
	qgishome = "/usr"
	QgsApplication.setPrefixPath(qgishome, True)
	QgsApplication.initQgis()

	print "    ...Done"

	load_layers()

	style='templatestyle.qml'
	print "Set style:", style
	for layer in QgsMapLayerRegistry.instance().mapLayers().values():
		layer.loadNamedStyle(style)
	print "    ...Done"

	# Render all loaded layers (works with project files to)
	renderLayers(QSize(2049,2049), QgsMapLayerRegistry.instance().mapLayers(), "./out/multipatch.tiff")

	print "exit"
	QgsApplication.exitQgis()