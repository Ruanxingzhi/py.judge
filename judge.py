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
    f1 = open(file1)
    f2 = open(file2)

    lineNumber = 0
    L1 = [x for x in f1.readlines() if x.strip() != '']
    L2 = [x for x in f2.readlines() if x.strip() != '']
    f1.close()
    f2.close()

    if len(L1) != len(L2):
        return (False, 0, '', '')

    for index in range(0, len(L2)):
        lineNumber += 1
        # print(L1[index], L2[index])

        if L1[index].strip() != L2[index].strip():
            return (False, lineNumber, L1[index].strip(), L2[index].strip())

    return (True, 0, '', '')

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

def judge(player , prob):
    global memory_max
    global timelimit

    memory_max = 0
    readline.parse_and_bind('tab: complete')

    setting = ""
    case = ""

    setting = prob

    with open("./data/{0}/{0}.json".format(setting)) as setting_file:
        document = json.load(setting_file)

    name          = document["name"]
    source_ext    = document["source_ext"]
    build_file    = document["build_file"]
    compiler      = document["compiler"]
    startid       = document["start_id"]
    endid         = document["end_id"]
    timelimit     = document["time_limit"]
    memlimit      = document["memory_limit"]
    input_suffix  = document["input_suffix"]
    output_suffix = document["output_suffix"]
    formatter     = document["name_format"]
    special_judge = document["special_judge"]

    spj = None

    if(os.system("cat ./source/{}/{}{} >tmp.out 2>tmp2.out".format(player,name,source_ext))):
        for i in range(startid, endid + 1):
            case += '-'
        print(case)
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
            case += 'C'
        print(case)
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
            case+='T'

        if flag:
            if status != 0:
                case+='R'

                flag = False

        if flag:
            if memory_max / (1024 ** 2) > memlimit:
                case+='M'
            
                flag = False

        if flag:
            if special_judge:
                if spj is None:
                    sys.path.append("./data/{}/".format(name))
                    import spj

                spj.init(
                    "./data/{0}/{1}".format(name, formatter.format(name, i, input_suffix)),
                    "./data/{0}/{1}".format(name, formatter.format(name, i, output_suffix)),
                    "{}.out".format(name)
                )

                spj.judge()
                status = spj.status

                if status != spj.ACCEPTED:
                    if status == spj.ERROR:
                        case+='X'

                        flag = False

                    elif status == spj.INTERNAL_ERROR:
                        case+='X'

                        flag = False

                    elif status == spj.UNKNOWN:
                        case+='U'

                        flag = False

                    if not flag:
                        print("(info) {}".format(spj.message))

            else:
                succeeded, lineNo, std, mine = diff('./data/{0}/{1}'.format(
                    name, formatter.format(name, i, output_suffix)),
                    '{}.out'.format(name)
                )
                if not succeeded:
                    case+='W'

                    flag = False

        if flag:
            case+='A'
            total_passed += 1

        total_time += passed
        memory_max = max(memory_max, max_memory)

    # print('### ANALYZE ###')

    print(case)
    

    os.system("rm *.in")
    os.system("rm *.out")

if __name__ == "__main__":
    judge('blue','aplusb')
    judge('LGer','aplusb')
    judge('ACer','aplusb')
    judge('WAer','aplusb')
    judge('REer','aplusb')
    judge('CEer','aplusb')
