numeri = [int(x) for x in input("Numeri separati da spazio: ").split()]
media = sum(numeri)/len(numeri) if numeri else 0

sopra = [x for x in numeri if x > media]
sotto = [x for x in numeri if x < media]

max_seq = 1
seq = 1
for i in range(1, len(numeri)):
    if numeri[i] == numeri[i-1]:
        seq += 1
        if seq > max_seq:
            max_seq = seq
    else:
        seq = 1

print("Media:", media)
print("Sopra la media:", len(sopra))
print("Sotto la media:", len(sotto))
print("Numeri sopra la media:", sopra)
print("Sequenza consecutiva massima:", max_seq)
