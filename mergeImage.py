#!/usr/bin/env python
# -*- coding: utf-8 -*-
#


import os
import hashlib
import json
import shutil
import gtk
import gobject
import urllib
import re
from sys import path
from gimpfu import *
from gimpenums import *
from time import strftime
import itertools
import copy


# Translation implementation
import locale
import gettext
import gimp


import math
import codecs


APP_NAME = "image"
APP_DIR = gimp.directory # ~/.gimp-2.x
LOCALE_DIR = os.path.join(APP_DIR, 'plug-ins', 'locale') # location of .mo files (e.g. ~/gimp-2.x/plug-ins/locale/fr/LC_MESSAGES/fr.mo)

# Get the default language. On Windows you need to set the LANG variable.
DEFAULT_LANGUAGES = os.environ.get('LANG', '').split(':')
DEFAULT_LANGUAGES += ['en_US']
lc, encoding = locale.getdefaultlocale()
if lc:
    languages = [lc]
languages += DEFAULT_LANGUAGES
mo_location = LOCALE_DIR


# Initialize gettext
gettext.install(True, localedir=LOCALE_DIR, unicode=1)
gettext.find(APP_NAME, mo_location)
gettext.textdomain (APP_NAME)
gettext.bind_textdomain_codeset(APP_NAME, "UTF-8")
language = gettext.translation(APP_NAME, mo_location, languages=languages, fallback=True)

# Define '_' function, so that strings will be with their correct translation.
_ = language.ugettext #use ugettext instead of getttext to avoid unicode errors

def gprint( text ):
   #pdb.gimp_message(text)
   return 

# Main
class Main(gtk.Window):
    # Builds a GTK windows for managing the pages of a book.
    def __init__ (self):
        #global previewSize,isHaveScene
        global localDir
        window = super(Main, self).__init__()
        self.set_title(_("Generate Image"))
        

        localDir= "E:/素材"

        elementH = 30
        winH = elementH*14
        winW = int(winH*0.6)
        self.set_size_request(winW, winH)
        self.set_position(gtk.WIN_POS_CENTER)
        self.set_resizable(False)
        
        GAP = 10
        leftW = winW
        leftBetweenW = int((leftW - 2*GAP)/4)
        leftMidW = int(leftW-2*leftBetweenW-2*GAP-20)
        #lvboxW = leftW - 3*GAP
        
# Label
        labelTips = gtk.Label("请输入语义")
        labelScene = gtk.Label("场景:")
        labelObj = gtk.Label("对象:")
        
        
        labelTips.set_size_request(leftW-2*GAP, elementH)
        labelScene.set_size_request(elementH, elementH)
        labelObj.set_size_request(elementH, elementH)
        
#        labelElement.set_size_request(10, 10)
        
# Button combox
        inputScene = gtk.Entry(30)
        inputObj = gtk.Entry(30)
        btAddScene = gtk.Button("添加")
        btAddObj = gtk.Button("添加")
        mergeBt = gtk.Button("合成图像")
        #combox a special function
        comboxTpl = gtk.combo_box_new_text()
        inputScene.set_size_request(leftMidW, elementH)
        inputObj.set_size_request(leftMidW, elementH)
        btAddScene.set_size_request(elementH, elementH)       
        btAddObj.set_size_request(elementH, elementH)
        mergeBt.set_size_request(int((leftW-3*GAP)/2), elementH)
        comboxTpl.set_size_request(int((leftW-3*GAP)/2), elementH)

        
    
# TreeView
        viewWindow = gtk.ScrolledWindow()
        store = gtk.TreeStore(gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_BOOLEAN)
        treeView = gtk.TreeView(store)
        viewWindow.add(treeView)
        treeView.set_size_request(leftW-3*GAP, int(winH*0.8))
        treeView.set_rules_hint(True)
        self.create_columns(treeView,leftW-2*GAP,store)

#       treeView.connect("cursor-changed",self.previewTreeImg,img,store,previewInfo)

# connect
##      btAddScene.connect("clicked", self.addScene, store, inputScene)
##      btAddObj.connect("clicked", self.addObj, store, inputObj)
        #combox a special function
        comboxTpl.connect('changed', self.comboxChanged,store)
        mergeBt.connect("clicked", self.mergeImg, store)
        
# Arrange
        vboxLeft = gtk.VBox(False,10)
        #hboxScene = gtk.HBox(False, 10)
        #hboxObj = gtk.HBox(False, 10)
        hboxEle = gtk.HBox(False, 10)
        vboxLeft.add(viewWindow)
        vboxLeft.add(hboxEle)
