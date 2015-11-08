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

# Translation implementation
import locale
import gettext
import gimp

import math



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
        global previewSize,imgPreview,localDir
        window = super(Main, self).__init__()
        self.set_title(_("Save Template"))
        
        localDir= "E:/素材"

        winW = int(gtk.gdk.Screen().get_width()*0.85)
        winH = int(gtk.gdk.Screen().get_height()*0.8)
        GAP = 10

        self.set_size_request(winW, winH)
        self.set_position(gtk.WIN_POS_CENTER)
        self.set_resizable(False)

        leftW= int(0.33*winW)
        rightW = int(0.4*winW)
        midW= winW-leftW-rightW -2*GAP
        leftW = leftW-1*GAP
        rightW = rightW-1*GAP
        labelW = int(0.3*(midW-4*GAP))
        btW = int(0.2*(midW-4*GAP))
        entryW = midW - 4*GAP - labelW - btW
        
        eleH = 30
        

# middle of window
        labelComTpl = gtk.Label("图像/类型")
        labelComTpl.set_size_request(labelW,eleH)
        comboxTpl = gtk.combo_box_new_text()
        comboxTpl.set_size_request(entryW,eleH)
        comboxTopic = gtk.combo_box_new_text()
        comboxTopic.set_size_request(btW,eleH)       
        hboxComTpl = gtk.HBox(False, GAP)
        hboxComTpl.add(labelComTpl)
        hboxComTpl.add(comboxTpl)
        hboxComTpl.add(comboxTopic)
        
        labelTpl = gtk.Label("模板命名")
        labelTpl.set_size_request(labelW,eleH)
        entryTpl = gtk.Entry(eleH)
        entryTpl.set_size_request(entryW,eleH)        
        btTpl = gtk.Button("确定")
        btTpl.set_size_request(btW,eleH)
        hboxTpl = gtk.HBox(False, GAP)
        hboxTpl.add(labelTpl)
        hboxTpl.add(entryTpl)
        hboxTpl.add(btTpl)

        labelComLayer = gtk.Label("选择图层")
        labelComLayer.set_size_request(labelW,eleH)
        comboxLayer = gtk.combo_box_new_text()
        comboxLayer.set_size_request(entryW+btW+GAP,eleH)
        hboxComLayer = gtk.HBox(False, GAP)
        hboxComLayer.add(labelComLayer)
        hboxComLayer.add(comboxLayer)
        

        
        labelLayer = gtk.Label("类型命名")
        labelLayer.set_size_request(labelW,eleH)
        entryLayer = gtk.Entry(eleH)
        entryLayer.set_size_request(entryW,eleH)
        btLayer = gtk.Button("确定")
        btLayer.set_size_request(btW,eleH)
        hboxLayer = gtk.HBox(False, GAP)
        hboxLayer.add(labelLayer)
        hboxLayer.add(entryLayer)
        hboxLayer.add(btLayer)

        #selected window 
        windowSelected = gtk.ScrolledWindow()
        #store = gtk.ListStore(gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING)
        store = gtk.ListStore(str,str,str)
        treeView = gtk.TreeView(store)
        windowSelected.add(treeView)
        windowSelected.set_size_request(midW, winH-4*eleH-6*GAP)
        #treeView.set_rules_hint(True)
        self.create_columns(treeView,midW,store)

        # vboxMid 
        vboxMid = gtk.VBox(False,GAP)
        vboxMid.add(hboxComTpl)
        vboxMid.add(hboxTpl)
        vboxMid.add(hboxComLayer)
        vboxMid.add(hboxLayer)
        vboxMid.add(windowSelected)

# right of window
        # FileChooser...
        fileChooser = gtk.FileChooserWidget(gtk.FILE_CHOOSER_ACTION_OPEN)
        fileChooserW = int(rightW)
        fileChooserH = int(winH*0.85)
        fileChooser.set_size_request(fileChooserW,fileChooserH)
        fileChooser.add_shortcut_folder(localDir)

        filter = gtk.FileFilter()
        filter.set_name("Images")
        filter.add_mime_type("image/png")
        filter.add_mime_type("image/jpeg")
        filter.add_pattern("*.png")
        filter.add_pattern("*.jpg")
        fileChooser.add_filter(filter)

        hboxRadio = gtk.HBox(False, GAP)
        #self.createRadio(hboxRadio,rightW,eleH)

        mergeBt = gtk.Button("保存模板")
        mergeBt.set_size_request(rightW, eleH)

        # vboxRight
        vboxRight = gtk.VBox(False,GAP)
        vboxRight.add(fileChooser)
        vboxRight.add(hboxRadio)
        vboxRight.add(mergeBt)

