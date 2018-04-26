#!/usr/bin/env python
# coding:utf-8

class Paging:
    """分页处理父类，有三个参数，一个是当前所在的页码，一个是数据集的模型名称，一个是每页显示的数据条数，默认为10;
        分页处理默认在页面上显示五页，格式结构大致为1...56789...100的格式"""

    def __init__(self, current_page_num, model_name, page_data_num=10):
        """初始化数据,构建实例"""
        self.current_page_num = current_page_num
        self.model_name = model_name
        self.page_data_num = page_data_num

    def get_data_set(self):
        """获取数据集合"""
        return self.model_name.objects.all()

    def get_data_empty(self):
        """判断数据集是否为空"""
        if len(self.get_data_set()):
            return True
        else:
            return False

    def get_page_total(self):
        """获取分页总页码数，如果当前数据集没有数据，则分页页码设为1"""
        data_set = self.get_data_set()
        data_length = len(data_set)
        if data_length != 0:
            if data_length % self.page_data_num == 0:
                return data_length / self.page_data_num
            return data_length / self.page_data_num + 1
        return 1

    def get_current_pagenum(self):
        """处理当前传递的页码数是否符合逻辑，如果不合逻辑，则返回页码为1"""
        page_total = self.get_page_total()
        if int(self.current_page_num) in range(1, page_total+1):
            return int(self.current_page_num)
        return 1

    def get_previous_pagenum(self):
        """判断上一页的页码，如果不合逻辑则返回第一页"""
        current_pagenum = self.get_current_pagenum()
        if current_pagenum - 1 > 0:
            return current_pagenum - 1
        return 1

    def get_next_pagenum(self):
        """判断下一页的页码，如果不合逻辑则返回最后一页"""
        current_pagenum = self.get_current_pagenum()
        page_total = self.get_page_total()
        if current_pagenum + 1 <= page_total:
            return current_pagenum + 1
        return page_total

    def get_first_end(self):
        """判断当前页码到第一页与最后一页之间是否以省略号显示，如果是，则返回1，如果不是，则返回0"""
        current_page_num = self.get_current_pagenum()
        page_total = self.get_page_total()
        if current_page_num > 3 and current_page_num + 2 <= page_total:
            return 1
        return 0

    def get_pagenum_range(self):
        """ 获取分页的页码范围，如果数据集为空，则页码范围为1 """
        current_pagenum = self.get_current_pagenum()
        page_total = self.get_page_total()
        if len(self.get_data_set()):
            if current_pagenum - 2 > 0:
                if current_pagenum + 2 < page_total:
                    return range(current_pagenum - 2, current_pagenum + 2 + 1)
                return range(current_pagenum - 2, page_total + 1)
            if page_total < 6:
                return range(1, page_total + 1)
            return range(1, 6)
        return [1, ]

    def get_current_page_data(self):
        """获取当前页码对应的数据集，返回一个数据的列表"""
        current_pagenum = self.get_current_pagenum()
        data_set = self.get_data_set()
        return data_set[(current_pagenum - 1) * self.page_data_num:current_pagenum * self.page_data_num]
