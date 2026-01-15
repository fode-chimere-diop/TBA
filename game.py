# Description: Game class

# Import modules
from room import Room
from player import Player
from item import Item
from command import Command
from actions import Actions
from character import Character
from quest import Quest
DEBUG = False        # AJOUTÉ
TIME_LIMIT = 20     # AJOUTÉ (temps max)
class Game:

    # Constructor
    def __init__(self):
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None
        self.start_room = None  #  on crée une variable pour la pièce de départ
        ###########deplacement########
        #self.characters = []
        #############################
        ############1_jeu################
        self.machine_reparee = False
        self.eclair_donne_au_garde = False
        ################################
        ############2_jeu################
        self.mr_red_enigme_donnee = False
        self.mr_red_enigme_resolue = False
        self.mr_white_enigme_donnee = False
        self.mr_white_enigme_resolue = False
        self.mr_blue_enigme_donnee = False
        self.mr_blue_enigme_resolue = False
        #################################
        self.hall_1 = None
        self.final_pnj_spawned = False
        self.france_riddle_unlocked = False
        self.france_win = False
        # --- Mini-jeu couleurs (accès niveau 4) ---
        self.couleurs_code = ["R", "B", "J", "V", "O"]  # tu peux changer / randomiser
        self.couleurs_jeu_actif = False
        self.acces_niveau_4 = False
    
    # Setup the game
    def setup(self):

        # Setup commands
        help = Command("help", " : afficher cette aide", Actions.help, 0)
        self.commands["help"] = help

        quit = Command("quit", " : quitter le jeu", Actions.quit, 0)
        self.commands["quit"] = quit

        go = Command("go", " <direction> : se déplacer dans une direction cardinale (N, E, S, O)", Actions.go, 1)
        self.commands["go"] = go

        history_cmd = Command("history", " : afficher l'historique des pièces visitées", Actions.history, 0)
        self.commands["history"] = history_cmd #ajouter pour l'historique

        back_cmd = Command("back", " : revenir à la pièce précédente", Actions.back, 0)
        self.commands["back"] = back_cmd #ajouter pour back 
          #pour l'inventaire

        inventory_cmd = Command("inventory", " : afficher votre inventaire", Actions.inventory, 0)
        self.commands["inventory"] = inventory_cmd

        # pour le look
        look_cmd = Command("look", " : observer la pièce et voir les objets", Actions.look, 0)
        self.commands["look"] = look_cmd

        take_cmd = Command("take", " <nom_item> : prendre un objet dans la pièce", Actions.take, 1)
        self.commands["take"] = take_cmd
        #pour le drop

        drop_cmd = Command("drop", " <item> : reposer un objet", Actions.drop, 1)
        self.commands["drop"] = drop_cmd
        #pour check 

        check_cmd = Command("check"," : afficher l'inventaire du joueur",Actions.check,0)
        self.commands["check"] = check_cmd

        #pour parler avec les pnj
        talk_cmd = Command("talk", " <nom> : parler à un personnage présent", Actions.talk, 1)
        self.commands["talk"] = talk_cmd
        #quests
        quests = Command("quests" , " : afficher la liste des quêtes" , Actions.quests, 0)
        self.commands["quests"] = quests
        #quest
        quest = Command("quest" , " <titre> : afficher les détails d'une quête" , Actions.quest, 1)
        self.commands["quest"] = quest
        #activate
        activate = Command("activate" , " <titre> : activer une quête " , Actions.activate, 1)
        self.commands["activate"] = activate
        #rewards
        rewards = Command("rewards" , " : afficher vos récompenses " , Actions.rewards, 0)
        self.commands["rewards"] = rewards
        #give
        give_cmd = Command("give", " <objet> <personnage> : donner un objet", Actions.give, 2)
        self.commands["give"] = give_cmd
        # quetes
        quests_cmd = Command("quests", " : afficher les quêtes", Actions.quests, 0)
        self.commands["quests"] = quests_cmd
        # couleurs mini-jeu
        colors_cmd = Command("colors", " <5 lettres> : proposer un ordre de couleurs", Actions.colors, 5)
        self.commands["colors"] = colors_cmd
        
        # Setup rooms
        # Niveau 1
        hall_0 = Room("hall_0", "dans le hall du rez-de-chaussée")
        #je vais mettre le texte ici
        self.rooms.append(hall_0)
        boulangerie = Room("boulangerie", "dans la boulangerie")
        #trouver une solution pour eviter trop de \n
        self.rooms.append(boulangerie)
        salle_du_garde = Room("salle_du_garde", "dans la salle du garde")
        self.rooms.append(salle_du_garde)
        local_technique = Room("local_technique", "dans le local technique")
        self.rooms.append(local_technique)

        # Niveau 2
        escalier_vers_le_1er = Room("escalier_vers_le_1er", "")
        self.rooms.append(escalier_vers_le_1er)
        hall_1 = Room("hall_1", "")
        self.rooms.append(hall_1)
        self.hall_1 = hall_1  # pour usage ultérieur
        pays_1 = Room("pays_1", "")
        self.rooms.append(pays_1)
        pays_2 = Room("pays_2", "")
        self.rooms.append(pays_2)
        pays_3 = Room("pays_3", "")
        self.rooms.append(pays_3)

        # Niveau 3
        escalier_vers_le_2eme = Room("escalier_vers_le_2eme", "")
        self.rooms.append(escalier_vers_le_2eme)
        terrasse_1 = Room("terrasse_1","")     
        self.rooms.append(terrasse_1)  

        # Niveau 4
        terrasse_2 = Room("terrasse_2","")
        self.rooms.append(terrasse_2)
        restaurant = Room("restaurant","")
        self.rooms.append(restaurant)
        bar = Room("bar","")
        self.rooms.append(bar)
        cuisine = Room("cuisine","")
        self.rooms.append(cuisine)

        # Niveau 5
        salle_secréte = Room("salle_secréte","")
        self.rooms.append(salle_secréte)

        # Create exits for rooms

        hall_0.exits = {"N" : hall_1 , "E" : salle_du_garde, "S" : None, "O" : boulangerie}
        boulangerie.exits = {"N" : None, "E" : hall_0, "S" : None, "O" : None}
        salle_du_garde.exits = {"N" : None, "E" : None, "S" : local_technique, "O" :hall_0}
        local_technique.exits = {"N" : salle_du_garde, "E" : None, "S" : None, "O" : None}

        escalier_vers_le_1er.exits = {"N" : hall_1, "E" : None, "S" : hall_0, "O" : None}
        hall_1.exits = {"N" : pays_3, "E" : pays_1, "S" : escalier_vers_le_1er, "O" : pays_2}
        pays_1.exits = {"N" :None ,"E" : None, "S" : None, "O" : hall_1}
        pays_2.exits = {"N" :None ,"E" : hall_1, "S" : None, "O" : None}
        pays_3.exits = {"N" :None ,"E" : None, "S" : hall_1, "O" : None}

        escalier_vers_le_2eme.exits = {"N" :None ,"E" : terrasse_1, "S" : None, "O" : pays_3}
        terrasse_1.exits = {"N" :None ,"E" : None, "S" : None, "O" : escalier_vers_le_2eme}

        terrasse_2.exits = {"N" :None ,"E" : None, "S" : terrasse_1, "O" : restaurant}
        restaurant.exits = {"N" :cuisine ,"E" : terrasse_2, "S" : None, "O" : bar}
        bar.exits = {"N" :None ,"E" : restaurant, "S" : None, "O" : None}
        cuisine.exits = {"N" :None ,"E" : None, "S" : restaurant, "O" : None}
        salle_secréte.exits = {"N" :None ,"E" : None, "S" : cuisine, "O" : None}

        #ON DÉFINIT ICI la salle de départ du joueur
        self.start_room = hall_0
        #inventaire 
        #niveau 1
        eclair = Item("eclair", "un délicieux éclair au chocolat",0.12)
        tournevis = Item("tournevis", "un tournevis utile", 0.01 )
        boulangerie.inventaire.append(eclair)
        local_technique.inventaire.append(tournevis)
        #niveau 2
        drapeau_sénégal = Item("drapeau_sénégal","Trois bandes verticales vert, jaune, rouge avec une étoile verte au centre",0.06)
        drapeau_tunisie = Item("drapeau_tunisie","Fond rouge avec un disque blanc, croissant et étoile rouges",0.06)
        drapeau_égypte = Item("drapeau_égypte","Trois bandes horizontales rouge, blanc, noir avec un aigle doré au centre",0.06)

        drapeau_Turquie = Item("drapeau_Turquie","Fond rouge avec un croissant et une étoile blancs",0.06)
        drapeau_Japon = Item("drapeau_Japon","Fond blanc avec un cercle rouge au centre",0.06)
        drapeau_Indonésie = Item("drapeau_Indonésie","Deux bandes horizontales rouge (haut) et blanche (bas)",0.06)

        drapeau_Mexique = Item("drapeau_Mexique","Trois bandes verticales vert, blanc, rouge avec un aigle sur un cactus au centre",0.06)
        drapeau_USA = Item("drapeau_USA","Bandes horizontales rouges et blanches avec un canton bleu étoilé",0.06)
        drapeau_Canada = Item("drapeau_Canada","Deux bandes rouges et une bande blanche centrale avec une feuille d’érable rouge",0.06)


        pays_1.inventaire.append(drapeau_sénégal)
        pays_1.inventaire.append(drapeau_tunisie)
        pays_1.inventaire.append(drapeau_égypte)

        pays_2.inventaire.append(drapeau_Turquie)
        pays_2.inventaire.append(drapeau_Japon)
        pays_2.inventaire.append(drapeau_Indonésie)

        pays_3.inventaire.append(drapeau_Mexique)
        pays_3.inventaire.append(drapeau_USA)
        pays_3.inventaire.append(drapeau_Canada)

    #ajout pnj 
    #niveau 1
        garde = Character("garde","Un garde sévère qui surveille les lieux",salle_du_garde, ["ici je suis le garde que voulez-vous"])
        salle_du_garde.characters[garde.name] = garde

        boulanger = Character("boulanger", "Un boulanger souriant couvert de farine",boulangerie,["Bonjour !", "Essayez mon éclair au chocolat !"])
        boulangerie.characters[boulanger.name]= boulanger
    #niveau 2
        Mr_Red =Character("Mr_Red", "Un homme mystérie ",pays_1,["Énigme ! Je cherche un drapeau :", "3 bandes verticales vert, jaune, rouge","une étoile verte au centre","Donne-moi ce drapeau"])
        pays_1.characters[Mr_Red.name]= Mr_Red

        Mr_White =Character("Mr_White", "Un homme mystérie ",pays_2,["Énigme : je suis un pays à cheval sur deux continents","Mon drapeau n'a que 2 couleurs","On y voit un symbole lié au calendrier lunaire… avec un astre","Si tu connais la réponse, donne-moi le bon drapeau."])
        pays_2.characters[Mr_White.name]= Mr_White

        Mr_Blue =Character("Mr_Blue", "Un homme mystérie ",pays_3,["Énigme : mon pays a un emblème au centre.","On y voit un rapace posé sur un cactus.","Le drapeau a 3 bandes verticales.","Donne-moi ce drapeau si tu veux avancer."])
        pays_3.characters[Mr_Blue.name]= Mr_Blue

        self.pnj_france = Character("PNG","Un personnage mystérieux apparu après vos 3 victoires",self.hall_1,["PNG : 'Tu as résolu les 3 énigmes... dernière question !'","PNG : 'Je suis en Europe.'","PNG : 'Ma capitale est surnommée la ville lumière.'","PNG : 'Tape le nom de mon pays dans le terminal pour gagner.'"])

        pnj_couleurs = Character("Couleurs","Un animateur qui bloque l'accès au niveau 4",terrasse_1,["Couleurs : 'Jeu des couleurs !'","Couleurs : 'Je te donne un ordre de 5 couleurs parmi : R B J V O.'","Couleurs : 'Pour jouer, tape : colors R B J V O (exemple)'","Couleurs : 'Je te dirai combien de couleurs sont bien placées.'"])
        terrasse_1.characters[pnj_couleurs.name] = pnj_couleurs
