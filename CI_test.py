from os import system

system("./judge.py aplusb >result")
system("echo AAAAAAARWT >correct")

if(system("diff -bB result correct")):
    print("The result is WRONG!!!!")
    system("rm result correct")
    exit(-1)

print("Test OK!")
system("rm result correct")
exit(0)