# left of window 
        
        imgPreview = gtk.Image()
        imgPreview.set_size_request(leftW, int(winH*0.8))
        labelImgInfo = gtk.Label("北航欢迎您")
        labelImgInfo.set_size_request(leftW, eleH)
        
        # vboxLeft
        vboxLeft = gtk.VBox(False,GAP)
        vboxLeft.add(imgPreview)
        #vboxLeft.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(6400, 6400, 6440))
        vboxLeft.add(labelImgInfo)
        
# put widgets
        fixed = gtk.Fixed()
        fixed.put(vboxLeft,GAP,GAP) #control,x,y
        fixed.put(vboxMid,leftW+2*GAP,GAP)
        fixed.put(vboxRight,leftW+midW+3*GAP,GAP)

        self.add(fixed)
        
# connect
        fileChooser.connect("update-preview", self.previewImg,imgPreview,labelImgInfo)
        fileChooser.connect("file-activated", self.addImg,store)
        
        treeView.connect("cursor-changed", self.previewTreeImg,imgPreview,store,labelImgInfo)
        treeView.connect("row-activated", self.removeImg,treeView,store)
        
        comboxTpl.connect('changed', self.comboxTplChanged,comboxLayer,entryTpl)
        comboxTopic.connect('changed', self.comboxTopicChanged)
        comboxLayer.connect('changed', self.comboxLayerChanged,store,entryLayer)
        
        
        mergeBt.connect('clicked',self.createTpl)
        btTpl.connect('clicked',self.changeTplName,entryTpl)
        btLayer.connect('clicked',self.changeLayerName,entryLayer)
 
               
# init data
        previewSize = (leftW,int(winH*0.8))
        #imgPreview = None
        global xcfEdits,tplName,numTpls
        
        tplName = []
        self.initData()
        
        numTpls = 0
        for ixcf in xcfEdits:
            fileName = gimp.pdb.gimp_image_get_filename(ixcf)
            name = os.path.basename(fileName) 
            comboxTpl.append_text(name)
            numTpls = numTpls + 1
            names = name.split('.')
            tplName.append(names[0])
        comboxTpl.set_active(0)
        
        topics = {"1":"东山","2":"台球","3":"南瓜","4":"热水"}
        for (topicid,topic) in topics.items():
            comboxTopic.append_text(topic)
        comboxTopic.set_active(0)
        #global curTopic
        #curTopic = "东海"
              
        #tplName = gimp.pdb.gimp_image_get_filename(xcfEdits[0])
        
        

        
##      curFilename = "D:/素材/default.jpg" layerName
##      imgBuf = gtk.gdk.pixbuf_new_from_file(curFilename)
##
##      imgBuf = imgBuf.scale_simple(leftW,int(winH*0.8),gtk.gdk.INTERP_NEAREST)
##      imgPreview.set_from_pixbuf(imgBuf)
##      imgPreview.show()

        ####comboxTpl.set_active(0)

        self.connect("destroy", gtk.main_quit)
        #fileChooser.connect("destroy", gtk.main_quit)
        self.show_all()
        return window

    def initData(self):
        global previewSize,imgPreview,localDir,xcfEdits,isHaveBack
        curFilename = localDir+"/default.jpg"
        imgBuf = gtk.gdk.pixbuf_new_from_file(curFilename)
        gprint(curFilename)
        imgBuf = imgBuf.scale_simple(previewSize[0],previewSize[1],gtk.gdk.INTERP_NEAREST)
        imgPreview.set_from_pixbuf(imgBuf)

        gprint('a')

        #获取当前打开的所有图像
        xcfEdits = gimp.image_list()
        isHaveBack = None
##        fileName = gimp.pdb.gimp_image_get_filename(xcfEdits[0])
##        name = os.path.basename(fileName) 
##        gprint(name)
##        layers = xcfEdits[1].layers
        
        return
    
    def create_columns(self, treeView, width, store):
        c1W = int(0.75*width)

        #存ID,但是不显示出来
        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn("path", rendererText, text=0)
        column.set_reorderable(False)
        column.set_sort_column_id(0)
        column.set_visible(False)
