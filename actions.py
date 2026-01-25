# Description: The actions module.

# The actions module contains the functions that are called when a command is executed.
# Each function takes 3 parameters:
# - game: the game object
# - list_of_words: the list of words in the command
# - number_of_parameters: the number of parameters expected by the command
# The functions return True if the command was executed successfully, False otherwise.
# The functions print an error message if the number of parameters is incorrect.
# The error message is different depending on the number of parameters expected by the command.


# The error message is stored in the MSG0 and MSG1 variables and formatted with the command_word variable, the first word in the command.
# The MSG0 variable is used when the command does not take any parameter.
MSG0 = "\nLa commande '{command_word}' ne prend pas de paramètre.\n"
# The MSG1 variable is used when the command takes 1 parameter.
MSG1 = "\nLa commande '{command_word}' prend 1 seul paramètre.\n"

class Actions:
    @staticmethod
    def go(game, list_of_words, number_of_parameters):
        """
        Move the player in the direction specified by the parameter.
        The parameter must be a cardinal direction (N, E, S, O).

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:
        
        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> go(game, ["go", "N"], 1)
        True
        >>> go(game, ["go", "N", "E"], 1)
        False
        >>> go(game, ["go"], 1)
        False

        """
        
        player = game.player
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        # Get the direction from the list of words.
        direction = list_of_words[1].lower() 
        if direction in ("n", "nord"): # condition pour go Nord ou go N 
            direction = "N"
        elif direction in ("s", "sud"):
            direction = "S"
        elif direction in ("e", "est"):
            direction = "E"
        elif direction in ("o", "ouest"):
            direction = "O"
        elif direction in ("u", "up"):
            direction = "U"

        else:
            print(f"\nDirection '{list_of_words[1]}' non reconnue.\n")
            return False
        # Move the player in the direction specified by the parameter. 
        player.move(direction)

        return True
    @staticmethod
    def quit(game, list_of_words, number_of_parameters):
        """
        Quit the game.

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> quit(game, ["quit"], 0)
        True
        >>> quit(game, ["quit", "N"], 0)
        False
        >>> quit(game, ["quit", "N", "E"], 0)
        False

        """
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        # Set the finished attribute of the game object to True.
        player = game.player
        msg = f"\nMerci {player.nom} d'avoir joué. Au revoir.\n"
        print(msg)
        game.finished = True
        return True
    @staticmethod
    def help(game, list_of_words, number_of_parameters):
        """
        Print the list of available commands.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> help(game, ["help"], 0)
        True
        >>> help(game, ["help", "N"], 0)
        False
        >>> help(game, ["help", "N", "E"], 0)
        False

        """

        # If the number of parameters is incorrect, print an error message and return False.
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        # Print the list of available commands.
        print("\nVoici les commandes disponibles:")
        for command in game.commands.values():
            print("\t- " + str(command))
        print()
        return True
      # 🔹 Nouvelle action : afficher l'historique sur commande
    def history(game, list_of_words, number_of_parameters): #ajouter pour l'historique
        """
        Affiche l'historique des pièces déjà visitées.
        """
        l = len(list_of_words)
        # Pas de paramètre attendu
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        print(game.player.get_history())
        return True
    def back(game, list_of_words, number_of_parameters): #ajouter pour le back 
        """
    Revenir à la pièce précédente.
    Impossible si aucune pièce n'a encore été visitée.
        """
        player = game.player
        l = len(list_of_words)

        # La commande back ne prend aucun paramètre
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        # Vérifier si retour possible
        if len(player.history) == 0:
            print("\nVous ne pouvez plus reculer davantage : impossible de revenir en arrière.\n")
            return False

        # Retirer la dernière salle visitée
        previous_room = player.history.pop()

        # Mise à jour de la salle courante
        player.current_room = previous_room

        # Affichage de la nouvelle salle
        print(player.current_room.get_long_description())

        # Affichage de l'historique mis à jour
        print(player.get_history())

        return True
    # pour le look

    def look(game, list_of_words, number_of_parameters):
        """
    Affiche la description de la pièce où se trouve le joueur
    ainsi que les objets présents dans cette pièce.
        """

    # Vérifier qu'il n'y a pas de paramètre supplémentaire
        if len(list_of_words) != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(f"Commande incorrecte : {command_word}")
            return False

        room = game.player.current_room
        if room is None:
            print("\nVous n'êtes dans aucune pièce.\n")
            return False

    #description de la pièce
        print(room.get_long_description())

    #affichage des items
        print(room.get_inventory())
        if room.name == "restaurant":
            print("\n💡Indice : Il n'y a personne ici,")
            print("mais la table n°4 semble attendre quelque chose... ")
            print("Essayez de POSER (drop) le plat.")
        if room.name == "salle_secréte":
            print("\n🔒 UN COFFRE MYSTÉRIEUX : Il porte l'emblème de Gustave Eiffel.")
            print("💡 Action : Utilisez la commande 'unlock <code>' pour tenter votre chance.")
            print(f"⚠️ Attention : Il ne vous reste que {game.unlock_attempts} essais avant que l'alarme ne sonne.")
        return True
