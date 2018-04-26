#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import csv


class CsvResolve(object):
    """
    CSV文件处理,接收一个UploadFile对象
    """
    def __init__(self, fobject):
        self.fobject = fobject
        self.csv_row_data = []

    def csv_read(self):
        reader = csv.reader(self.fobject)
        for row in reader:
            self.csv_row_data.append(row)
        self.fobject.close()
        return self.csv_row_data
