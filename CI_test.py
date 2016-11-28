from os import system

print("Testing judge.py:")

system("./judge.py >result.csv")
system("""echo 'Name , aplusb  , bplusa  , total ,
ACer , AAAAAAAAAA , AAAAAAAAAA , 200 , 
CEer , CCCCCCCCCC , CCCCCCCCCC , 0 , 
LGer , AAAAAAAAAA , FFFFFFFFFF , 100 , 
REer , RRRRRRRRRR , RRRRRRRRRR , 0 , 
WAer , WWWWWWWWWW , WWWWWWWWWW , 0 , 
blue , AAAAAAARWT , AAAAAAARWT , 140 ,' >correct.csv""")

if(system("diff -bB result.csv correct.csv")):
    print("✖ The result is WRONG!!!!")
    system("rm *.csv")
    exit(-1)

print("✔ Test OK.")
system("rm *.csv")
exit(0)
