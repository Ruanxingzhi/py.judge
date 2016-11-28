from os import system

print("Testing judge.py:")

system("./judge.py aplusb >result")
system("""echo 'AAAAAAARWT
----------
AAAAAAAAAA
WWWWWWWWWW
RRRRRRRRRR
CCCCCCCCCC' >correct""")

if(system("diff -bB result correct")):
    print("✖ The result is WRONG!!!!")
    system("rm result correct")
    exit(-1)

print("✔ Test OK.")
system("rm result correct")
exit(0)
