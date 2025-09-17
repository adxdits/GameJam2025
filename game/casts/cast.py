import arcade


# Classe gérant la validation des QTE pour cast un sort
class Cast:
    index_current_combo = 0  # Index de la touche actuelle à valider
    
    # Liste contenant la suite des saisies
    def __init__(self):
        self.combinations = {}
        self.current_combo = []
        #print(f"{target.name} gagne +5 attaque pour 3 tours !")
        
    def set_data_combo(self, combinations: dict, words: list, lvl: int):
        self.combinations = combinations
        # Mise en place du QTE complet
        self.current_combo = []          # <-- vider l'ancienne combo
        self.index_current_combo = 0
        self.current_combo.extend(self.combinations["TYPES"][words[0]])
        if lvl >= 2: 
            self.current_combo.extend(self.combinations["QUALIFICATIFS"][words[1]])
        if lvl == 3: 
            self.current_combo.extend(self.combinations["CIBLES"][words[2]])
        
    def check_qte(self, key):
        if len(self.combinations) == 0 or len(self.current_combo) == 0:
            raise ValueError("Combinations dict & words list must be set before checking QTE.")
        
        n = len(self.current_combo)
        if key == self.current_combo[self.index_current_combo]:
            self.index_current_combo += 1
            if self.index_current_combo == n:
                self.index_current_combo = 0  # Reset pour le prochain QTE
                return 1 # QTE réussi
            return 0 # QTE continue
        else:
            print("QTE échoué !")
            self.index_current_combo = 0  # Reset pour le prochain QTE
            return -1 # QTE échoué
    
    def print_stratagem_qte(self): # Appel la fonction d'affichage des touches sur l'écran OU appel la fonction de mise à jour de la liste affiché à l'écran
        pass