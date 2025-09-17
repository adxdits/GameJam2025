import arcade
import random

# =========================
# Données
# =========================

TYPES = {
    "Massage":       [arcade.key.LEFT,  arcade.key.RIGHT, arcade.key.LEFT,  arcade.key.RIGHT],   # va-et-vient
    "Lissage":       [arcade.key.RIGHT, arcade.key.RIGHT, arcade.key.RIGHT, arcade.key.RIGHT],   # gestes rectilignes
    "Polissage":     [arcade.key.UP,    arcade.key.RIGHT, arcade.key.DOWN,  arcade.key.LEFT],    # mouvement circulaire
    "Hydratation":   [arcade.key.UP,    arcade.key.UP,    arcade.key.DOWN,  arcade.key.DOWN],    # vagues
    "Réchauffage":   [arcade.key.UP,    arcade.key.RIGHT, arcade.key.UP,    arcade.key.RIGHT],   # friction qui monte
    "Rafraîchissement":[arcade.key.DOWN,arcade.key.LEFT,  arcade.key.DOWN,  arcade.key.LEFT],    # souffle frais
    "Peignage":      [arcade.key.UP,    arcade.key.DOWN,  arcade.key.UP,    arcade.key.DOWN],    # peigne haut-bas
    "Brillance":     [arcade.key.UP,    arcade.key.LEFT,  arcade.key.UP,    arcade.key.LEFT],    # éclats en zig
    "Couture":       [arcade.key.LEFT,  arcade.key.LEFT,  arcade.key.RIGHT, arcade.key.RIGHT],   # point aller/retour
    "Démêlage":      [arcade.key.DOWN,  arcade.key.UP,    arcade.key.DOWN,  arcade.key.UP],      # contre-peigne
}

QUALIFICATIFS = {
    "exquis":        [arcade.key.RIGHT, arcade.key.UP,    arcade.key.RIGHT, arcade.key.UP],
    "délicat":       [arcade.key.LEFT,  arcade.key.UP,    arcade.key.LEFT,  arcade.key.UP],
    "parfumé":       [arcade.key.RIGHT, arcade.key.DOWN,  arcade.key.RIGHT, arcade.key.DOWN],
    "divin":         [arcade.key.UP,    arcade.key.RIGHT, arcade.key.RIGHT, arcade.key.UP],
    "soyeux":        [arcade.key.DOWN,  arcade.key.RIGHT, arcade.key.RIGHT, arcade.key.DOWN],
    "scintillant":   [arcade.key.UP,    arcade.key.LEFT,  arcade.key.LEFT,  arcade.key.UP],
    "inutile":       [arcade.key.LEFT,  arcade.key.DOWN,  arcade.key.LEFT,  arcade.key.DOWN],
    "urgent":        [arcade.key.UP,    arcade.key.UP,    arcade.key.RIGHT, arcade.key.RIGHT],
    "royal":         [arcade.key.DOWN,  arcade.key.DOWN,  arcade.key.LEFT,  arcade.key.LEFT],
    "cosmétique":    [arcade.key.RIGHT, arcade.key.RIGHT, arcade.key.UP,    arcade.key.UP],
}

CIBLES = {
    "des cheveux":     [arcade.key.UP,    arcade.key.LEFT,  arcade.key.DOWN,  arcade.key.RIGHT],
    "de la moustache": [arcade.key.LEFT,  arcade.key.DOWN,  arcade.key.RIGHT, arcade.key.UP],
    "des bottes":      [arcade.key.DOWN,  arcade.key.DOWN,  arcade.key.RIGHT, arcade.key.LEFT],
    "du plastron":     [arcade.key.RIGHT, arcade.key.LEFT,  arcade.key.UP,    arcade.key.DOWN],
    "des gants":       [arcade.key.LEFT,  arcade.key.RIGHT, arcade.key.DOWN,  arcade.key.UP],
    "de l’armure":     [arcade.key.RIGHT, arcade.key.UP,    arcade.key.LEFT,  arcade.key.DOWN],
    "des sourcils":    [arcade.key.UP,    arcade.key.DOWN,  arcade.key.LEFT,  arcade.key.RIGHT],
    "du casque":       [arcade.key.UP,    arcade.key.UP,    arcade.key.LEFT,  arcade.key.RIGHT],
    "des ongles":      [arcade.key.DOWN,  arcade.key.LEFT,  arcade.key.UP,    arcade.key.RIGHT],
    "du bouclier":     [arcade.key.LEFT,  arcade.key.UP,    arcade.key.RIGHT, arcade.key.DOWN],
}

LISTES = {
    "TYPES" : TYPES,
    "QUALIFICATIFS" : QUALIFICATIFS,
    "CIBLES" : CIBLES,
}


# =========================
# Vérification des incohérences
# =========================
def est_coherent(type_mot: str, cible: str) -> bool:
    """Vérifie si la combinaison type + cible a du sens."""
    # Exemple d'incohérences à éviter :
    if type_mot in ["Peignage", "Démêlage", "Lissage"] and cible not in ["des cheveux", "de la moustache", "des sourcils"]:
        return False
    if type_mot in ["Couture"] and cible not in ["des bottes", "des gants"]:
        return False
    if type_mot in ["Massage"] and cible not in ["des cheveux", "de la moustache", "des sourcils", "des ongles"]:
        return False
    return True

# =========================
# Génération de phrase
# =========================
def generer_phrase(niveau: str):
    type_mot = random.choice(list(TYPES.keys()))
    qualitatif = random.choice(list(QUALIFICATIFS.keys()))
    cible = random.choice(list(CIBLES.keys()))

    # Réessayer si incohérent
    while not est_coherent(type_mot, cible):
        type_mot = random.choice(list(TYPES.keys()))
        cible = random.choice(list(CIBLES.keys()))

    if niveau == "1":
        return [type_mot]
    elif niveau == "2":
        return [type_mot, qualitatif]
    elif niveau == "3":
        return [type_mot, qualitatif, cible]
    else:
        raise ValueError("Le niveau doit être une string '1', '2' ou '3'.")

# =========================
# Exemple d'utilisation
# =========================
if __name__ == "__main__":
    for n in range(10):
        for n in ["1", "2", "3"]:
            print(f"Niveau {n} :", generer_phrase(n))