##      column.set_max_width(c1W)
##      column.set_min_width(c1W)
        treeView.append_column(column)
        
        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn("图像", rendererText, text=1)
        column.set_reorderable(False)
        column.set_sort_column_id(1)
        column.set_max_width(c1W)
        column.set_min_width(c1W)
        treeView.append_column(column)

        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn("类型", rendererText, text=2)
        column.set_reorderable(False)
        column.set_sort_column_id(2)
        column.set_max_width(width-c1W)
        column.set_min_width(width-c1W)
        treeView.append_column(column)

        return


    def createRadio(self,hbox,width,eleH):
        labelTemp = gtk.Label("")
        labelTemp.set_size_request(int(width*0.5), eleH)
        hbox.pack_start(labelTemp, True, True, 0)
        button = gtk.RadioButton(None, "前景")
        #button.connect("toggled", self.radioCallBack, "前景")
        hbox.pack_start(button, True, True, 0)
        button.show()
        

        button = gtk.RadioButton(button, "背景")
        #button.connect("toggled", self.radioCallBack, "背景")
        button.set_active(True)
        hbox.pack_start(button, True, True, 0)
        button.show()

    def radioCallBack(self,widget,data):
        #global typBf
        #typBf = data
        
        return

   # plot
    def comboxTplChanged(self,comboxTpl,comboxLayer,entryTpl):
        global xcfEdits,curXcf,typDict,typToimgs,curTypId,curTplId,typBf,numLayers,tplName,layerName,numTpls

        comboxLayer.get_model().clear()


        tid = comboxTpl.get_active()
        entryTpl.set_text(tplName[tid])
        curTplId = tid
     
        layerName = []
        curTypId = None
        typToimgs = {}
        curXcf = None
        for ixcf in xcfEdits:
            fileName = gimp.pdb.gimp_image_get_filename(ixcf)
            name = os.path.basename(fileName)
            if name == comboxTpl.get_active_text():
                curXcf = ixcf
                break
        
        typDict = {}
        index = 0
        ##gimp-image-get-layer-by-name
        ##gimp-image-get-layer-position  The position of the item in its level in the item tree
        ##gimp-image-grid-get-offset
        ##gimp-image-grid-get-spacing
        for layer in curXcf.layers:
            name = gimp.pdb.gimp_item_get_name(layer)
            # 图层名作为模板中该层类型名
            comboxLayer.append_text(name)
            temp = gimp.pdb.gimp_image_get_layer_position(curXcf,layer)
            offset = gimp.pdb.gimp_drawable_offsets(layer)
            width = gimp.pdb.gimp_drawable_width(layer)
            height = gimp.pdb.gimp_drawable_height(layer)
            typDict[index] = (name,offset[0],offset[1],width,height,index)#{id:(name,x,y,w,h,order)...
            typToimgs[index] = [] # {id:[(图像path,图像name,背景or前景)....],id:....
            names = name.split('.')
            layerName.append(names[0])
            index = index + 1

            
        numLayers = index
        comboxLayer.set_active(0)
        curTypId = 0
        if numLayers == 1:
            typBf = "背景"
        else:
            typBf = "前景"
            
        return

    def comboxTopicChanged(self,comboxTopic):
        global curTopicId
        curTopicId = comboxTopic.get_active()
        curTopicId = int(curTopicId) + 1
        return


    def comboxLayerChanged(self,comboxLayer,store,entryLayer):
        global curTypId,typToimgs,typBf,numLayers,layerName
        curTypId = comboxLayer.get_active()
        
        #gprint(layerName)
        #gprint(curTypId)
        #gprint(layerName[curTypId])
        entryLayer.set_text(layerName[curTypId])
        if curTypId == numLayers-1 or numLayers == 1:
            typBf = "背景"
        else:
            typBf = "前景"
        
        store.clear()
        # update treeview
        for (tpath,tname,ttypBf) in typToimgs[curTypId]:
            if ttypBf == "背景":
                store.insert(0,[tpath,tname,ttypBf])
            else:
                store.append([tpath,tname,ttypBf])
        
        return

    def previewImg(self,widget,img,previewInfo):
        global curFilename,previewSize
        imgTemp = gtk.Image()
        curFilename = widget.get_preview_filename()
        if curFilename != None:
            imgTemp.set_from_file(curFilename)
        imgBuf = imgTemp.get_pixbuf()
        previewInfo.set_text(str(imgBuf.get_width())+"×"+str(imgBuf.get_height()))
        imgBuf = imgBuf.scale_simple(previewSize[0],previewSize[1],gtk.gdk.INTERP_NEAREST)
        img.set_from_pixbuf(imgBuf)
        

    def previewTreeImg(self,widget,img,store,previewInfo):
        global previewSize
        selection = widget.get_selection()
        a,toRemove = selection.get_selected()
        t = store.get_value(toRemove,0)
        imgTemp = gtk.Image()
        imgTemp.set_from_file(store.get_value(toRemove,0))
        if imgTemp == None:
            return
        imgBuf = imgTemp.get_pixbuf()
        previewInfo.set_text(str(imgBuf.get_width())+"×"+str(imgBuf.get_height()))
        imgBuf = imgBuf.scale_simple(previewSize[0],previewSize[1],gtk.gdk.INTERP_NEAREST)
        img.set_from_pixbuf(imgBuf)


    def addImg(self,fileChooser,store):
        global typBf,isHaveBack,curTypId,typToimgs,localDir

        path = fileChooser.get_filename()
    
        if path == None:
            return
        
        allname = os.path.basename(path)
        names = allname.split('.')
        name = names[0]
        
        # guarantee only have one back..        
        if isHaveBack and typBf == "背景":
            item = store.get_iter_first()
            while True:
                if item == None:
                    break
                if store.get_value(item,2) == "背景":
                    store.remove(item)
                    typToimgs[curTypId]= []
                    break
                item = store.iter_next(item)
                
        # background img always insert 0                
        if typBf == "背景":
            isHaveBack = True
            store.insert(0,[path,name,typBf])
        else:
            store.append([path,name,typBf])
        typToimgs[curTypId].append([path,name,typBf])
        
        return

