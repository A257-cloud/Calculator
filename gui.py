import math
import tkinter as tk
from main import Calculator, HistoryManager


# ============================================================
# THÈME CLAIR — Palette moderne
# ============================================================
THEME_CLAIR = {
    "fond_fenetre":       "#f5f5f7",
    "fond_affichage":     "#ffffff",
    "texte_affichage":    "#1a1a1a",
    "curseur":            "#0066cc",

    "fond_chiffre":       "#ffffff",
    "texte_chiffre":      "#1a1a1a",
    "actif_chiffre":      "#e8e8ec",

    "fond_operateur":     "#e3f2fd",
    "texte_operateur":    "#0d47a1",
    "actif_operateur":    "#bbdefb",

    "fond_scientifique":  "#f3e5f5",
    "texte_scientifique": "#6a1b9a",
    "actif_scientifique": "#e1bee7",

    "fond_egal":          "#0066cc",
    "texte_egal":         "#ffffff",
    "actif_egal":         "#0052a3",

    "fond_action":        "#eceff1",
    "texte_action":       "#37474f",
    "actif_action":       "#cfd8dc",

    "texte_erreur":       "#d32f2f",
}


# ============================================================
# THÈME SOMBRE — Palette élégante
# ============================================================
THEME_SOMBRE = {
    "fond_fenetre":       "#1e1e2e",
    "fond_affichage":     "#181825",
    "texte_affichage":    "#cdd6f4",
    "curseur":            "#89b4fa",

    "fond_chiffre":       "#313244",
    "texte_chiffre":      "#cdd6f4",
    "actif_chiffre":      "#45475a",

    "fond_operateur":     "#1e3a5f",
    "texte_operateur":    "#89b4fa",
    "actif_operateur":    "#2a4d7a",

    "fond_scientifique":  "#3b2a4d",
    "texte_scientifique": "#cba6f7",
    "actif_scientifique": "#4d3560",

    "fond_egal":          "#89b4fa",
    "texte_egal":         "#1e1e2e",
    "actif_egal":         "#b4c9fc",

    "fond_action":        "#45475a",
    "texte_action":       "#cdd6f4",
    "actif_action":       "#585b70",

    "texte_erreur":       "#f38ba8",
}

theme_actuel = THEME_CLAIR


# ============================================================
# CALCULATRICE SCIENTIFIQUE
# ============================================================
class ScientificCalculator(Calculator):
    def racine(self, x):
        if x < 0:
            raise ValueError("Racine d'un nombre négatif impossible")
        return math.sqrt(x)

    def pourcentage(self, x):
        return x / 100

    def inverse(self, x):
        if x == 0:
            raise ZeroDivisionError("Inverse de zéro impossible")
        return 1 / x

    def exposant(self, x, y):
        if x == 0 and y < 0:
            raise ZeroDivisionError("0 puissance négative impossible")
        return math.pow(x, y)


# ============================================================
# INSTANCES
# ============================================================
calc  = ScientificCalculator()
histo = HistoryManager()

fenetre      = None
frame_calc   = None
frame_histo  = None
affichage    = None
zone_histo   = None


# ============================================================
# CATÉGORISATION DES BOUTONS
# ============================================================
def categoriser_bouton(texte):
    """Retourne la catégorie d'un bouton selon son texte."""
    if texte == "=":
        return "egal"
    if texte in ("+", "-", "*", "/"):
        return "operateur"
    if texte in ("√", "%", "1/x", "^"):
        return "scientifique"
    if texte in ("C", "⌫", "Historique", " Thème"):
        return "action"
    return "chiffre"


# ============================================================
# GESTION DU THÈME
# ============================================================
def basculer_theme():
    global theme_actuel
    if theme_actuel is THEME_CLAIR:
        theme_actuel = THEME_SOMBRE
    else:
        theme_actuel = THEME_CLAIR
    appliquer_theme()


