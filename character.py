import random

class Character:
    def __init__(self, name, description, current_room, msgs):
        self.name = name
        self.description = description
        self.current_room = current_room
        self.msgs = msgs
        # Pour faire défiler les messages en boucle
        self._msgs_queue = list(msgs)  # copie
        self._msgs_done = []           # ceux déjà affichés

    def __str__(self):
        return f"{self.name} : {self.description}"
######################deplacement##########################
    #def move(self):
       # """
       # Déplacement aléatoire du PNJ :
       # - 1 chance sur 2 de rester sur place
       #- sinon, va dans une pièce adjacente au hasard
        #"""

        # 1 chance sur 2 de ne pas bouger
        #if random.choice([True, False]) is False:
            #return False

        # Récupérer les sorties possibles
        #rooms = []
        #for room in self.current_room.exits.values():
            #if room is not None:
                #rooms.append(room)

        #if not rooms:
            #return False

        # Choix aléatoire d'une pièce
        #self.current_room = random.choice(rooms)
        #return True
###################################################################################
# pour faire defiler les messages 
    def get_msg(self):
        """
        Affiche un message du PNJ, en alternant/cyclant.
        """
        if not self.msgs:
            print(f"{self.name} n'a rien à dire.")
            return

        # Si on a épuisé la "queue", on la re-remplit avec ceux déjà dits
        if len(self._msgs_queue) == 0:
            self._msgs_queue = self._msgs_done
            self._msgs_done = []

        msg = self._msgs_queue.pop(0)  # pop(0) -> premier message
        self._msgs_done.append(msg)

        print(msg)