##      vboxLeft.add(labelTips)
        #vboxLeft.add(hboxScene)
        #vboxLeft.add(hboxObj)

        hboxEle.add(mergeBt)
        hboxEle.add(comboxTpl)
##        
##        hboxScene.add(labelScene)
##        hboxScene.add(inputScene)
##        hboxScene.add(btAddScene)
##        
##        hboxObj.add(labelObj)
##        hboxObj.add(inputObj)
##        hboxObj.add(btAddObj)
        
             
# put widgets
        fixed = gtk.Fixed()
        fixed.put(vboxLeft,GAP,GAP)
        self.add(fixed)
        
        
##        global localDir
##        localDir = "D:/素材"
        self.readTpl()
        global tpl
        for t in tpl:
            comboxTpl.append_text(t[1])
            
        comboxTpl.set_active(0)

        self.connect("destroy", gtk.main_quit)
        #fileChooser.connect("destroy", gtk.main_quit)
        self.show_all()
        return window

    
    def create_columns(self, treeView, width, store):
        c1W = int(0.75*width)

        #存ID,但是不显示出来
        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn("ID", rendererText, text=0)
        column.set_reorderable(False)
        column.set_sort_column_id(0)
        column.set_visible(False)
##        column.set_max_width(c1W)
##        column.set_min_width(c1W)
        treeView.append_column(column)
        
        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn("语义", rendererText, text=1)
        column.set_reorderable(False)
        column.set_sort_column_id(1)
        column.set_max_width(c1W)
        column.set_min_width(c1W)
        treeView.append_column(column)
        
        rendererTog = gtk.CellRendererToggle()
        rendererTog.set_property('activatable', True)
        rendererTog.connect( 'toggled', self.toggledChange, treeView, treeView.get_model())
        column = gtk.TreeViewColumn("选择", rendererTog)
        column.add_attribute(rendererTog, "active", 2)
        column.set_max_width(width-c1W)
        column.set_min_width(width-c1W)
        treeView.append_column(column)
        return
    
    def toggledChange(self,cell,path,treeView,model):
        global backgroundId,layerIdlist,curTplBgkTypId
        #path store a path from parent to child e.g: 0:3
        if len(path) == 1:
            return

        #model[path[0]][0] 当前图像的类型ID
        #model[path][0] 当前图像的ID
        #判断当前所选图像是否用作背景
        if curTplBgkTypId == model[path[0]][0]:
            backgroundId = model[path][0]
        else:
            layerIdlist.append(model[path][0])
        
        model[path][2] = not model[path][2]
        return
    
# invalid    
    def addScene(self, widget, store, inputScene):
##        global isHaveScene        
##        text = inputScene.get_text().strip()       
        return


# invalid
    def addObj(self,btAdd,store,inputObj):
##        text = inputObj.get_text().strip()
##        if len(text) != 0:
##            store.append([text,"前景"])
##            inputObj.set_text("")
        return

    def comboxChanged(self,comboxTpl,store):
        global tpl,curTplId,curTplBgkTypId,layerIdlist,backgroundId
        curTplId = None
        backgroundId = None
        layerIdlist = []
        gprint(tpl)
        for l in tpl:
            if l[1] == comboxTpl.get_active_text():
                curTplId = l[0]
                curTplBgkTypId = l[2]
##        gprint(curTplId)
        #根据curTplId查询类型及图，填充数据
        #类型: 指代人物... ..
        #查询过程
        #模板ID-->类型ID-->类型属性和 图像ID
        #图像ID-->图像属性

        #填充以下结构 typList没必要使用字典,模板已定
        #
        #typDict = {类型ID:(类型属性),()...()}  类型属性(name,x,y,w,h)
        #dataDict = {类型ID:[(图像ID,图像属性),(),()...()],...,类型ID:..}

        #gprint(11)
        self.readData()
        self.updateTreeView(store)
        return
    