def appliquer_theme():
    fenetre.config(bg=theme_actuel["fond_fenetre"])
    frame_calc.config(bg=theme_actuel["fond_fenetre"])
    frame_histo.config(bg=theme_actuel["fond_fenetre"])

    for widget in frame_calc.winfo_children():
        appliquer_theme_widget(widget)
    for widget in frame_histo.winfo_children():
        appliquer_theme_widget(widget)


def appliquer_theme_widget(widget):
    classe = widget.winfo_class()

    if classe == "Entry":
        widget.config(
            bg=theme_actuel["fond_affichage"],
            fg=theme_actuel["texte_affichage"],
            insertbackground=theme_actuel["curseur"],
        )

    elif classe == "Button":
        texte = widget.cget("text")
        cat = categoriser_bouton(texte)
        widget.config(
            bg=theme_actuel[f"fond_{cat}"],
            fg=theme_actuel[f"texte_{cat}"],
            activebackground=theme_actuel[f"actif_{cat}"],
            activeforeground=theme_actuel[f"texte_{cat}"],
            cursor="hand2",
            bd=0,
            relief="flat",
        )

    elif classe == "Label":
        widget.config(
            bg=theme_actuel["fond_fenetre"],
            fg=theme_actuel["texte_affichage"],
        )

    elif classe == "Text":
        widget.config(
            bg=theme_actuel["fond_affichage"],
            fg=theme_actuel["texte_affichage"],
            insertbackground=theme_actuel["curseur"],
            bd=0,
            relief="flat",
        )

    elif classe == "Frame":
        widget.config(bg=theme_actuel["fond_fenetre"])


# ============================================================
# FONCTIONS CALCUL
# ============================================================
def evaluer():
    expression = affichage.get().strip()
    if not expression:
        return
    try:
        resultat = calc.evaluer_expression(expression)
        affichage.delete(0, tk.END)
        affichage.insert(0, str(resultat))
        affichage.config(fg=theme_actuel["texte_affichage"])
        histo.ajouter(expression, resultat)
        if frame_histo.winfo_ismapped():
            rafraichir_historique()
    except ZeroDivisionError as e:
        afficher_erreur(f"Erreur : {e}")
    except ValueError as e:
        afficher_erreur(f"Erreur de syntaxe : {e}")
    except Exception as e:
        afficher_erreur(f"Erreur : {e}")


def afficher_erreur(message):
    affichage.delete(0, tk.END)
    affichage.insert(0, message)
    affichage.config(fg=theme_actuel["texte_erreur"])


def appliquer_fonction(fonction, nom):
    expression = affichage.get().strip()
    if not expression:
        return
    try:
        valeur = calc.evaluer_expression(expression)
        resultat = fonction(valeur)
        affichage.delete(0, tk.END)
        affichage.insert(0, str(resultat))
        affichage.config(fg=theme_actuel["texte_affichage"])
        histo.ajouter(f"{nom}({expression})", resultat)
        if frame_histo.winfo_ismapped():
            rafraichir_historique()
    except ZeroDivisionError as e:
        afficher_erreur(f"Erreur : {e}")
    except ValueError as e:
        afficher_erreur(f"Erreur : {e}")
    except Exception as e:
        afficher_erreur(f"Erreur : {e}")


def inserer_exposant():
    affichage.insert(tk.END, "**")


# ============================================================
# PANNEAU HISTORIQUE
# ============================================================
def afficher_historique():
    if not frame_histo.winfo_ismapped():
        frame_histo.pack(side="right", fill="y", padx=(0, 8), pady=8)
    rafraichir_historique()
    fenetre.geometry("620x640")


def cacher_historique():
    frame_histo.pack_forget()
    fenetre.geometry("360x640")


def rafraichir_historique():
    zone_histo.config(state="normal")
    zone_histo.delete("1.0", tk.END)

    if not histo.historique:
        zone_histo.insert(tk.END, "(historique vide)")
    else:
        for i, entree in enumerate(histo.historique, start=1):
            expr = entree.get("expression", "?")
            res  = entree.get("resultat", "?")
            date = entree.get("date", "?")
            zone_histo.insert(tk.END, f"{i}. [{date}]\n   {expr} = {res}\n\n")

    zone_histo.config(state="disabled")


