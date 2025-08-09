# Convierte entero (1..3999) a números romanos
n = int(input("Número (1-3999): "))
val = [1000,900,500,400,100,90,50,40,10,9,5,4,1]
sim = ["M","CM","D","CD","C","XC","L","XL","X","IX","V","IV","I"]
res = ""
for v,s in zip(val, sim):
    while n >= v:
        res += s
        n -= v
print(res)
