studenti = []
n = int(input("Quanti studenti? "))
for i in range(n):
    nome = input("Nome: ")
    voti = [int(x) for x in input("Voti separati da spazio: ").split()]
    media = sum(voti) / len(voti) if voti else 0
    stato = "Promosso" if media >= 6 else "Bocciato"
    studenti.append([nome, media, stato])

media_alta = max(studenti, key=lambda x: x[1])[0]
media_bassa = min(studenti, key=lambda x: x[1])[0]
promossi = [s[0] for s in studenti if s[2] == "Promosso"]

for s in studenti:
    print(f"{s[0]} - media: {s[1]:.2f} - {s[2]}")
print("Media più alta:", media_alta)
print("Media più bassa:", media_bassa)
print("Promossi:", promossi)
