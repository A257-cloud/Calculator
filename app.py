import re

#1- Découper l'expression en morceaux

def tokinizer(expression):
    """2+3*4 -> [ 2, '+', 3, '*', 4]"""
    tokens = []
    position = 0
    motif = r"\s*(?:(\d+\.\d+|\d+)|(\*\*|[-+*/()]))"

    while position < len(expression):
        match = re.match(motif, expression[position])
        if not match: 
            raise ValueError(f"Caractère invalide : '{expression[position]}'")

        nombre, operateur = match.groups()
        if nombre is not None:
            tokens.append(float(nombre) if "." in nombre else int(nombre))
        else:
            tokens.append(operateur)
        position += match.end()

    return tokens 

#2- Parser : chaque fonction =  un niveau de priorité

def lire_expression(tokens, pos):
    """Niveau 1: Gère + et - """
    resultat, pos = lire_terme(tokens, pos)

    while pos < len(tokens) and tokens[pos] in ("+", "-"):
        operateur = tokens[pos]
        pos += 1 
        droite, pos = lire_terme(tokens, pos)
        if operateur == "+":
            resultat += droite 
        else: 
            resultat -= droite 

    return resultat, pos 

def lire_terme(tokens, pos):
    """niveau 2: Gère * et / """
    resultat, pos = lire_facteur(tokens, pos)

    while pos < len(tokens) and tokens[pos] in ("*", "/"):
        operateur = tokens[pos]
        pos += 1
        droite, pos = lire_facteur(tokens, pos)
        if operateur == "*":
            resultat *= droite 
        else:
            if droite == 0:
                raise ZeroDivisionError("Division par zéro impossible ! ")
            resultat /= droite 

    return resultat, pos

def lire_facteur(tokens, pos):
    """Niveau 3: Gere les signes unaires(nbrs négatifs)"""
    if pos < len(tokens) and tokens[pos]  == "-":
        valeur, pos = lire_facteur(tokens, pos + 1)
        return -valeur, pos
    if pos < len(tokens) and tokens[pos] == "+":
        valeur, pos = lire_facteur(tokens, pos)
        return lire_facteur(tokens, pos + 1)
    return lire_puissance(tokens, pos)

def lire_puissance(tokens, pos):
    """Niveau 4: Gère les ** (associatif à droite )"""
    base, pos = lire_primaire(tokens, pos)

    if pos < len(tokens) and tokens[pos] == "**":
        exposant, pos = lire_facteur(tokens, pos + 1)
        return base ** exposant, pos 

    return base, pos 

def lire_primaire(tokens, pos):
    """Niveau 5: Gère nombre OU(expression)"""
    if pos >= len(tokens):
        raise ValueError("Expression incomplète.")

    token = tokens[pos]

    if isinstance(token, (int, float)):
        return  token, pos + 1

    if token == "(":
        valeur, pos = lire_expression(tokens, pos + 1)
        if pos >= len(tokens) or tokens[pos] != ")":
            raise ValueError("Parenthèse fermante manquante.")
        return valeur, pos + 1

    raise ValueError(f"Token innatendu : '{token}'")


#3- Fonction d'evaluation publique 

def evaluer_expression(expression):
    """evalue les expressions en respectat PAMDAS."""
    if not expression.strip():
        raise ValueError("Expression Vide")

    tokens = tokinizer(expression)
    resultat, position = lire_expression(tokens, 0)

    if position != len(tokens):
        raise ValueError("Token inattendu : '{tokens[position]}'")

    return resultat

#4- Operations classiques

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
    print("\n" + "="*50)
    print("\t CALCULATRICE AMELIORER :) ")
    print("="*50)
    print("1. Addition")
    print("2. Soustraction")
    print("3. Multiplication")
    print("4. Division")
    print("5. operation")
    print("0. Quittez")
    print("="*50)


while True:
    menu()
    choix = input("votre choix : ").strip()

    if choix == "0":
        print("\n Merci d'avoir utiliser la calculatrice. Au revoir !")
        break
    
    if choix not in ("1", "2", "3", "4", "5", "0",):
        print(" \n choix invalide, réessayer")
        continue

#Mode expression 
    if choix == "5":
        expr = input("Entrez votre operation > ").strip()
        try: 
            resultat = evaluer_expression(expr)
            print(f"\n Resultat : {expr} = {resultat}")
        except ZeroDivisionError as e: 
            print(f"\n Erreur : {e}")
        except ValueError as e:
            print(f"\n Erreur de syntaxe : {e}")
        continue

#Mpde operation simple 
    try:
        nbr1 = float(input("nombre1 >"))
        nbr2 = float(input("nombre2 >"))
    except ValueError:
        print(" Choix invalide, veuillez entrez des nombres valides")
        continue

        if choix == "1":
            resultat = Addition(nbr1,nbr2)
        elif choix ==  "2":
            resultat = Soustraction(nbr1,nbr2)
        elif choix ==  "3":
            resultat = Multiplication(nbr1,nbr2)
        elif choix ==  "4":
            resultat = Division(nbr1, nbr2)
            if resultat is None:
                print("Division impossible !!")
                continue

    print(f"resultat : {resultat}")