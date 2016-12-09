#!/usr/bin/env python3

import os
import sys
import time
import shutil
import json
import psutil
import subprocess
import readline
import threading
from subprocess import *

def diff(file1, file2):

    try:
        f1 = open(file1)
        f2 = open(file2)
    except Exception:
        return (2,0,'','')      # FILE ERROR

    lineNumber = 0
    L1 = [x for x in f1.readlines() if x.strip() != '']
    L2 = [x for x in f2.readlines() if x.strip() != '']
    f1.close()
    f2.close()

    if len(L1) != len(L2):
        return (1, 0, '', '')   # WA

    for index in range(0, len(L2)):
        lineNumber += 1
        # print(L1[index], L2[index])

        if L1[index].strip() != L2[index].strip():
            return (False, lineNumber, L1[index].strip(), L2[index].strip())

    return (0, 0, '', '')       # AC

memory_max = 0
timelimit = 0

def memory_checker(pid, time_limit):
    global memory_max
    global timelimit

    time.sleep(0.001)
    starttime = time.time()

    try:
        proc = psutil.Process(pid)
    except:
        return

    memory_max = 0

    while True:
        endtime = time.time()

        if endtime - starttime > timelimit:
            return

        try:
            for i in range(0, 5):
                mem = proc.memory_info()
                usage = mem.vms
                memory_max = max(memory_max, usage)

        except:
            return

        time.sleep(0.005)

tot = 0

def judge(player , prob):
    global memory_max
    global timelimit
    global tot

    memory_max = 0
    readline.parse_and_bind('tab: complete')

    setting = ""
    case = ""

    setting = prob

    try:
        with open("./data/{0}/{0}.json".format(setting)) as setting_file:
            document = json.load(setting_file)
    except Exception:
        pass
    
    name = prob

    try:
        compiler_pas  = document["compiler_pas"]
    except Exception:
        compiler_pas = "fpc "
    try:
        compiler_cpp  = document["compiler_cpp"]
    except Exception:
        compiler_cpp  = "g++ "
    try:
        compiler_c    = document["compiler_c"]
    except Exception:
        compiler_c    = "gcc "
    

    try:
        startid       = document["start_id"]
    except Exception:
        startid       = 1
    try:
        endid         = document["end_id"]
    except Exception:
        endid         = 10
    try:
        timelimit     = document["time_limit"]
    except Exception:
        timelimit     = 1.0
    try:
        memlimit      = document["memory_limit"]
    except Exception:
        memlimit      = 128.0
    try:
        input_suffix  = document["input_suffix"]
    except Exception:
        input_suffix  = 'in'
    try:
        output_suffix = document["output_suffix"]
    except Exception:
        output_suffix = 'out'

    formatter     = "{0}{1}.{2}"
    source_ext = '.cpp'
    build_file = 'a.out'

    if(os.system("cat ./source/{}/{}.cpp >tmp.out 2>tmp2.out".format(player,name)) == 0):
        source_ext='.cpp'
    elif(os.system("cat ./source/{}/{}.c >tmp.out 2>tmp2.out".format(player,name)) == 0):
        source_ext='.c'
    elif(os.system("cat ./source/{}/{}.pas >tmp.out 2>tmp2.out".format(player,name)) == 0):
        source_ext='.pas'
    
    if(source_ext == '.cpp'):
        compiler = compiler_cpp
    elif(source_ext == '.c'):
        compiler = compiler_c
    elif(source_ext == '.pas'):
        compiler = compiler_pas
    

    spj = None

    if(os.system("cat ./source/{}/{}{} >tmp.out 2>tmp2.out".format(player,name,source_ext))):
        for i in range(startid, endid + 1):
            print('-',end='')
            sys.stdout.flush()

        os.system("rm *.out")
        return

    # print('(info) Compiling source...')

    if source_ext == ".pas":
        # print("(warn) Enabled Pascal support")
        status = os.system("{0} ./source/{1}/{2}{3} 2>tmp.out".format(compiler, player, name, source_ext))
        os.system("mv {0} {1}".format("./source/{}".format(name), "./{}".format(build_file)))
    else:
        status = os.system("{0} ./source/{1}/{2}{3} -o {4} 2>tmp.out".format(compiler, player, name, source_ext, build_file))

    if status != 0:
        for i in range(startid, endid + 1):
            print('C',end='')
            sys.stdout.flush()
        
        os.system("rm *.out")
        return

    total_passed = 0
    total_time = 0.0
    max_memory = 0.0

    for i in range(startid, endid + 1):
        # print('\n\033[32m# Testcase\033[0m {}'.format(i))

        # time.sleep(0.1)
        try:
            os.remove('{}.out'.format(name))
        except:
            pass 

        shutil.copy2('./data/{0}/{1}'.format(name, formatter.format(name, i, input_suffix)), '{0}.in'.format(name))

        # ......
        os.system('pkill -9 {}'.format(build_file))

        starttime = 0.0
        flag = True

        status = 0
        proc = Popen(["./{}".format(build_file)])
        pid = proc.pid
        t = threading.Thread(target=memory_checker, args=(pid, timelimit))
        t.start()

        starttime = time.time()
        try:
            proc.wait(timeout = timelimit)
        except subprocess.TimeoutExpired:
            flag = False
        endtime = time.time()

        status = proc.returncode
        t.join(timelimit)

        passed = endtime - starttime
        max_memory = max(max_memory, memory_max)
        # print("Time:   {}s".format(passed))
        # print("Memory: {}MB".format(float(memory_max) / (1024 * 1024)))

        if not flag:        
            print('T',end='')
            sys.stdout.flush()

        if flag:
            if status != 0:
                print('R',end='')
                sys.stdout.flush()

                flag = False

        if flag:
            if memory_max / (1024 ** 2) > memlimit:
                print('M',end='')
                sys.stdout.flush()
            
                flag = False

        if flag:
            succeeded, lineNo, std, mine = diff('./data/{0}/{1}'.format(
                name, formatter.format(name, i, output_suffix)),
                '{}.out'.format(name)
            )
            if succeeded == 1:
                print('W',end='')
                sys.stdout.flush()
                flag = False
            elif succeeded == 2:
                print('F',end='')
                sys.stdout.flush()
                flag = False

        if flag:
            print('A',end='')
            sys.stdout.flush()
            total_passed += 1

        total_time += passed
        memory_max = max(memory_max, max_memory)

    # print('### ANALYZE ###')

    # print(case,end='')
    

    os.system("rm *.in")
    os.system("rm *.out")


    tot += int(float(total_passed)/float(endid - startid + 1)*100)

def judgeSingle(player):
    global tot

    tot = 0

    print("%s , "%player,end='')
    for prob in sorted(os.listdir('data/')):
        if os.path.isdir('data/'+prob):
            judge(player,prob)
            print(" , ",end='')
    print("%s , "%tot)
    

def makehead():
    print("Name , ",end='')
    for prob in sorted(os.listdir('data/')):
        if os.path.isdir('data/'+prob):
            print(prob,' , ',end='')
    print("total ,")

if __name__ == "__main__":

    makehead()

    for player in sorted(os.listdir('source/')):
        if os.path.isdir('source/'+player):
            judgeSingle(player)
