operazioni = [int(x) for x in input("Operazioni: ").split()]
saldo = 0
saldi = []
depositi = 0
prelievi = 0
saldo_max = -1000000
saldo_min = 1000000

for o in operazioni:
    saldo += o
    saldi.append(saldo)
    if o>0:
        depositi +=1
    elif o<0:
        prelievi +=1
    if saldo > saldo_max:
        saldo_max = saldo
    if saldo < saldo_min:
        saldo_min = saldo

print("Saldo finale:", saldo)
print("Saldo massimo:", saldo_max)
print("Saldo minimo:", saldo_min)
print("Depositi:", depositi)
print("Prelievi:", prelievi)
print("Saldi dopo ogni operazione:", saldi)