# Stroe data will have error after creatTpl
    def removeImg(self,removeImg, path, view_column, treeView,store):
        global typToimgs,curTypId
        selection = treeView.get_selection()
        a,toRemove = selection.get_selected()
        #gprint(1)
        for (tpath,tname,ttypBf) in typToimgs[curTypId]:
            gprint(store.get_value(toRemove,0))
            gprint(tpath)
            if store.get_value(toRemove,0) == tpath:
                #gprint(21)
                store.remove(toRemove)
                typToimgs[curTypId].remove([tpath,tname,ttypBf])
                break

        return

        
#####        
    def createTpl(self,widget):
        global typToimgs,typDict,localDir,layerName

        # handle path. copy image which is not in localDir meantime
        # copy to folder localDir+'/imgTyp'
        for key,imgs in typToimgs.items():
            for index,(tpath,tname,ttypBf) in enumerate(imgs):
                #gprint(111111)
                #gprint(tpath)
                tlocalDir=localDir.replace('/','\\')
                typName = layerName[key]
                timgDir = os.path.join(tlocalDir, typName)
                
                #timgDir = tlocalDir+'\\'+typName
##                gprint(tpath)
##                gprint(timgDir)
##                gprint(tpath.find(timgDir))
                if tpath.find(timgDir) == -1:
                    # copy image to typName folder if it is not in localDir
                    # 判断改路径 localDir/typName 是否已经存在
                    if not os.path.exists(unicode(timgDir,'utf8')):
                        os.mkdir(unicode(timgDir,'utf8'))
                    
                    # copy
                    #gprint(tpath)
                    filename = os.path.basename(tpath)
                    #gprint(timgDir+'\\'+filename)
                    shutil.copyfile(unicode(tpath,'utf8'), unicode(timgDir+'\\'+filename,'utf8'))
                    #gprint(122)
                    tpath = timgDir+'\\'+filename
                    
                # replace
                tpath = tpath.replace('\\','/')
                tpath = tpath.replace(localDir,'')     
                typToimgs[key][index][0] = tpath

        self.saveData()
        gtk.main_quit()

        return
    
    def saveData(self):
        (tplID,typID,imgID) = self.readInfo()
        #gprint([tplID,typID,imgID])
        
        self.writeInfo(tplID,typID,imgID)
        return
    

    def readInfo(self):
        global localDir
        tplFile = open(unicode(localDir+"/config/tpl.txt",'utf8'),'r')
        typFile = open(unicode(localDir+"/config/typ.txt",'utf8'),'r')
        imgFile = open(unicode(localDir+"/config/img.txt",'utf8'),'r')
        try:
            #read
            lines = tplFile.readlines()
            if len(lines) == 0:
                tplID = 0
            else:
                eles = lines[len(lines)-1].split()
                tplID = int(eles[0].strip())+1

            lines = typFile.readlines()
            if len(lines) == 0:
                typID = 0
            else:
                eles = lines[len(lines)-1].split()
                typID = int(eles[0].strip())+1

            lines = imgFile.readlines()
            if len(lines) == 0:
                imgID = 0
            else:
                eles = lines[len(lines)-1].split()
                imgID = int(eles[0].strip())+1
            
        finally:
            #process
            tplFile.close()
            typFile.close()
            imgFile.close()
            
        return (tplID,typID,imgID)

    def writeInfo(self,tplID,typID,imgID):
        global typToimgs,typDict,localDir,layerName,curTplId,curTopicId
