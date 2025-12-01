#ajouter A
class Item:
    def __init__(self,nom,description,poids=1):
        self.description=description
        self.nom=nom
        self.poids=poids
    def __str__(self):
        
        return f"{self.name} : {self.description} ({self.weight} kg)" 