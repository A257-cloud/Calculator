import math
import tkinter as tk 
from main import Calculator,HistoryManager

#Ajout de la classe scientifique
class ScientificCalculator(Calculator):
    """Etend Calculator avec les fonctions scientifique"""
    def racine(self, x):
        if x <0:
            raise ValueError("Racine d'un négatif impossible")
        return math.sqrt(x)

    def pourcentage(self, x):
        return x / 100

    def inverse(self, x ):
        if x == 0:
            raise ZeroDivisionError("inverse de zéro impossible")
        return 1 / x

    def exposant(self, x, y):
        if x == 0 and y < 0:
            raise ZeroDivisionError(" calcul impossible")

calc = ScientificCalculator()
histo = HistoryManager()

fenetre = None
affichage = None

#Logique d'evaluation
def evaluer():
    """Evalue l'expression afficher et enregistre dans l'historique"""
    expression = affichage.get().strip() 
    print(f"DEBUG : expression ='{expression}'") 

    if not expression: 
        return

    try: 
        resultat = calc.evaluer_expression(expression)
        print(f"DEBUG : resultat='{resultat}'")
        affichage.delete(0, tk.END)
        affichage.insert(0, str(resultat))
        affichage.config(fg="black")
        histo.ajouter(expression, resultat)
    except ZeroDivisionError as e:
        afficher_erreur(f"Erreur : {e}")
    except ValueError as e :
        afficher_erreur(f"Erreur de syntaxe : {e}")
    except Exception as e:
        afficher_erreur(f"Erreur : {e}")

def afficher_erreur(message):
    """affiche en rouge l'erreur a l'ecran"""
    affichage.delete(0, tk.END)
    affichage.insert(0, message)
    affichage.config(fg="red")

#Logique de l'historique
def ouvrir_historique():
    """ouvre un fenetre avec l'historique"""
    fenetre_histo = tk.Toplevel(fenetre)
    fenetre_histo.title("Historique")
    fenetre_histo.geometry("450x350")

    zone = tk.Text(fenetre_histo, font=("Consolas", 11), wrap="word")
    zone.pack(fill="both", expands=True, padx=10, pady=10)

    if not histo.historique:
        zone.insert(tk.END, "(historique vide)")
    else: 
        for i, entree in enumerate(histo.historique, start=1):
            expr = entree.get("expression", "?")
            res = entree.get("resultat", "?")
            date = entree.get("date", "?")
            zone.insert(tk.END, f"{i}.[{date}]\n {expr} = {res}\n\n")

    zone.config(state="disabled")

    tk.Button(
        fenetre_histo, 
        text="Fermer",
        command=fenetre_histo.destroy, 
    ).pack(pady=5)
#application des fonctions 
def appliquer_fonction(fonction, nom):
    """
    Applique une fonction scientifique (racine, %, inverse) à la valeur affichée.
    Remplace l'écran par le résultat.
    """
    expression = affichage.get().strip()
    if not expression:
        return

    try:
        # 1. Évalue d'abord l'expression affichée (au cas où elle contient un calcul)
        valeur = calc.evaluer_expression(expression)
        # 2. Applique la fonction
        resultat = fonction(valeur)
        # 3. Affiche le résultat
        affichage.delete(0, tk.END)
        affichage.insert(0, str(resultat))
        affichage.config(fg="black")
        # 4. Enregistre dans l'historique
        histo.ajouter(f"{nom}({expression})", resultat)
    except ZeroDivisionError as e:
        afficher_erreur(f"Erreur : {e}")
    except ValueError as e:
        afficher_erreur(f"Erreur : {e}")
    except Exception as e:
        afficher_erreur(f"Erreur : {e}")

def inserer_exposant():
    affichage.insert(tk.END, "**")  
#====LOGIQUE DES BOUTONS =======
def action_clic(texte):
    """gere le clic sur les boutons"""
    print(f"DEBUG : Clic sur '{texte}'")

    if texte =="C":
        affichage.delete(0, tk.END)
        affichage.config(fg="black")
    elif texte =="Del":
        contenu = affichage.get()
        affichage.delete(0, tk.END)
        affichage.insert(0, contenu[:-1])
    elif texte == "=":
        evaluer()
    elif texte == "√":
        appliquer_fonction(calc.racine, "√")
    elif texte == "%":
        appliquer_fonction(calc.pourcentage, "%")
    elif texte == "1/x":
        appliquer_fonction(calc.inverse, "1/x")
    elif texte == "^":
        inserer_exposant()
    else:
        affichage.insert(tk.END, texte)
        affichage.config(fg="black")

#Ajout clavier
def touche_entree(event):
    evaluer()
    return "break"

def touche_echap(event):
    affichage.delete(0, tk.END)

#======Affichage=========
fenetre = tk.Tk()
fenetre.title("Calculator")
fenetre.geometry("320x450")
fenetre.resizable(False, False)

# ---Zone d'afffichage
affichage = tk.Entry(
    fenetre,
    font=("Arial", 20),
    justify= "right",
    bd=10,
    insertwidth=2,
)
affichage.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=5, pady=5)

# ---zone des boutons
BOUTONS = [
    ["√", "%", "1/x", "^"],
    ["C", "(", ")", "/"],
    ["7", "8", "9", "*"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["0", ".", "Del", "="],
]

for ligne, rangee in enumerate(BOUTONS):
    for colonne, texte in enumerate(rangee):
        bouton = tk.Button(fenetre, text=texte, font=("Arial",14), command=lambda t=texte:
                           action_clic(t),)
        bouton.grid(row=ligne + 1, column=colonne, sticky="nsew", padx=2, pady=2)

for i in range(4):
    fenetre.columnconfigure(i, weight=1)

for i in range(1, 7):
    fenetre.rowconfigure(i, weight=1)

fenetre.rowconfigure(0, weight=0)

#RACOURCIS CLAVIER
fenetre.bind("<Return>", touche_entree)
fenetre.bind("<Escape>", touche_echap)

fenetre.mainloop()