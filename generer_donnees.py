# =========================================================
# Projet : Tableau de bord Supply Chain - LaitNord (fictif)
# Script : génère un fichier Excel par site logistique
# =========================================================

# --- BLOC 1 : les outils ---------------------------------
import os            # pour créer des dossiers et des chemins de fichiers
import random        # pour générer des nombres aléatoires
import pandas as pd  # pour créer des tableaux et les écrire dans Excel

random.seed(42)  # rend les nombres "aléatoires" identiques à chaque exécution


# --- BLOC 2 : les paramètres -----------------------------
# Chaque site a une "taille" : Laval est le plus gros (x1,3), Le Mans le plus petit (x0,8)
SITES = {
    "Laval": 1.3,
    "Rennes": 1.0,
    "Le Mans": 0.8,
    "Angers": 0.9,
}

# Budget mensuel de base pour chaque type de coût (pour un site de taille 1)
TYPES_COUTS = {
    "Transport": 40000,
    "Stockage": 25000,
    "Manutention": 15000,
}

# Les 12 mois de l'année 2026 (le 1er de chaque mois)
MOIS = [pd.Timestamp(2026, m, 1) for m in range(1, 13)]

# Dossier où seront déposés les fichiers des sites
DOSSIER = "donnees_sites"
os.makedirs(DOSSIER, exist_ok=True)  # crée le dossier s'il n'existe pas


# --- BLOC 3 : les fonctions de génération ----------------
def generer_couts(site, taille):
    """Crée le tableau des coûts : 1 ligne par mois et par type de coût."""
    lignes = []
    for mois in MOIS:
        # Volume transporté ce mois-ci (environ 1 000 t x taille, +/- 10 %)
        volume = round(1000 * taille * random.uniform(0.9, 1.1))
        for type_cout, base in TYPES_COUTS.items():
            budget = round(base * taille, -2)                  # arrondi à la centaine
            reel = round(budget * random.uniform(0.90, 1.15))  # de -10 % à +15 % du budget
            lignes.append({
                "Site": site,
                "Mois": mois,
                "Type_cout": type_cout,
                "Budget": budget,
                "Reel": reel,
                "Volume_tonnes": volume,
            })
    return pd.DataFrame(lignes)


def generer_livraisons(site, taille):
    """Crée le tableau des livraisons : 1 ligne par mois."""
    lignes = []
    for mois in MOIS:
        total = round(800 * taille * random.uniform(0.9, 1.1))
        a_l_heure = round(total * random.uniform(0.88, 0.98))  # 88 % à 98 % à l'heure
        lignes.append({
            "Site": site,
            "Mois": mois,
            "Commandes_total": total,
            "Commandes_a_l_heure": a_l_heure,
        })
    return pd.DataFrame(lignes)


def ajouter_erreurs(couts, site):
    """Ajoute volontairement 3 erreurs, comme dans de vraies données."""
    # Erreur 1 : une valeur manquante dans la colonne Reel
    couts.loc[random.randrange(len(couts)), "Reel"] = None
    # Erreur 2 : le nom du site écrit en minuscules ("laval" au lieu de "Laval")
    couts.loc[random.randrange(len(couts)), "Site"] = site.lower()
    # Erreur 3 : une ligne en double
    doublon = couts.iloc[[random.randrange(len(couts))]]
    couts = pd.concat([couts, doublon], ignore_index=True)
    return couts


# --- BLOC 4 : le programme principal ---------------------
for site, taille in SITES.items():
    couts = generer_couts(site, taille)
    couts = ajouter_erreurs(couts, site)
    livraisons = generer_livraisons(site, taille)

    # Nom du fichier : "site_Le_Mans.xlsx" (pas d'espace dans les noms de fichiers)
    nom_fichier = os.path.join(DOSSIER, f"site_{site.replace(' ', '_')}.xlsx")

    # Un fichier Excel avec 2 feuilles : "Couts" et "Livraisons"
    with pd.ExcelWriter(nom_fichier) as writer:
        couts.to_excel(writer, sheet_name="Couts", index=False)
        livraisons.to_excel(writer, sheet_name="Livraisons", index=False)

    print(f"Fichier créé : {nom_fichier} ({len(couts)} lignes de coûts)")

print("Terminé !")