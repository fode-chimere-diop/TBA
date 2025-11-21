# Define the Room class.

class Room:

    # Define the constructor. 
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exits = {}
    
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
        first = True
        for ex in ['N', 'E', 'S', 'O']:  # ordre lisible
            target = self.exits.get(ex, None)
            if target is not None:
                if not first:
                    exit_string += ", "
                exit_string += ex
                first = False
        if first:  # aucune sortie trouvée
            exit_string += "aucune"
        return exit_string

    # Return a long description of this room including exits.
    def get_long_description(self):
        return f"\nVous êtes {self.description}\n\n{self.get_exit_string()}\n"
