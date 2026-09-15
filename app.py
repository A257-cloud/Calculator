def Addition (nbr1, nbr2):
    return nbr1 + nbr2

def Soustraction (nbr1, nbr2):
    return nbr1 - nbr2

def Multiplication (nbr1, nbr2):
    return nbr1 * nbr2 

def Division (nbr1, nbr2):
    if nbr2 == 0:
        return None
    return nbr1 / nbr2

def menu():
    print("\n" + "="*30)
    print("CALCULATRICE :) ")
    print("="*30)
    print("1. Addition")
    print("2. Soustraction")
    print("3. Multiplication")
    print("4. Division")
    print("0. Quittez")
    print("="*30)


while True:
    menu()
    choix = input("votre choix : ").strip()

    if choix == "0":
        print("\n Merci d'avoir utiliser la calculatrice. Au revoir !")
        break
    
    if choix not in ("1", "2", "3", "4", "0"):
        print(" \n choix invalide, réessayer")
        continue

    try:
        nbr1 = float(input("nombre1 >"))
        nbr2 = float(input("nombre2 >"))
    except ValueError:
        print(" Choix invalide, veuillez entrez des nombres valides")
        continue


    match choix:
        case "1":
            resultat = Addition(nbr1,nbr2)
        case "2":
            resultat = Soustraction(nbr1,nbr2)
        case "3":
            resultat = Multiplication(nbr1,nbr2)
        case "4":
            resultat = Division(nbr1, nbr2)
            if resultat is None:
                print("Division impossible !!")

    print(f"resultat : {resultat}")