#fill typeList and imgDict by curTplId
#need fuc: fillTypList and fillImgDict
    def readTpl(self):
        global tpl
        filepath = unicode(localDir+"/config/tpl.txt",'utf8')
        tplFile = open(filepath,'r')
        tpl = []
        try:
            while True:
                #去除换行符s[0]与{比较出错
                line = tplFile.readline()
                
                if not line:
                    break
                #字符串处理
                tplTuple = line.split()
                tplTuple[1] = tplTuple[1].decode('gbk')
                tpl.append((tplTuple[0],tplTuple[1],tplTuple[2]))
        finally:
            tplFile.close()
            
        return
    
    def readData(self):
        gprint("begin readData")
        self.fillTypDict()
        self.fillImgDict()
        gprint("end readData")
        return

    #get typDict: store used typ info
    def fillTypDict(self):
        gprint("begin fillTypList")
        global curTplId,typDict,dataDict
        typDict = {}
        
        #fill typList
        tplTotypPath = unicode(localDir+"/config/tplTotyp.txt",'utf8')
        typPath = unicode(localDir+"/config/typ.txt",'utf8')
        tplTotypFile = open(tplTotypPath,'r')
        typFile = open(typPath,'r')
        
        typID = []
        try:
            #read typ
            while True:
                #
                line = tplTotypFile.readline()
                if not line:
                    break
                
                #fill typList
                tplTotypTuple = line.split()
                if tplTotypTuple[0] == curTplId:
                    typID.append(tplTotypTuple[1])
            #gprint(typID)
                
            #fill typList by typ
            while True:
                line = typFile.readline()
                if not line:
                    break
                typAttribute = line.split()
                #
                if not typAttribute[0] in typID:
                    continue

                #typDict = {类型ID:(类型属性),()...()}  类型属性(name,x,y,w,h)
                typAttribute[1] = typAttribute[1].decode('gbk')
                typDict[typAttribute[0]] = (typAttribute[1],typAttribute[2],typAttribute[3],typAttribute[4],typAttribute[5],typAttribute[6])
            #gprint(typDict)
                
        finally:
            tplTotypFile.close()
            typFile.close()
        gprint("end fillTypList")
        return
    
   
    def fillImgDict(self):
        gprint("begin fillImgDict")
        global curTplId,typDict,dataDict
        dataDict = {}

        #fill imgDict
        typToimgPath = unicode(localDir+"/config/typToimg.txt",'utf8')
        imgPath = unicode(localDir+"/config/img.txt",'utf8')
        typToimgFile = open(typToimgPath,'r')
        imgFile = open(imgPath,'r')
        
        typID = typDict.keys()
        imgs = {}
        typToimgs = {}
        #预先读入img.txt,存入字典imgs备查
        try:
            while True:
                line = imgFile.readline()
                if not line:
                    break

                imgAttribute = line.split()
                imgAttribute[1] = imgAttribute[1].decode('gbk')                
                imgAttribute[2] = imgAttribute[2].decode('gbk')
                imgs[imgAttribute[0]] = (imgAttribute[1],imgAttribute[2])

            #gprint(imgs)
            #预先读入typToimg.txt,中的一部分，用到的类型,存入字典typToimgs备查   
            while True:
                line = typToimgFile.readline()
                if not line:
                    break
                
                lineTuple = line.split()
                if lineTuple[0] in typID:
                    if not lineTuple[0] in typToimgs:     
                        typToimgs[lineTuple[0]] = []
                    typToimgs[lineTuple[0]].append(lineTuple[1])
                    
            #gprint(typToimgs)

            #imgs {图像ID:(图像属性)..} 存有所有图像
            #typToimgs {类型ID:[图像ID]..} 只存有会用到的类型ID
            #typDict = {类型ID:(类型属性),()...()}  类型属性(name,x,y,w,h)
            
            #fill
            #dataDict = {类型ID:[(图像ID,图像属性),(),()...()],...,类型ID:..}
            for typId,typAttribute in typDict.items():
                #一个类型只需要处理一次
                dataDict[typId] = []
                imgIdList = typToimgs[typId]
                for imgid in imgIdList:
                    temp = imgs[imgid]
                    dataDict[typId].append((imgid,temp[0],temp[1]))
                    
            #gprint(dataDict)
        finally:
            imgFile.close()
            typToimgFile.close()
            
        gprint("end fillImgDict")
        return
    
    def updateTreeView(self,store):
        global typDict,dataDict,backgroundId
        
        #
        #typDict = {类型ID:(类型属性),()...()}  类型属性(name,x,y,w,h,order)
        #dataDict = {类型ID:[(图像ID,图像属性),(),()...()],...,类型ID:..}
        store.clear()
        for key,value in dataDict.items():
            typInfo = typDict[key]
            parent = store.append(None, (key,typInfo[0], None) )
            imgList = dataDict[key]
            for img in imgList:
                if typInfo[0] == '背景':
                    store.append( parent, (img[0],img[1], True) )
                    backgroundId = img[0]
                else:
                    store.append( parent, (img[0],img[1], None) )
        
        return
    
    def mergeImg(self,mergeBt,store):
        global isHaveScene,localDir,elementPrm,Semantic
        global backgroundId,layerIdlist,dataDict,curTplBgkTypId,typDict,dataDict
        gprint("begin mergeImg")
        #更新 newImage,layerImageList
        bakimage = None
        bgkImgs = dataDict[curTplBgkTypId]
        for img in bgkImgs:
            if img[0] == backgroundId:
                bakimage = gimp.pdb.gimp_file_load(localDir+img[2],localDir+img[2])
                break
        
        if bakimage == None:
            return     
        
        #gprint(image)
        #elementPrm = [(order,imageId,imageName,imagePath,x,y,x,h),()...()..]
        elementPrm = []
        #gprint(dataDict)
        haveTypIds = [];
        for typId,imgs in dataDict.items():
            for img in imgs:
                if img[0] in layerIdlist:
                    imgAttribute = typDict[typId]
                    elementPrm.append((imgAttribute[5],typId,img[0],img[1],img[2],imgAttribute[1],imgAttribute[2],imgAttribute[3],imgAttribute[4]))
                    haveTypIds.append(typId)

        
        haveTypIds = set(haveTypIds)
        #gprint(elementPrm)
        elementCombines = list(itertools.combinations(elementPrm,len(haveTypIds)))
        #gprint(len(haveTypIds))
        #gprint(elementCombines)
        images = []
        for elements in elementCombines:
            #have [judge] and only have [OK]
            typIds = set([])
            for (order,typId,imgId,name,path,x,y,w,h) in elements:
                typIds.add(typId)
            gprint(typIds)
            if len(typIds) != len(haveTypIds):
                continue
            
            #image = copy.deepcopy(bakimage)
            image = bakimage
            #images.append(image)
            
            elements = list(elements)
            elements.sort(reverse=True)
            #遍历elementPrm，按序添加载入图像
            i = 0
            for (order,typId,imgId,name,path,x,y,w,h) in elements:
                gprint(i)
                i = i + 1
                filePath = localDir+path
                layerName = name+str(imgId)
                l = gimp.pdb.gimp_file_load_layer(image,filePath)
                gimp.pdb.gimp_item_set_name(l,layerName)
                image.add_layer(l)
                gimp.pdb.gimp_layer_scale(l,w,h,TRUE)
                gimp.pdb.gimp_layer_set_offsets(l,x,y)
            # append image into images and clear layers for the next image
            tmp = gimp.pdb.gimp_image_duplicate(image)
            images.append(tmp)
            for layer in image.layers[:-1]:
                image.remove_layer(layer)
        # show image        
        for image in images:            
            gimp.pdb.gimp_display_new(image)
        
        gtk.main_quit()
            
        return
    