##      typDict[index] = (name,offset[0],offset[1],width,height,index)#{id:(name,x,y,w,h,order)...
##      typToimgs[index] = [] # {id:[(图像path,图像name,背景or前景)....],id:....
        tplFile = open(unicode(localDir+"/config/tpl.txt",'utf8'),'a')
        typFile = open(unicode(localDir+"/config/typ.txt",'utf8'),'a')
        imgFile = open(unicode(localDir+"/config/img.txt",'utf8'),'a')
        tplTotypFile = open(unicode(localDir+"/config/tplTotyp.txt",'utf8'),'a')
        typToimgFile = open(unicode(localDir+"/config/typToimg.txt",'utf8'),'a')
        
        
        try:
            #process
            # write typ.txt
            for ttypid,(tname,x,y,w,h,order) in typDict.items():
                line = '\n'+str(typID+ttypid)+' '+layerName[ttypid]+' '+str(x)+' '+str(y)+' '+str(w)+' '+str(h)+' '+str(order)
                typFile.write(line.encode('gbk'))

            # write img.txt typToimg.txt and get bgkid meantime
            imgIdCount = 0
            gbkId = 0
            for ttypid,imgs in typToimgs.items():
                for (tpath,tname,ttypBf) in imgs:
                    lineImg = '\n'+str(imgID+imgIdCount)+' '+tname+' '+tpath
                    imgFile.write(lineImg.encode('gbk'))
                    if ttypBf == '背景':
                        gbkId = typID+ttypid
                    lineTypToimg = '\n'+str(typID+ttypid)+' '+str(imgID+imgIdCount)
                    typToimgFile.write(lineTypToimg.encode('gbk'))
                    imgIdCount = imgIdCount + 1
                                               
            # write tpl.txt
            line = '\n'+str(tplID)+' '+tplName[curTplId]+' '+str(gbkId)+' '+str(curTopicId)
            tplFile.write(line.encode('gbk'))
            
            # tplTotyp
            typIdList = typDict.keys()
            for tid in typIdList:
                line = '\n'+str(tplID)+' '+str(typID+tid)
                tplTotypFile.write(line.encode('gbk'))

        
                          
        finally:
            tplFile.close()
            typFile.close()
            imgFile.close()
            tplTotypFile.close()
            typToimgFile.close()

        return


    def changeTplName(self,btTpl,entryTpl):
        global tplName,curTplId
        tplName[curTplId] = entryTpl.get_text().strip()
        return

    def changeLayerName(self,btLayer,entryLayer):
        global layerName,curTypId,typDict
        layerName[curTypId] = entryLayer.get_text().strip()
        return



# data
    previewSize = ()
    imgPreview = None
    localDir= None
    xcfEdits = None
    curXcf = None
    curTypId = None
    curTplId = None
    curTopicId = None
    numTpls = None
    numLayers = None
    typDict = {}
    typBf = None
    isHaveBack = None
    tplName = []
    layerName = []
    typToimgs = {}
    
    
    table = {}


#end main
def saveTpl():
    # Display the book window.
    r = Main()
    gtk.main()




# This is the plugin registration function
register(
    "saveTpl",
    _("Tool for managing multiple pages of a comic book, childrens book, sketch book or similar."),
    "GNU GPL v3 or later.",
    "Ragnar Brynjúlfsson",
    "Ragnar Brynjúlfsson",
    _("February 2014"),
    "<Toolbox>/存为模板",
    "",
    [
    ],
    [],
    saveTpl,
)


main()



