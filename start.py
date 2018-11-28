#! /usr/bin/env python3
from scanfunc import scan_func
import os


def start():
    func_list=[]
    path="/home/tet/test_sets/workspace/glibc-2.23/"
    with open("./result.csv","w") as result:
        # result.write("|函数名|返回值|参数类型|\n")
        # result.write("|-----|-----|-----|\n")
        for root,dir,file in os.walk(path):
            for filename in file:
                if filename[-2:]==".h":
                    scan_func(os.path.join(root,filename),func_list,result)

if __name__=="__main__":
    start()