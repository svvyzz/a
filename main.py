#создай тут фоторедактор Easy Editor!
import os
from PyQt5.QtWidgets import(
    QApplication, QWidget, QFileDialog, 
    QLabel, QPushButton, QListWidget, 
    QHBoxLayout, QVBoxLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont

from PIL import Image, ImageEnhance, ImageOps
from PIL.ImageQt import ImageQt
from PIL.ImageFilter import *

app = QApplication([])
win = QWidget()
win.resize(700,400)
win.setWindowTitle('Easy Editor')

Ib_image = QLabel('Картинка')
btn_dir = QPushButton('Папка')
lw_files = QListWidget()
btn_l = QPushButton('Лево')
btn_r = QPushButton("Право")
btn_mr = QPushButton("Зеркало")
btn_rez = QPushButton("Резкость")
btn_bw = QPushButton("Ч/Б")

btn_ram = QPushButton('Рамка')
btn_Brt = QPushButton('+ яркость')
btn_brt = QPushButton('- яркость')
btn_cntr = QPushButton('Контраст')
btn_rel = QPushButton('Рельеф')

btn_l.setFont(QFont('Times', 16, QFont.Bold))
btn_r.setFont(QFont('Times', 16, QFont.Bold))
btn_mr.setFont(QFont('Times', 16, QFont.Bold))
btn_rez.setFont(QFont('Times', 16, QFont.Bold))
btn_bw.setFont(QFont('Times', 16, QFont.Bold))
btn_rel.setFont(QFont('Times', 16, QFont.Bold))

btn_ram.setFont(QFont('Times', 16, QFont.Bold))
btn_dir.setFont(QFont('Times', 16, QFont.Bold))
btn_Brt.setFont(QFont('Times', 16, QFont.Bold))
btn_brt.setFont(QFont('Times', 16, QFont.Bold))
btn_cntr.setFont(QFont('Times', 16, QFont.Bold))


btn_l.setStyleSheet('background: rgb(200, 100, 200)')
btn_r.setStyleSheet('background: rgb(200, 100, 200)')
btn_mr.setStyleSheet('background: rgb(200, 100, 200)')
btn_rez.setStyleSheet('background: rgb(200, 100, 200)')
btn_bw.setStyleSheet('background: rgb(200, 100, 200)')
btn_rel.setStyleSheet('background: rgb(200, 100, 200)')

btn_ram.setStyleSheet('background: rgb(200, 100, 200)')
btn_dir.setStyleSheet('background: rgb(150, 220, 130)')
btn_Brt.setStyleSheet('background: rgb(200, 100, 200)')
btn_brt.setStyleSheet('background: rgb(200, 100, 200)')
btn_cntr.setStyleSheet('background: rgb(200, 100, 200)')


layout1 = QVBoxLayout()
layout2 = QHBoxLayout()
layout02 = QHBoxLayout()
layout3 = QHBoxLayout()
layout4 = QVBoxLayout()

layout1.addWidget(btn_dir)
layout1.addWidget(lw_files)
layout2.addWidget(Ib_image)
layout2.addWidget(btn_l, alignment= Qt.AlignBottom)
layout2.addWidget(btn_r, alignment= Qt.AlignBottom)
layout2.addWidget(btn_mr, alignment= Qt.AlignBottom)
layout2.addWidget(btn_rez, alignment= Qt.AlignBottom)
layout2.addWidget(btn_bw, alignment= Qt.AlignBottom)
layout2.addWidget(btn_rel, alignment= Qt.AlignBottom)
layout02.addWidget(btn_ram)
layout02.addWidget(btn_brt)
layout02.addWidget(btn_Brt)
layout02.addWidget(btn_cntr)

layout4.addLayout(layout2)
layout4.addLayout(layout02)
layout3.addLayout(layout1, 20)
layout3.addLayout(layout4, 80)

win.setLayout(layout3)

workdir = ''

def filter(filenames, extensions):
    result = []
    for filename in filenames:
        for extension in extensions:
            if filename.endswith(extension):
                result.append(filename)
    return result

def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def showFilenamesList():
    extensions  = ['.jpg', '.png', '.jpeg', '.gif', '.bmp']
    chooseWorkdir()
    filenames = filter(os.listdir(workdir), extensions)

    lw_files.clear()
    for files in filenames:
        lw_files.addItem(files)

btn_dir.clicked.connect(showFilenamesList)  

class ImageProcessor():
    def __init__(self):
        self.image = None
        self.filename = None
        self.save_dir = 'Modified/'
    def loadImage(self, filename):
        self.filename = filename
        image_path = os.path.join(workdir, filename)
        self.image = Image.open(image_path)

    def showImage(label, path):
        Ib_image.hide()
        pixmapimage = QPixmap(path)
        w,h = Ib_image.width(), Ib_image.height()
        pixmapimage = pixmapimage.scaled(w,h,Qt.KeepAspectRatio)
        Ib_image.setPixmap(pixmapimage)
        Ib_image.show()

    def saveImage(self):
        path = os.path.join(workdir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)

    def do_bw(self):
        self.image = self.image.convert('L')
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    
    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_mirror(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    
    def do_rez(self):
        self.image = self.image.filter(SHARPEN)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_ram(self):
        self.image = ImageOps.expand(self.image, border=(10,10,10,10), fill = 'yellow')
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_brt(self):
        self.image = ImageEnhance.Brightness(self.image).enhance(0.5)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_Brt(self):
        self.image = ImageEnhance.Brightness(self.image).enhance(1.5)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_cntr(self):
        self.image = ImageEnhance.Contrast(self.image).enhance(1.5)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)    

    def do_rel(self):
        self.image = self.image.filter(EMBOSS)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

workimage = ImageProcessor()

def showChosenImage():
    if lw_files.currentRow() >= 0:
        filename = lw_files.currentItem().text()
        workimage.loadImage(filename)
        image_path = os.path.join(workdir, workimage.filename)
        workimage.showImage(image_path)

lw_files.currentRowChanged.connect(showChosenImage)

btn_bw.clicked.connect(workimage.do_bw)
btn_l.clicked.connect(workimage.do_left)
btn_r.clicked.connect(workimage.do_right)
btn_mr.clicked.connect(workimage.do_mirror)
btn_rez.clicked.connect(workimage.do_rez)
btn_ram.clicked.connect(workimage.do_ram)
btn_Brt.clicked.connect(workimage.do_Brt)
btn_brt.clicked.connect(workimage.do_brt)
btn_cntr.clicked.connect(workimage.do_cntr)
btn_rel.clicked.connect(workimage.do_rel)

win.showMaximized()
app.exec()