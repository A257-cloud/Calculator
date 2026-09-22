
import re
import json
from datetime import datetime

# 1. TOKENIZER
class Tokenizer:
    """Découpe une expression en tokens (nombres, opérateurs, parenthèses)."""

    MOTIF = r"\s*(?:(\d+\.\d+|\d+)|(\*\*|[-+*/()]))"

    def tokenizer(self, expression):
        """'2+3*4'  ->  [2, '+', 3, '*', 4]"""
        tokens = []
        position = 0

        while position < len(expression):
            match = re.match(self.MOTIF, expression[position:])
            if not match:
                raise ValueError(f"Caractère invalide : '{expression[position]}'")

            nombre, operateur = match.groups()
            if nombre is not None:
                tokens.append(float(nombre) if "." in nombre else int(nombre))
            else:
                tokens.append(operateur)
            position += match.end()

        return tokens

# 2. PARSER (PEMDAS)

class Parser:
    """Parseur récursif descendant : chaque méthode = un niveau de priorité."""

    def __init__(self):
        self.tokens = []
        self.pos = 0

    # --- Point d'entrée public ---
    def evaluer(self, expression):
        """Évalue une expression en respectant PEMDAS."""
        if not expression.strip():
            raise ValueError("Expression Vide")

        self.tokens = Tokenizer().tokenizer(expression)
        self.pos = 0
        resultat = self.lire_expression()

        if self.pos != len(self.tokens):
            raise ValueError(f"Token inattendu : '{self.tokens[self.pos]}'")

        return resultat

    # --- Niveau 1 : + et - ---
    def lire_expression(self):
        resultat = self.lire_terme()

        while self.pos < len(self.tokens) and self.tokens[self.pos] in ("+", "-"):
            operateur = self.tokens[self.pos]
            self.pos += 1
            droite = self.lire_terme()
            if operateur == "+":
                resultat += droite
            else:
                resultat -= droite

        return resultat

    # --- Niveau 2 : * et / ---
    def lire_terme(self):
        resultat = self.lire_facteur()

        while self.pos < len(self.tokens) and self.tokens[self.pos] in ("*", "/"):
            operateur = self.tokens[self.pos]
            self.pos += 1
            droite = self.lire_facteur()
            if operateur == "*":
                resultat *= droite
            else:
                if droite == 0:
                    raise ZeroDivisionError("Division par zéro impossible ! ")
                resultat /= droite

        return resultat

    # --- Niveau 3 : signes unaires ---
    def lire_facteur(self):
        if self.pos < len(self.tokens) and self.tokens[self.pos] == "-":
            self.pos += 1
            return -self.lire_facteur()
        if self.pos < len(self.tokens) and self.tokens[self.pos] == "+":
            self.pos += 1
            return self.lire_facteur()
        return self.lire_puissance()

    # --- Niveau 4 : ** (associatif à droite) ---
    def lire_puissance(self):
        base = self.lire_primaire()
        if self.pos < len(self.tokens) and self.tokens[self.pos] == "**":
            self.pos += 1
            exposant = self.lire_puissance()
            return base ** exposant
        return base

    # --- Niveau 5 : nombre OU ( expression ) ---
    def lire_primaire(self):
        if self.pos >= len(self.tokens):
            raise ValueError("Expression incomplète.")

        token = self.tokens[self.pos]

        if isinstance(token, (int, float)):
            self.pos += 1
            return token

        if token == "(":
            self.pos += 1
            valeur = self.lire_expression()
            if self.pos >= len(self.tokens) or self.tokens[self.pos] != ")":
                raise ValueError("Parenthèse fermante manquante.")
            self.pos += 1
            return valeur

        raise ValueError(f"Token innatendu : '{token}'")

# 3. GESTION DE L'HISTORIQUE

