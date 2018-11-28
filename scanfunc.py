import os,re,gc

# 这个函数一次只扫描一个文件
def scan_func(path,func_list,result):
    # 读取文件内的所有内容
    # 且全部保存到内存中
    with open(path,"rb") as e:
        # 对于非utf8格式编码出错的问题,这里暂时忽略掉这个文件
        try:
            filestr=e.read().decode(encoding="utf-8")
        except UnicodeDecodeError:
            print(path)
            return
    # 第一步先去掉注释,以免误判
    annotation=re.compile(r"(/\*.*?\*/)|(//.*?\n)", re.S)
    filestr=annotation.sub("",filestr)
    # 第二步开始从中读取函数
    function=re.compile(r"extern\s+([\w\s]*?)[\s\*]+(\w+)\s+\(([^\)]*?)\)(;|(\s*__.*?;))",re.S)
    func_iter=function.finditer(filestr)
    # 清理内存
    del filestr
    gc.collect()
    # 对每个函数进行操作,
    # 首先提取出函数的函数名
    # 然后在函数列表中查找,如果有的话就不管了
    for iter in func_iter:
        if iter.group(2) not in func_list:
            func_list.append(iter.group(2))
            func_name=iter.group(2)
            func_ret=iter.group(1)
            func_pam=re.sub("\s+"," ",iter.group(3))
            result.write("{},{},\"{}\",".format(func_name,func_ret,func_pam))
            result.write("\n")
    