#pour pouvoir prendre l'objet
    @staticmethod
    def take(game, list_of_words, number_of_parameters):
        if len(list_of_words) != number_of_parameters + 1:
            print("Utilisation : take <nom_item>")
            return False

        item_name = list_of_words[1].lower()
        player = game.player
        room = player.current_room

        for item in room.inventaire:
            if item.nom.lower() == item_name:
                
                # --- ÉNIGME : BLOQUER SI PAS DE NOTE ---
                if item_name == "glaçons":
                    a_la_note = any(i.nom.lower() == "note" for i in player.inventaire)
                    if not a_la_note:
                        print("\n❓ Vous voyez des glaçons, mais sans indice, vous ne savez pas quoi en faire.")
                        print("Allez sur la terrasse pour chercher un indice !")
                        return False
                
                # --- MACHINE À ÉCLAIR ---
                if item_name == "eclair" and not game.machine_reparee:
                    print("La machine est cassée. L'éclair n'est pas encore prêt !")
                    return False

                # Vérification poids et ajout
                if player.current_weight() + item.poids > player.max_weight:
                    print("Trop lourd !")
                    return False

                player.inventaire.append(item)
                room.inventaire.remove(item)
                print(f"Vous avez pris : {item.nom}")
                return True
        return False
    
    #pour l'inventaire
    def inventory(game, list_of_words, number_of_parameters):
        """
    Affiche l'inventaire du joueur.
    Syntaxe : inventory
        """
        if len(list_of_words) != number_of_parameters + 1:
            print("Commande incorrecte : utilisez 'inventory'")
            return False

        if not game.player.inventaire:
            print("Votre inventaire est vide.")
            return True

        print("Vous possédez :")
        for item in game.player.inventaire:
            print(f" - {item.nom} : {item.description} ({item.poids} kg)")
        return True
    def drop(game, list_of_words, number_of_parameters):
        """
    Repose un item de l'inventaire du joueur dans la pièce actuelle.
    Syntaxe : drop <nom_item>
        """
    # Vérification du nombre de paramètres
        if len(list_of_words) != number_of_parameters + 1:
            print("Utilisation : drop <item>")
            return False

        player = game.player
        room = player.current_room
        item_name = list_of_words[1].lower()

    # Cherche l'item dans l'inventaire du joueur
        item_to_drop = next((i for i in player.inventaire if i.nom.lower() == item_name), None)
        if not item_to_drop:
            print("Vous n'avez pas cet objet.")
            return False

        if player.current_room.name == "restaurant" and item_name == "plat":
            print("✨🍽️ En le posant, vous voyez un papier collé sous l'assiette : 'Le dernier chiffre est le 1'.")
            # ✅ Correction du Crash (envoie bien les 3 arguments)
            game.player.quest_manager.check_action_objectives("poser", "restaurant", item_to_drop)
            
            # ✅ Déblocage de la sortie Up
            for r in game.rooms:
                if r.name == "salle_secréte":
                    player.current_room.exits["U"] = r
            print("✨ Un escalier vers le sommet (U) vient d'apparaître !")

        player.inventaire.remove(item_to_drop)
        player.current_room.inventaire.append(item_to_drop)
        return True

    
    def check(game, list_of_words, number_of_parameters):
        """
    Affiche l'inventaire du joueur
        """

    # check ne prend aucun paramètre
        if len(list_of_words) != number_of_parameters + 1:
            print("Utilisation : check")
            return False

        player = game.player
        print(player.check())
        return True
    #interagir avec les pnj
    @staticmethod
    def talk(game, list_of_words, number_of_parameters):
        """
        talk <someone> : fait parler un PNJ présent dans la pièce.
        """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        player = game.player
        room = player.current_room
        target = list_of_words[1].strip().lower()

        for name, character in room.characters.items():
            if name.lower() == target:
                # On valide l'objectif "parler" dans le QuestManager
                game.player.quest_manager.check_action_objectives("parler", character.name)

                # --- 🎯 NIVEAU 3 : ACTIVATION DU JEU DES COULEURS ---
                if character.name.lower() == "couleurs":
                    # Cette ligne déclenche l'affichage de la quête sur ton écran
                    game.player.quest_manager.activate_quest("Le Maître des Couleurs")
                    character.get_msg()
                    return True

                # --- NIVEAU 1 : GARDE ET BOULANGER ---
                if character.name.lower() == "garde":
                    print("\nGarde : 'Halte ! Je ne laisse passer personne sans une autorisation... ou un bon éclair au chocolat.'")
                    return True

                elif character.name.lower() == "boulanger":
                    if game.machine_reparee:
                        print("\nBoulanger : 'Merci encore pour votre aide ! Mes éclairs sont à votre disposition.'")
                    else:
                        print("\nBoulanger : 'Quelle catastrophe... Ma machine est en panne. Il me faudrait un tournevis pour la réparer.'")
                    return True

                # --- NIVEAU 2 : AMBASSADEURS ---
                if character.name.lower() == "mr_red":
                    game.mr_red_enigme_donnee = True
                    character.get_msg()
                    return True
                
                if character.name.lower() == "mr_white":
                    game.mr_white_enigme_donnee = True
                    character.get_msg()
                    return True
                
                if character.name.lower() == "mr_blue":
                    game.mr_blue_enigme_donnee = True
                    character.get_msg()
                    return True

                # Autres PNJ (messages en boucle : barman, chef, etc.)
                character.get_msg()
                return True 

        print(f"\nIl n'y a pas de '{list_of_words[1]}' ici.\n")
        return False

    # --- MÉTHODE GIVE (Action réelle) ---
    @staticmethod
    def give(game, list_of_words, number_of_parameters):
        """
        Syntaxe : give <objet> <personnage>
        """
        if len(list_of_words) != 3:
            print("Utilisation : give <objet> <personnage>")
            return False 

        item_name = list_of_words[1].lower()
        target = list_of_words[2].lower()
        player = game.player
        room = player.current_room

        if target not in [n.lower() for n in room.characters.keys()]:
            print(f"{target} n'est pas ici.")
            return False

        item_to_give = next((i for i in player.inventaire if i.nom.lower() == item_name), None)

        if item_to_give is None:
            print(f"Vous n'avez pas de '{item_name}' dans votre inventaire.")
            return False

        # --- LOGIQUE DES ÉCHANGES ---

        # CAS DU GARDE (L'Éclair) - DÉBLOQUE LE NIVEAU 2
        if target == "garde" and item_name == "eclair":
            print(f"\nVous donnez l'éclair au garde.")
            print("Garde : 'Oh merci ! Il a l'air délicieux. Allez, je vous laisse passer !'")
            print("Le garde vous glisse un secret : 'Retenez bien ce chiffre pour le code final : 8'")
            
            player.quest_manager.check_action_objectives("donner", target, item_to_give)
            
            game.rooms[0].exits["U"] = game.hall_1
            player.inventaire.remove(item_to_give)
            game.eclair_donne_au_garde = True

            # 🗡️ ACTIVATION DES QUÊTES DU NIVEAU 2 ICI
            player.quest_manager.activate_quest("Énigme de Mr_Red")
            player.quest_manager.activate_quest("Énigme de Mr_White")
            player.quest_manager.activate_quest("Énigme de Mr_Blue")
            return True

        # CAS DU BOULANGER (Le Tournevis)
        elif target == "boulanger" and item_name == "tournevis":
            print(f"\nVous donnez le tournevis au boulanger.")
            print("Boulanger : 'Merci ! Je répare la machine tout de suite. Voilà, elle fonctionne !'")
            
            player.quest_manager.check_action_objectives("donner", target, item_to_give)
            
            player.inventaire.remove(item_to_give)
            game.machine_reparee = True
            return True

        # MR_RED
        elif target == "mr_red":
            if item_name in ("drapeau_sénégal", "drapeau_senegal"):
                print("\nMr_Red : 'Correct.'")
                player.quest_manager.check_action_objectives("donner", target, item_to_give)
                player.inventaire.remove(item_to_give)
                game.mr_red_enigme_resolue = True
                game.try_spawn_france_pnj()
                return True
            else:
                return Actions._handle_wrong_flag(game)

        # MR_WHITE
        elif target == "mr_white":
            if item_name == "drapeau_turquie":
                print("\nMr_White : 'Exact. Tu as l'esprit vif.'")
                player.quest_manager.check_action_objectives("donner", target, item_to_give)
                player.inventaire.remove(item_to_give)
                game.mr_white_enigme_resolue = True
                game.try_spawn_france_pnj()
                return True
            else:
                return Actions._handle_wrong_flag(game)

        # MR_BLUE
        elif target == "mr_blue":
            if item_name == "drapeau_mexique":
                print("\nMr_Blue : 'Exact. Tu as bien observé.'")
                player.quest_manager.check_action_objectives("donner", target, item_to_give)
                player.inventaire.remove(item_to_give)
                game.mr_blue_enigme_resolue = True
                game.try_spawn_france_pnj()
                return True
            else:
                return Actions._handle_wrong_flag(game)

        # ÉCHANGES NIVEAU 4
        elif target == "barman" and item_name == "glaçons":
            print("\n🧊 Barman : 'Parfait ! Voici votre bouteille d'élixir.'")
            player.inventaire.remove(item_to_give)
            from item import Item
            player.inventaire.append(Item("bouteille", "Une bouteille d'élixir rare.", 0.5))
            return True

        elif target == "chef" and item_name == "bouteille":
            print("\n🍳 Chef : 'Magnifique ! Voici le plat à poser au Restaurant !'")
            player.inventaire.remove(item_to_give)
            from item import Item
            player.inventaire.append(Item("plat", "Le plat signature du chef.", 0.8))
            return True

        print(f"{target.capitalize()} ne semble pas intéressé par cet objet.")
        return False

    @staticmethod
    def _handle_wrong_flag(game):
        """Méthode interne pour gérer les erreurs de drapeaux"""
        print("Ambassadeur : 'Non. Ce n'est pas le bon drapeau.'")
        game.wrong_flags += 1
        if game.wrong_flags >= 3:
            print("\n" + "!"*50 + "\n💀 GAME OVER : ERREUR DIPLOMATIQUE !\n" + "!"*50)
            # On déclenche le reset automatique au lieu du Game Over
            game.reset_niveau_2()
        else:
            print(f"⚠️ Attention : {3 - game.wrong_flags} essais restants.")
        return False

    
    #GIVE
    #@staticmethod
    """def give(game, list_of_words, number_of_parameters):
        Syntaxe : give <objet> <personnage>
        if len(list_of_words) != 3:
            print("Utilisation : give <objet> <personnage>")
            return False

        item_name = list_of_words[1].lower()
        target = list_of_words[2].lower()
        player = game.player
        room = player.current_room

        # 1. Vérifier que le PNJ est bien présent dans la pièce
        if target not in [n.lower() for n in room.characters.keys()]:
            print(f"{target} n'est pas ici.")
            return False

        # 2. Chercher l'objet dans l'inventaire du joueur
        item_to_give = None
        for item in player.inventaire:
            if item.nom.lower() == item_name:
                item_to_give = item
                break

        if item_to_give is None:
            print(f"Vous n'avez pas de '{item_name}' dans votre inventaire.")
            return False

        # --- LOGIQUE SPÉCIFIQUE POUR LES ÉCHANGES ---

        # CAS DU GARDE (L'Éclair)
        if target == "garde" and item_name == "eclair":
            print(f"\nVous donnez l'éclair au garde.")
            print("Garde : 'Oh merci ! Il a l'air délicieux. Vous pouvez passer !'")
            
            player.inventaire.remove(item_to_give)
            game.eclair_donne_au_garde = True # Déclenche la victoire
            
            # Validation de la quête
            player.quest_manager.check_action_objectives("donner", "eclair")
            return True

        # CAS DU BOULANGER (Le Tournevis)
        if target == "boulanger" and item_name == "tournevis":
            print(f"\nVous donnez le tournevis au boulanger.")
            print("Boulanger : 'Merci ! Je vais pouvoir réparer la machine à éclairs.'")
            
            player.inventaire.remove(item_to_give)
            game.machine_reparee = True # Débloque l'item éclair dans la pièce
            
            # Validation d'une éventuelle quête
            player.quest_manager.check_action_objectives("donner", "tournevis")
            return True

        # Si ce n'est pas le bon objet ou le bon PNJ
        print(f"{target} ne sait pas quoi faire de cet objet.")
        return False
    """