class HistoryManager:
    """Gère l'historique en mémoire + sauvegarde JSON + horodatage."""

    def __init__(self, fichier="historique.json"):
        self.fichier = fichier
        self.historique = []
        self.charger()

    # --- Chargement au démarrage ---
    def charger(self):
        try:
            with open(self.fichier, "r", encoding="utf-8") as f:
                self.historique = json.load(f)
        except FileNotFoundError:
            self.historique = []
        except (json.JSONDecodeError, ValueError):
            self.historique = []
        except Exception as e:
            print(f" Impossible de charger l'historique : {e}")
            self.historique = []

    # --- Sauvegarde sur disque ---
    def sauvegarder(self):
        try:
            with open(self.fichier, "w", encoding="utf-8") as f:
                json.dump(self.historique, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f" Impossible de sauvegarder l'historique : {e}")

    # --- Ajout d'une entrée ---
    def ajouter(self, expression, resultat):
        self.historique.append({
            "expression": expression,
            "resultat":   resultat,
            "date":       datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        })
        self.sauvegarder()

    # --- Affichage ---
    def afficher(self):
        print("\n" + "="*40)
        print("\n HISTORIQUE")
        print("="*40)
        if not self.historique:
            print("(vide)")
        else:
            for i, entree in enumerate(self.historique, start=1):
                expr = entree.get("expression", "?")
                res  = entree.get("resultat", "?")
                date = entree.get("date", "?")
                print(f"{i}. [{date}] {expr} = {res}")
        print("="*40)

# 4. CALCULATRICE (opérations simples + expressions)

class Calculator:
    """Combine les opérations simples et l'évaluation PEMDAS."""

    def __init__(self):
        self.parser = Parser()

    def addition(self, a, b):
        return a + b

    def soustraction(self, a, b):
        return a - b

    def multiplication(self, a, b):
        return a * b

    def division(self, a, b):
        if b == 0:
            return None
        return a / b

    def evaluer_expression(self, expression):
        return self.parser.evaluer(expression)

# 5. APPLICATION (menu + boucle principale)

class Application:
    """Programme principal : menu, saisies."""

    def __init__(self):
        self.calc = Calculator()
        self.histo = HistoryManager()

    # --- Menu ---
    def menu(self):
        print("\n" + "="*50)
        print("\t CALCULATRICE  AVEC HISTORIQUE :) ")
        print("="*50)
        print("1. Addition")
        print("2. Soustraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. operation")
        print("/history. voir l'historique")
        print("0. Quittez")
        print("="*50)

    # --- Mode expression complète ---
    def mode_expression(self):
        expr = input("Entrez votre operation > ").strip()
        try:
            resultat = self.calc.evaluer_expression(expr)
            print(f"\n Resultat : {expr} = {resultat}")
            self.histo.ajouter(expr, resultat)
        except ZeroDivisionError as e:
            print(f"\n Erreur : {e}")
        except ValueError as e:
            print(f"\n Erreur de syntaxe : {e}")

    # --- Mode opérations simples (1 à 4) ---
    def mode_operation_simple(self, choix):
        try:
            nbr1 = float(input("nombre1 >"))
            nbr2 = float(input("nombre2 >"))
        except ValueError:
            print(" Choix invalide, veuillez entrez des nombres valides")
            return

        operateur = ""
        resultat = None

        if choix == "1":
            resultat = self.calc.addition(nbr1, nbr2)
            operateur = "+"
        elif choix == "2":
            resultat = self.calc.soustraction(nbr1, nbr2)
            operateur = "-"
        elif choix == "3":
            resultat = self.calc.multiplication(nbr1, nbr2)
            operateur = "*"
        elif choix == "4":
            resultat = self.calc.division(nbr1, nbr2)
            operateur = "/"
            if resultat is None:
                print("Division impossible !!")
                return

        print(f"resultat : {resultat}")
        self.histo.ajouter(f"{nbr1} {operateur} {nbr2}", resultat)

    # --- Boucle principale ---
    def run(self):
        while True:
            self.menu()
            choix = input("votre choix : ").strip()

            if choix == "/history":
                self.histo.afficher()
                continue

            if choix == "0":
                print("\n Merci d'avoir utiliser la calculatrice. Au revoir !")
                break

            if choix not in ("1", "2", "3", "4", "5", "0"):
                print(" \n choix invalide, réessayer")
                continue

            if choix == "5":
                self.mode_expression()
                continue

            self.mode_operation_simple(choix)


# ============================================================
# POINT D'ENTRÉE
# ============================================================
if __name__ == "__main__":
    Application().run()