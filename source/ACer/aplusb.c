#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    freopen("aplusb.in","r",stdin);
    freopen("aplusb.out","w",stdout);
    
    int a,b;
    scanf("%d%d",&a,&b);

    printf("%d",a+b);



    return 0;
}
