Enterlist=eval(input("Enter numbers seperated by ,  : "))
A=list(Enterlist)

t =0
x =0
while(x<len(A)):
   t=t+A[x]
   x+=1
print(t)
