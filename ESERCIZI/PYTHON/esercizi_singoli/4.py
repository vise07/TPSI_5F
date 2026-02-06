frase = input("Inserisci una frase: ")
parole = frase.split()

conteggio = {}
for p in parole:
    if p in conteggio:
        conteggio[p] += 1
    else:
        conteggio[p] = 1

piu_lunga = max(parole, key=len)
piu_corta = min(parole, key=len)
ricorrenti = [p for p, c in conteggio.items() if c>1]

print("Parole:", parole)
print("Conteggio:", conteggio)
print("Parola più lunga:", piu_lunga)
print("Parola più corta:", piu_corta)
print("Parole ricorrenti:", ricorrenti)
