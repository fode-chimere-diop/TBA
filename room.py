class Room:

    # Define the constructor. 
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exits = {}
        self.inventaire =[] # ajouter INVENTAIRE
    
    # Define the get_exit method.
    def get_exit(self, direction):

        # Return the room in the given direction if it exists.
        
        if direction in self.exits.keys():
            return self.exits[direction]
        else:
            return None
    # Ajoute une sortie (pratique pour construire la carte) A
    def set_exit(self, direction, room):
        """
        direction : 'N','S','E','O'
        room : objet Room (ou None pour indiquer pas de sortie)
        """
        self.exits[direction.upper()] = room
    
    # Return a string describing the room's exits.
    # Retourne une chaîne listant les sorties disponibles A
    def get_exit_string(self):
        exit_string = "Sorties : "
        sorties=[]
        for ex in ['N', 'E', 'S', 'O']:  # ordre lisible
           if self.exits.get(ex) is not None:
              sorties.append(ex)

        if sorties:
          exit_string += ", ".join(sorties)
        else:
          exit_string += "aucune"

        return exit_string

    # Return a long description of this room including exits.
    #def get_long_description(self):
       #return f"\nVous êtes {self.description}\n\n{self.get_exit_string()}\n" 
  
    def get_long_description(self):
        """
        Retourne la description de la pièce et ses sorties,
        mais PAS les objets (inventaire) !
        """
        txt = f"\nVous êtes {self.description}\n\n"
        txt += self.get_exit_string() + "\n"
        return txt
    #pour inventaire 

    def get_inventory(self):
        if len(self.inventaire) == 0:
            return "Il n'y a rien ici.\n"

        txt = "La pièce contient :\n"
        for item in self.inventaire:
            txt += f" - {item.nom} : {item.description}\n"
        return txt