#########################deplacement#######################################################
        #self.characters.append(boulanger)
        #self.characters.append(garde)
#########################################################################
        
    def setup_quests(self):
        # 1. Créer la quête
        self.quete_garde = Quest("Le Garde Gourmand", "Donnez un éclair au garde.", ["donner avec eclair"], "Code: 8")
        
        # 2. L'ajouter au joueur
        self.player.quest_manager.add_quest(self.quete_garde)
        
        # 3. L'ACTIVER (Très important !)
        self.player.quest_manager.activate_quest("Le Garde Gourmand")

        # Faire pareil pour le boulanger
        self.quete_boulanger = Quest("Réparation Urgente", "Donnez le tournevis.", ["donner avec tournevis"], "Accès éclair")
        self.player.quest_manager.add_quest(self.quete_boulanger)
        self.player.quest_manager.activate_quest("Réparation Urgente")

        #Quete de Mr_red
        self.quete_mr_red = Quest("Énigme de Mr_Red","Résoudre l’énigme de Mr_Red en lui donnant le bon drapeau.",["donner avec drapeau_sénégal"],"")
        self.player.quest_manager.add_quest(self.quete_mr_red)
        self.player.quest_manager.activate_quest("Énigme de Mr_Red")
        #Quete Mr WHite 
        self.quete_mr_white = Quest("Énigme de Mr_White","Résoudre l’énigme de Mr_White en lui donnant le bon drapeau.",["donner avec drapeau_Turquie"],"")
        self.player.quest_manager.add_quest(self.quete_mr_white)
        self.player.quest_manager.activate_quest("Énigme de Mr_White")
        #Quete Mr Blue 
        self.quete_mr_blue = Quest("Énigme de Mr_Blue","Résoudre l’énigme de Mr_Blue en lui donnant le bon drapeau.",["donner avec drapeau_Mexique"],"")
        self.player.quest_manager.add_quest(self.quete_mr_blue)
        self.player.quest_manager.activate_quest("Énigme de Mr_Blue")
    

    def play(self):
        self.setup()
        self.print_welcome()
        self.setup_quests()

        while not self.finished:
        # Le joueur entre une commande
            command = input("> ")
            self.process_command(command)
        #nouveau
            #if "eclair" in self.player.inventaire and self.player.current_room.name == "salle_du_garde":
                #self.eclair_donne_au_garde = True
                #self.player.inventaire.remove("eclair")
                #print("\nVous avez donné l'éclair au garde.\n")
        #Test de victoire
            """if self.win():
                self.finished = True
                break

        #  Test de défaite
            if self.loose():
                self.finished = True
                break"""

    # Process the command entered by the player
    def process_command(self, command_string) -> None:
        # ✅ Réponse finale (pas une commande)
        if self.france_riddle_unlocked and command_string.strip().lower() == "france":
            print("\n🏆 BRAVO ! Tu as trouvé la bonne réponse : FRANCE")
            print("🎉 Tu remportes le CROISSANT D’OR !")
            self.finished = True
            return
        if command_string.strip() == "":
           return

        list_of_words = command_string.split(" ")
        command_word = list_of_words[0]

        if command_word not in self.commands.keys(): 
            print(f"\nCommande '{command_word}' non reconnue. Entrez 'help' pour voir la liste des commandes disponibles.\n") 
        else: 
            command = self.commands[command_word] 
            command.action(self, list_of_words, command.number_of_parameters)
        ################deplacement####################
        #for character in self.characters:
            #moved = character.move()
            #if moved:
               # print(f"{character.name} se déplace dans une autre pièce.")
        #####################################################################""
    def try_spawn_france_pnj(self):
        if self.final_pnj_spawned:
            return

        if self.mr_red_enigme_resolue and self.mr_white_enigme_resolue and self.mr_blue_enigme_resolue:
            self.hall_1.characters[self.pnj_france.name] = self.pnj_france
            self.final_pnj_spawned = True
            self.france_riddle_unlocked = True
            print("\n✨ Un nouveau personnage apparaît dans le hall du 1er étage (hall_1) !")
    def win(self):
        if self.eclair_donne_au_garde:
            print("\n🎉 VICTOIRE !")
            print("Le garde a dégusté son éclair et vous laisse explorer le reste de la Tour.")
            print("Il vous glisse un papier dans la main : 'Vous en aurez besoin pour le sommet... C'est le chiffre 8.'")
            #print("\n--- CODE FINAL : _ 8 _ _ ---") # Indice visuel pour le joueur
            return True
        return False

    def loose(self):
        """
    Défaite : temps écoulé
        """
        if self.player.move_count >= TIME_LIMIT:
            print("\n⏰ TEMPS ÉCOULÉ")
            print("Tu n'as pas réparé la machine à temps.")
            return True
        return False
   

    # Print the welcome message
    def print_welcome(self):
        print("==========================================")
        print("        BIENVENUE A LA TOUR EIFFEL")
        print("==========================================")

        # ASCII ART (inchangé)
        effeil = r""" 
                                        
                                ⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣤⣤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣤⢞⣍⣂⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⡷⠶⠋⠹⡞⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣃⡤⣶⠛⣷⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢨⠃⣏⠀⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⠋⠀⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⡀⠀⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⣇⠀⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⣿⠀⢹⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⣿⠀⢸⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⢰⢻⠀⠸⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⣸⢸⠀⠀⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠇⣿⠸⡄⠀⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⠀⡇⠀⡇⠀⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡟⠀⡇⠀⣧⠀⢻⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⢰⡇⠀⣿⠀⠘⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⡇⣸⡀⠀⢽⣦⣀⣩⣉⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⡿⢇⣿⣶⠶⠿⠟⠋⠉⠙⢷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣶⠾⠛⠋⠉⣀⣠⣴⠖⠀⠰⣦⡀⠈⠳⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⡿⠐⢲⠉⠉⠀⣿⠀⠀⠀⢹⣿⣷⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠃⠀⡞⠀⠀⠀⣿⠀⠀⠀⠈⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⡇⠀⢰⡇⠀⠀⠀⢸⡄⠀⠀⠀⢸⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡿⠁⢀⣾⠁⠀⠀⠀⠘⣿⠀⠀⠀⠈⢿⣿⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⠇⠀⣼⡇⠀⠀⠀⠀⠀⣿⣦⠀⠀⠀⠘⠿⠿⠿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⡟⠀⣸⣿⠁⠀⠀⠀⠀⣀⣛⣹⣤⣤⣤⣶⠶⢦⣄⠈⠳⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⢿⣁⣘⣭⣵⣴⡶⠶⠶⠿⠛⠛⠉⠉⠉⠀⠀⠀⠈⣍⠳⠶⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡿⠟⠛⠛⠋⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣆⠀⠀⠀⠀⠀⢹⣷⣦⣌⠙⠲⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀⢠⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡀⢹⡀⠀⠀⠀⠀⠸⣿⣿⣿⣿⣶⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣤⠛⠀⠀⢠⡿⠤⢤⡤⠄⠀⠀⠘⠛⠿⢯⣍⠀⠈⣷⡄⠀⠀⠀⠀⠹⣿⣿⣿⣿⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⢀⡾⠃⠀⢀⣴⠋⠀⣚⣡⠤⠔⠒⠚⠛⠒⠦⢤⣤⣀⡀⠸⣿⣆⠀⠀⠀⠀⠹⣿⣿⣿⣿⣿⣦⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⢠⡞⠁⠀⣠⢟⣭⠖⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠿⣶⣄⡈⠧⠀⠀⠀⠀⠙⣿⣿⠀⠉⠙⢷⡄⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⢀⣴⠏⠀⠀⣀⡿⣫⣤⠶⠶⢶⣦⡀⠀⠀⠀⠀⠀⠀⠀⣀⡤⠶⠚⠻⣿⣦⡀⠀⠀⠀⠀⠙⣿⣆⠀⠀⠀⢻⣆⡀⠀⠀⠀⠀
        ⠀⠀⠀⠀⢀⡾⠃⠀⢀⣴⠏⠞⠉⠁⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀⣠⠞⠉⠀⠀⠀⠀⠈⢻⣿⣆⠀⠀⠀⠀⠈⣿⣦⠀⠀⠀⠙⢷⡄⠀⠀⠀
        ⠀⠀⠀⣰⡿⠃⠀⢠⣾⠇⠀⠀⠀⠀⠀⠀⢀⣿⡇⠀⠀⠀⠀⣼⠟⠀⠀⠀⠀⠀⠀⠀⠀⠹⣿⣧⠀⠀⠀⠀⠈⢿⣧⡀⠀⠀⠈⢿⣆⠀⠀
        ⠀⢀⣼⡟⠀⠀⢠⣿⠇⠀⠀⠀⠀⠀⠀⠀⢸⣿⣅⣀⡀⠀⢠⣿⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣿⣧⠀⠀⠀⠀⠈⢻⣧⡄⠀⠀⠀⢻⣧⠀
        ⢠⣿⣏⡀⠀⠀⣾⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣦⠀⠀⠀⠀⢀⣿⣷⣄⠀⠒⠚⠛⠓
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⠛⠀⠀⠀⠒⠛⠉⠉⠛⠂⠀⠀⠀⠀
                ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠲⡆⠄⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀
        """
        print(effeil)
        
        # Création du joueur
        self.player = Player(input("\nQuel est ton nom ? : "))
        print(f"\nBienvenue {self.player.nom} !")
        print()
        print("Entrez 'help' si vous avez besoin d'aide.")
        print("==========================================")
        print("Tu te trouves maintenant au pied de la Tour Eiffel.")
        print("Un mystérieux trésor serait caché au sommet")
        print("de la Tour Eiffel... Mais seuls les plus")
        print("courageux peuvent atteindre le 4ème étage.")
        print("Ton objectif : monter jusqu'au 4ème étage ")
        print("et trouver le croissant d'or.")
        print("Chaque étage de la Tour Eiffel cache un défi unique.")
        print("Réussis les épreuves, collecte tous les chiffres")
        print("Et Va Decrocher le CROISSANT D’OR !")
        print("==========================================")
        input("\nAppuie sur [ENTRER] pour entrer dans le hall du rez-de-chaussée...")
        print()

        self.player.current_room = self.start_room

        print(self.player.current_room.get_long_description())



def main():
    Game().play()
    

if __name__ == "__main__":
    main()