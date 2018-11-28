import os,re,gc
import subprocess

# 这个函数一次只扫描一个文件
def scan_func(path,func_list,result):

    # 使用使用gcc对文件进行预处理,将预处理的结果保存到filestr中
    # 预处理默认会消除宏定义,并去掉注释
    # 可以在gcc命令中设置预处理的宏定义以选择分支,这里先设置默认的分支
    try:
        filestr=subprocess.run(["gcc","-E","-P",path],capture_output=True).stdout.decode(encoding="utf-8")
    except subprocess.CalledProcessError as identifier:
        print("error:"+identifier.stderr)
        exit(-1)
    except UnicodeDecodeError:
        print(path)
        return

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
    
