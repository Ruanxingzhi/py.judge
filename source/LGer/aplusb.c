#include <stdio.h>
#include <stdlib.h>

int s[1]={0};

int main(void)
{
    freopen("aplusb.in","r",stdin);
    freopen("aplusb.out","w",stdout);
    
    int a,b;
    scanf("%d%d",&a,&b);

    printf("%d",a+b);



    return 0;
}
