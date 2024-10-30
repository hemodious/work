import random
import string
characters=string.ascii_letters+ string.digits*4

ans=''.join(random.choices(characters, k=7) )
store=[] 
for good in store:
    if store == ans :
        print("already exists")
    else:
        store.append(ans)  
        print(ans)   
print(ans)
dof="car"
car=f"car {dof.upper()}"
print(car)