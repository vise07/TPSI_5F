def calcolatrice():

    operazioni = ['+', '-', '*', '/']
    
    while True:
        print("\nScegli l'operazione:")
        print("1. Somma (+)")
        print("2. Sottrazione (-)")
        print("3. Moltiplicazione (*)")
        print("4. Divisione (/)")
        print("5. Esci")

        scelta = input("Inserisci il numero dell'operazione desiderata: ")

        if scelta == '5':
            print("Fine programma.")
            break

        if scelta not in ['1', '2', '3', '4']:
            print("Scelta non valida. Riprova.")
            continue

        num1 = float(input("Inserisci il primo numero: "))
        num2 = float(input("Inserisci il secondo numero: "))

        if scelta == '1':
            risultato = num1 + num2
        elif scelta == '2':
            risultato = num1 - num2
        elif scelta == '3':
            risultato = num1 * num2
        elif scelta == '4':
            if num2 == 0:
                print("Errore, impossibile dividere per 0.")
                continue
            else:
                risultato = num1 / num2

        print(f"Il risultato è: {risultato}")

calcolatrice()
