magazzino = []
n = int(input("Quanti prodotti? "))
for i in range(n):
    nome = input("Nome: ")
    prezzo = float(input("Prezzo: "))
    quantita = int(input("Quantità: "))
    magazzino.append([nome, prezzo, quantita])

valori = [p[1]*p[2] for p in magazzino]
totale = sum(valori)
max_valore = max(valori)
prodotto_max = magazzino[valori.index(max_valore)][0]
esauriti = [p[0] for p in magazzino if p[2]==0]

print("Valore totale magazzino:", totale)
print("Prodotto con valore più alto:", prodotto_max)
print("Prodotti esauriti:", esauriti)