# invalid
    def findImg(self,store):
##        global isHaveScene,localDir,elementPrm,Semantic
##        gprint("begin loadImg")
##        if isHaveScene == False:

        return (newImage,layerImageList)
# invalid    
    def initData(self):

##            "刘铁男":("/人物/刘铁男.png",1),
##            "边框":("/边框/边框.png",4),
##            "内容":("/文字/内容.png",5)
##                   }
        
        return
    
# invalid
    def parseConfig(self,backKey,store):
##        global isHaveScene,localDir,elementPrm,Semantic,belongStr
##        gprint("begin parseConfig")
        return
    



# global vars  
    isHaveScene = None
    localDir = None
    # location and size parameter for a specified background
    #[(),()..(type,x,y,w,h)..()]
    elementPrm = []
    belongStr = []
    Semantic = {}

    #comboxChanged modify
    #curTplBgkId current tpl background id
    curTplId = None
    curTplBgkTypId = None
    #main fill
    tpl = []
    typDict = {}
    dataDict = {}
    #newImage and layerImageList存(name,id,path) fill in toggledChange
    backgroundId = None
    layerIdlist = []

#end main
def mergeUser():
    # Display the book window.
    r = Main()
    gtk.main()




# This is the plugin registration function
register(
    "mergeUser",
    _("Tool for managing multiple pages of a comic book, childrens book, sketch book or similar."),
    "GNU GPL v3 or later.",
    "Ragnar Brynjúlfsson",
    "Ragnar Brynjúlfsson",
    _("February 2014"),
    "<Toolbox>/模板成图",
    "",
    [
    ],
    [],
    mergeUser,
)


main()





        
