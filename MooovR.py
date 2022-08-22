#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, uic
import os, sys
import glob
import shutil, pathlib

class Ui(QtWidgets.QMainWindow):
    
    progres = flag = 0
    
    def __init__(self):
        
        super(Ui, self).__init__()
        uic.loadUi(r'.\MooovR.ui', self)
        self.show()
        self.srcF.setFocus()
        self.start_moving.clicked.connect(self.startMooovR)
        
    def get_files(self, path):
        
        filenames = []
        files = glob.glob(path + '\**', recursive=True)
        for file in files:
            filenames.append(file)
        return filenames
        
    def copyFile(self, src,dst,buffer_size=10485760,perserveFileDate=True):
        
        self.flag +=1
        self.filename.setText(src)
        self.mooovr_progress.setValue(int((self.flag/self.progres)*100))
        (dstParent, dstFileName) = os.path.split(dst)
        if not os.path.exists(dstParent):
            os.makedirs(dstParent)
        buffer_size = min(buffer_size, os.path.getsize(src))
        if buffer_size == 0:
            buffer_size = 1024
        if shutil._samefile(src, dst):
            raise shutil.Error('`%s` and `%s` are the same file' % (src,dst))
        for fn in [src, dst]:
            try:
                st = os.stat(fn)
            except OSError:
                pass
        else:
            if shutil.stat.S_ISFIFO(st.st_mode):
                raise shutil.SpecialFileError('`%s` is a named pipe'% fn)
        with open(src, 'rb') as fsrc:
            with open(dst, 'wb') as fdst:
                shutil.copyfileobj(fsrc, fdst, buffer_size)
        if perserveFileDate:
            shutil.copystat(src, dst)
            
    def cpDir(self, src, dst):
        
        files = self.get_files(src)
        for each_file in files:
            if os.path.isfile(each_file):
                dst_new = self.get_new_dst_path(src, each_file, dst)
                self.copyFile(each_file, dst_new)
        
    def get_new_dst_path(self, input_folder, new, dst):
        
       sp = list(pathlib.Path(input_folder).parts)
       spn = list(pathlib.Path(new).parts)
       stem_index_insource = len(sp) -1
       spn = spn[stem_index_insource:]
       return os.path.join(dst, *spn)
    
    def getTotalFiles(self, src_list):
        count = 0
        for file_path in src_list:
            count = count + len(self.get_files(file_path))
        return count
    
    def startMooovR(self):
        
        self.mooovr_progress.setValue(0)
        src = self.srcF.toPlainText().split("\n")
        dst = self.dstF.toPlainText().split("\n")
        
        if src[0] == "":
            print("No input or output destinations specified!")
            sys.exit(1)

        self.progres = int(self.getTotalFiles(src))
            
        for it, i in enumerate(src):
            if os.path.isdir(i):
                for j in range(len(dst)):
                    self.cpDir(i, dst[j])
            else:
                for j in range(len(dst)):
                    self.copyFile(i,os.path.join(dst[j], pathlib.Path(i).name))
        self.mooovr_progress.setValue(100)
        self.flag = 0
        
app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