# ajout pour les quetes
    @staticmethod
    def quests(game, list_of_words, number_of_parameters):
        """
        Show all quests and their status.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup("TestPlayer")
        >>> Actions.quests(game, ["quests"], 0)
        <BLANKLINE>
        📋 Liste des quêtes:
          ❓ Grand Explorateur (Non activée)
          ❓ Grand Voyageur (Non activée)
          ❓ Découvreur de Secrets (Non activée)
        <BLANKLINE>
        True
        >>> Actions.quests(game, ["quests", "param"], 0)
        <BLANKLINE>
        La commande 'quests' ne prend pas de paramètre.
        <BLANKLINE>
        False

        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        # Show all quests
        game.player.quest_manager.show_quests()
        return True


    @staticmethod
    def quest(game, list_of_words, number_of_parameters):
        """
        Show details about a specific quest.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup("TestPlayer")
        >>> Actions.quest(game, ["quest", "Grand", "Voyageur"], 1)
        <BLANKLINE>
        📋 Quête: Grand Voyageur
        📖 Déplacez-vous 10 fois entre les lieux.
        <BLANKLINE>
        Objectifs:
          ⬜ Se déplacer 10 fois (Progression: 0/10)
        <BLANKLINE>
        🎁 Récompense: Bottes de voyageur
        <BLANKLINE>
        True
        >>> Actions.quest(game, ["quest"], 1)
        <BLANKLINE>
        La commande 'quest' prend 1 seul paramètre.
        <BLANKLINE>
        False

        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n < number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        # Get the quest title from the list of words (join all words after command)
        quest_title = " ".join(list_of_words[1:])

        # Prepare current counter values to show progress
        current_counts = {
            "Se déplacer": game.player.move_count
        }

        # Show quest details
        game.player.quest_manager.show_quest_details(quest_title, current_counts)
        return True


    @staticmethod
    def activate(game, list_of_words, number_of_parameters):
        """
        Activate a specific quest.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup("TestPlayer")
        >>> Actions.activate(game, ["activate", "Grand", "Voyageur"], 1) # doctest: +ELLIPSIS
        <BLANKLINE>
        🗡️  Nouvelle quête activée: Grand Voyageur
        📝 Déplacez-vous 10 fois entre les lieux.
        <BLANKLINE>
        True
        >>> Actions.activate(game, ["activate"], 1)
        <BLANKLINE>
        La commande 'activate' prend 1 seul paramètre.
        <BLANKLINE>
        False

        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n < number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        # Get the quest title from the list of words (join all words after command)
        quest_title = " ".join(list_of_words[1:])

        # Try to activate the quest
        if game.player.quest_manager.activate_quest(quest_title):
            return True

        msg1 = f"\nImpossible d'activer la quête '{quest_title}'. "
        msg2 = "Vérifiez le nom ou si elle n'est pas déjà active.\n"
        print(msg1 + msg2)
        # print(f"\nImpossible d'activer la quête '{quest_title}'. \
        #             Vérifiez le nom ou si elle n'est pas déjà active.\n")
        return False


    @staticmethod
    def rewards(game, list_of_words, number_of_parameters):
        """
        Display all rewards earned by the player.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup("TestPlayer")
        >>> Actions.rewards(game, ["rewards"], 0)
        <BLANKLINE>
        🎁 Aucune récompense obtenue pour le moment.
        <BLANKLINE>
        True
        >>> Actions.rewards(game, ["rewards", "param"], 0)
        <BLANKLINE>
        La commande 'rewards' ne prend pas de paramètre.
        <BLANKLINE>
        False
        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        # Show all rewards
        game.player.show_rewards()
        return True
   
    @staticmethod
    def colors(game, list_of_words, number_of_parameters):
        """
        Mini-jeu: proposer un ordre de 5 couleurs.
        Usage: colors R B J V O
        Retour: nombre de couleurs bien placées ou Game Over si trop d'essais.
        """
        # 1. Vérif nombre de paramètres (colors + 5)
        if len(list_of_words) != number_of_parameters + 1:
            print("\nUtilisation : colors R B J V O\n")
            return False

        room = game.player.current_room
        if room is None:
            print("\nVous n'êtes dans aucune pièce.\n")
            return False

        # 2. Diminuer le nombre d'essais restants
        game.couleurs_attempts -= 1

        # 3. Récupérer le code attendu et la proposition du joueur
        code = [c.upper() for c in game.couleurs_code]   # ex: ["R","B","J","V","O"]
        guess = [w.upper() for w in list_of_words[1:]]
        allowed = {"R", "B", "J", "V", "O"}

        # 4. Vérifications (lettres autorisées et doublons)
        for c in guess:
            if c not in allowed:
                print(f"\nCouleur '{c}' invalide. Utilise seulement : R B J V O\n")
                return False

        if len(set(guess)) != 5:
            print("\nTu dois donner 5 couleurs différentes (pas de doublons).\n")
            return False

        # 5. Comptage des bonnes réponses BIEN PLACÉES
        good = 0
        for i in range(5):
            if guess[i] == code[i]:
                good += 1

        # 6. Gestion des résultats (Victoire)
        if good == 5:
            print("\n" + "="*50)
            print("🎉 BRAVO ! Tu as trouvé le bon ordre !")
            print("TU AS OBTENU LE CHIFFRE : 8")
            print("Le PNJ te laisse passer vers le niveau 4.")
            print("="*50 + "\n")
            
            # ✅ VALIDATION DE LA QUÊTE : On envoie "colors" pour correspondre à l'objectif
            game.player.quest_manager.check_action_objectives("colors", "colors")
            game.player.move_count = 0
            # Déblocage de la sortie
            target_room = next(r for r in game.rooms if r.name == "terrasse_2")
            game.player.current_room.exits["N"] = target_room
            game.acces_niveau_4 = True

            # 🗡️ ACTIVATION DE LA QUÊTE DU NIVEAU 4
            game.player.quest_manager.activate_quest("Le Protocole du Sommet")
            
            return True

        # 7. Si ce n'est pas bon, vérifier s'il reste des essais
        if game.couleurs_attempts > 0:
            print(f"\n❌ Pas encore. Il y a {good} bonne(s) réponse(s) bien placée(s).")
            print(f"⚠️ Attention : Il vous reste {game.couleurs_attempts} essais avant le verrouillage !\n")
        else:
            # 💀 CONDITION DE DÉFAITE NIVEAU 3
            print("\n" + "!"*50)
            print("💀 GAME OVER : SYSTÈME DE SÉCURITÉ ACTIVÉ !")
            print("Vous avez échoué trop de fois à synchroniser les projecteurs.")
            print("L'accès à la tour est définitivement verrouillé.")
            print("!"*50)
            # Réinitialisation des essais
            game.couleurs_attempts = 20
            
            # On renvoie le joueur au hall du 2ème étage
            game.player.current_room = game.hall_2
            
        return True
    
    @staticmethod
    def unlock(game, list_of_words, number_of_parameters):
        player = game.player
        
        # Vérification du lieu
        if player.current_room.name != "salle_secréte":
            print("\nIl n'y a aucun coffre ici à ouvrir.")
            return False

        # Vérification des paramètres
        if len(list_of_words) < 2:
            print("\nUsage : unlock <combinaison>")
            return False

        choix = list_of_words[1]

        # --- VICTOIRE ---
        if choix == "1887":
            print("\n" + "★"*50)
            print("         ✨ L'HÉRITAGE D'EIFFEL EST À VOUS ✨")
            print("          LE COFFRE S'OUVRE ENFIN : 1887")
            print("★"*50)
            print("\nLe mécanisme tourne parfaitement. Le couvercle se soulève...")
            print("Félicitations ! Vous avez trouvé le CROISSANT D'OR !")
            game.player.quest_manager.check_action_objectives("unlock", "1887")
            game.finished = True # Ici on garde True car c'est la fin du jeu
            return True

        # --- ÉCHEC : Gestion des essais et des indices ---
        game.unlock_attempts -= 1 # On diminue le compteur
        
        if game.unlock_attempts > 0:
            print(f"\n❌ Code incorrect ! Il vous reste {game.unlock_attempts} essais.")
            print("\n💡 Besoin d'un rappel ? Voici un indice :")
            
            if game.unlock_attempts == 4:
                print("Indice du Niveau 1 : 'Je suis le premier, l'unique (1).'")
            elif game.unlock_attempts == 3:
                print("Indice du Niveau 2 : 'Le nombre de pieds de la Tour (4), multiplié par deux (8).'")
            elif game.unlock_attempts == 2:
                print("Indice du Niveau 3 : 'L'infini mis debout (8).'")
            elif game.unlock_attempts == 1:
                print("Indice du Niveau 4 : 'Le chiffre porte-bonheur croisé au restaurant (7).'")
        else:
            # 🔄 RESET AU LIEU DE FINISHED
            # On ne met PAS game.finished = True ici !
            # La méthode loose() de game.py va détecter que unlock_attempts <= 0 
            # et va téléporter le joueur au restaurant.
            print("\n🚨 ALARME DÉCLENCHÉE ! Trop de tentatives infructueuses.")
            print("Le système vous éjecte de la salle secrète !")

        return True