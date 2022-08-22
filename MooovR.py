#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, uic
import os, sys
import glob
import shutil, pathlib

class Ui(QtWidgets.QMainWindow):

    op1 = op2 = op = ''

    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi(r'C:\Users\sul00\Desktop\MooovR.ui', self)
        self.show()
        self.start_moving.clicked.connect(self.startMooovR)
        
    def get_files(self, path):
        filenames = []
        files = glob.glob(path + '\**', recursive=True)
        for file in files:
            filenames.append(file)
        return filenames
        
    def copyFile(self, src,dst,buffer_size=10485760,perserveFileDate=True):
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
        p = ''
        files = self.get_files(src)
        for each_file in files:
            if os.path.isfile(each_file):
                p = pathlib.Path(each_file)
                dst_new = dst + '\\'+str(pathlib.Path(*p.parts[2:]))
                self.copyFile(each_file, dst_new)
                print ('Copying ', each_file, ' .....', 'to ', dst_new)

    def getSrc(self):
        srcs = self.srcF.toPlainText().split("\n")
        srcs.pop()
        print ("sources: ", srcs, len(srcs)) 
        return srcs
    
    def getDst(self):
        dsts = self.dstF.toPlainText().split("\n")
        print ("destinations: ", dsts) 
        return dsts
    
    def getTotalFiles(self, src_list):
        count = 0
        for file_path in src_list:
            count = count + len(self.get_files(file_path))
        return count
    
    def startMooovR(self):

        src = self.getSrc()
        total_files = self.getTotalFiles(src)
        dst = self.getDst()
        
        for it, i in enumerate(src):
            if os.path.isdir(i):
                for j in range(len(dst)):
                    self.cpDir(i, dst[j])
            else:
                for j in range(len(dst)):
                    self.copyFile(i,dst[j])
            self.mooovr_progress.setValue(floor((total_files/(it+1))))
        
app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
