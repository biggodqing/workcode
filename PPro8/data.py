# -*- coding: utf-8 -*-
# @Time    : 2018/3/19 11:07
# @Author  : tao.shao
# @File    : data.py


class Base(object):
    TimeKey = ""
    last_time = ""

    def add(self, data):
        if self.last_time < data[self.TimeKey]:
            self._add(data)