# ============================================================
# GESTION DES CLICS
# ============================================================
def action_clic(texte):
    if texte == "C":
        affichage.delete(0, tk.END)
        affichage.config(fg=theme_actuel["texte_affichage"])
    elif texte == "⌫":
        contenu = affichage.get()
        affichage.delete(0, tk.END)
        affichage.insert(0, contenu[:-1])
    elif texte == "=":
        evaluer()
    elif texte == " Historique":
        if frame_histo.winfo_ismapped():
            cacher_historique()
        else:
            afficher_historique()
    elif texte == " Thème":
        basculer_theme()
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
        affichage.config(fg=theme_actuel["texte_affichage"])


# ============================================================
# CLAVIER
# ============================================================
def touche_entree(event):
    evaluer()
    return "break"


def touche_echap(event):
    affichage.delete(0, tk.END)


# ============================================================
# FENÊTRE PRINCIPALE
# ============================================================
fenetre = tk.Tk()
fenetre.title("Calculatrice scientifique ")
fenetre.geometry("360x640")
fenetre.resizable(False, False)

# --- Frame calculatrice (gauche) ---
frame_calc = tk.Frame(fenetre)
frame_calc.pack(side="left", fill="both", expand=True)

# --- Frame historique (droite, caché au départ) ---
frame_histo = tk.Frame(fenetre, width=250)

# --- Écran ---
affichage = tk.Entry(
    frame_calc,
    font=("Segoe UI", 24),
    justify="right",
    bd=0,
    relief="flat",
    insertwidth=3,
)
affichage.grid(
    row=0, column=0, columnspan=4,
    sticky="nsew",
    padx=12, pady=(12, 6),
    ipady=12,
)

# --- Grille de boutons ---
BOUTONS = [
    ["√", "%", "1/x", "^"],
    ["C", "(", ")", "/"],
    ["7", "8", "9", "*"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["0", ".", "⌫", "="],
    [" Historique", " Thème"],
]

for ligne, rangee in enumerate(BOUTONS):
    for colonne, texte in enumerate(rangee):
        bouton = tk.Button(
            frame_calc,
            text=texte,
            font=("Segoe UI", 14, "bold"),
            command=lambda t=texte: action_clic(t),
        )
        if texte == " Historique":
            bouton.grid(row=ligne + 1, column=0, columnspan=2,
                        sticky="nsew", padx=4, pady=4)
        elif texte == " Thème":
            bouton.grid(row=ligne + 1, column=2, columnspan=2,
                        sticky="nsew", padx=4, pady=4)
        else:
            bouton.grid(row=ligne + 1, column=colonne,
                        sticky="nsew", padx=4, pady=4)

# --- Poids de la grille ---
for i in range(4):
    frame_calc.columnconfigure(i, weight=1)
for i in range(1, 8):
    frame_calc.rowconfigure(i, weight=1)
frame_calc.rowconfigure(0, weight=0)

# --- Contenu du panneau historique ---
titre_histo = tk.Label(
    frame_histo,
    text=" Historique",
    font=("Segoe UI", 14, "bold"),
)
titre_histo.pack(pady=(12, 6))

zone_histo = tk.Text(
    frame_histo,
    font=("Consolas", 10),
    wrap="word",
    width=30,
    state="disabled",
    bd=0,
    relief="flat",
    padx=8, pady=8,
)
zone_histo.pack(fill="both", expand=True, padx=10, pady=6)

bouton_fermer_histo = tk.Button(
    frame_histo,
    text="✖ Fermer",
    font=("Segoe UI", 10),
    command=cacher_historique,
)
bouton_fermer_histo.pack(pady=8)

# --- Raccourcis clavier ---
fenetre.bind("<Return>", touche_entree)
fenetre.bind("<Escape>", touche_echap)

# --- Thème initial ---
appliquer_theme()

# --- Lancement ---
fenetre.mainloop()