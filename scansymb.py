import os,subprocess

def scan_symb(libdir):
    # 第一步扫描所有libxx.so文件
    with open("test.csv","w") as result:
        for root,dir,file in os.walk(libdir):
            for filename in file:
                if filename[0:3]=="lib" and filename[-3:]==".so":
                    # 对每个libxxx.so,使用nm命令读取其接口
                    try:
                        ret=subprocess.run(["nm","--defined-only","-g",os.path.join(root,filename)],capture_output=True)
                        for line in ret.stdout.decode(encoding="utf-8").split("\n"):
                            if " T " in line and "@" not in line:
                                result.write(line.split(" T ")[1]+",\n")
                    except subprocess.CalledProcessError as e:
                        print(e.stderr)

if __name__=="__main__":
    scan_symb("/home/tet/test_sets/workspace/glibc-build/")
