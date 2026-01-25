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
TIME_LIMIT = 20    # AJOUTÉ (temps max) # LE JEU 1
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

        self.couleurs_attempts = 20  # Le joueur a 10 essais pour le Mastermind LE NIVEAU 3
        self.wrong_flags = 0   # nombre de mauvaises tentatives sur les drapeaux (niveau 2) LE NIVEAU 2 

        # --- Mini-jeu couleurs (accès niveau 4) ---
        self.couleurs_code = ["R", "B", "J", "V", "O"]  # tu peux changer / randomiser
        self.couleurs_jeu_actif = False
        self.acces_niveau_4 = False

        self.unlock_attempts = 5  # nombre de tentatives restantes pour le coffre LE COFFRE FINAL
    
    # Setup the game
    def setup(self):

        # Setup commands
        help = Command("help", " : afficher cette aide", Actions.help, 0)
        self.commands["help"] = help

        quit = Command("quit", " : quitter le jeu", Actions.quit, 0)
        self.commands["quit"] = quit

        go = Command("go", " <direction> : se déplacer dans une direction cardinale (N, E, S, O, U)", Actions.go, 1)
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
        # Commande de déverrouillage du coffre final    
        unlock_cmd = Command("unlock", " <code_historique> : tenter d'ouvrir le coffre final", Actions.unlock, 1)
        self.commands["unlock"] = unlock_cmd
        
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
        hall_1 = Room("hall_1", "dans le Hall du premiére étage")
        self.rooms.append(hall_1)
        self.hall_1 = hall_1  # pour usage ultérieur
        pays_1 = Room("pays_1", "dans la salle de Mr red")
        self.rooms.append(pays_1)
        pays_2 = Room("pays_2", "dans la salle de Mr white")
        self.rooms.append(pays_2)
        pays_3 = Room("pays_3", "dans la salle de Mr blue")
        self.rooms.append(pays_3)

        # Niveau 3
        hall_2 = Room("hall_2", "dans le hall du deuxiéme étage")
        self.rooms.append(hall_2)
        self.hall_2 = hall_2
        terrasse_1 = Room("terrasse_1","dans la premiére terrasse")     
        self.rooms.append(terrasse_1)  

        # Niveau 4
        terrasse_2 = Room("terrasse_2", "une terrasse venteuse. Une inscription sur une table attire votre regard : 'Le Barman a soif de froid, le Chef a soif d'élixir.'")
        self.rooms.append(terrasse_2)
        # Dans game.py
        restaurant = Room("restaurant", "un restaurant luxueux. Une table numérotée '4' est dressée au centre, elle semble attendre qu'on y dépose le plat signature du Chef.")
        self.rooms.append(restaurant)
        bar = Room("bar","dans le bar")
        self.rooms.append(bar)
        cuisine = Room("cuisine","dans la cuisine")
        self.rooms.append(cuisine)


        # Niveau 5
        # Niveau 5
        salle_secréte = Room("salle_secréte", "le sommet de la Tour. Le vent siffle entre les poutres. Au centre, un coffre massif en fer forgé semble attendre un code historique pour libérer son trésor.")
        self.rooms.append(salle_secréte)

        # Create exits for rooms

        hall_0.exits = {"N" : None, "E" : salle_du_garde, "S" : None, "O" : boulangerie, "U" : None}
        boulangerie.exits = {"N" : None, "E" : hall_0, "S" : None, "O" : None, "U" : None}
        salle_du_garde.exits = {"N" : None, "E" : None, "S" : local_technique, "O" :hall_0, "U" : None}
        local_technique.exits = {"N" : salle_du_garde, "E" : None, "S" : None, "O" : None, "U" : None}

        hall_1.exits = {"N" : pays_3, "E" : pays_1, "S" : None, "O" : pays_2, "U" : None}
        pays_1.exits = {"N" :None ,"E" : None, "S" : None, "O" : hall_1, "U" : None}
        pays_2.exits = {"N" :None ,"E" : hall_1, "S" : None, "O" : None, "U" : None}
        pays_3.exits = {"N" :None ,"E" : None, "S" : hall_1, "O" : None, "U" : None}

        hall_2.exits= {"N" :None ,"E" : terrasse_1, "S" : None, "O" : None, "U" : None}
        terrasse_1.exits = {"N" :None ,"E" : None, "S" : None, "O" : hall_2, "U" : None}

        terrasse_2.exits = {"N" :None ,"E" : None, "S" : None , "O" : restaurant, "U" : None}
        restaurant.exits = {"N" :cuisine ,"E" : terrasse_2, "S" : None, "O" : bar, "U" : None}
        bar.exits = {"N" :None ,"E" : restaurant, "S" : None, "O" : None, "U" : None}
        cuisine.exits = {"N" :None ,"E" : None, "S" : restaurant, "O" : None, "U" : None}
        salle_secréte.exits = {"N" :None ,"E" : None, "S" : None, "O" : None, "U" : None}

        #ON DÉFINIT ICI la salle de départ du joueur 
        self.start_room = salle_secréte      
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
        #niveau 4
        glaçons = Item("glaçons", "Des cubes de glace qui fondent lentement.", 0.2)
        bouteille = Item("bouteille", "Une bouteille d'élixir rare.", 0.5)
        plat = Item("plat", "Le plat signature du chef, prêt à être servi.", 0.8)
        indice_final = Item("note", "Un papier griffonné : 'Glace pour le Barman -> Élixir pour le Chef -> Secret au Restaurant'", 0.01)
        terrasse_2.inventaire.append(indice_final)
        # 3. Placement initial (Les glaçons sont déjà en cuisine)
        cuisine.inventaire.append(glaçons)
    #ajout pnj 
    #niveau 1
        # --- Dans game.py, méthode setup ---

        garde = Character("garde", "Un garde imposant dont l'estomac gargouille bruyamment.", salle_du_garde, ["Mes yeux ne quittent pas cette porte... mais mon esprit est à la boulangerie.","L'ordre règne ici. Enfin, il règnerait mieux avec un peu de sucre dans le sang.","Vous voulez monter ? Trouvez-moi quelque chose de chocolaté pour rompre l'ennui."])
        salle_du_garde.characters[garde.name] = garde
        boulanger = Character("boulanger", "Un pâtissier en détresse, couvert de farine.", boulangerie,["Sacrébleu ! Sans ma machine, la Tour Eiffel va manquer de douceurs !", "Entendez-vous ce grincement ? C'est le bruit d'une catastrophe pâtissière.","Un simple tour de vis et l'odeur du chocolat envahira à nouveau ce hall !"])
        boulangerie.characters[boulanger.name] = boulanger
    #niveau 2
        Mr_Red =Character("Mr_Red", "Un homme mystérie ",pays_1,["Énigme ! Je cherche un drapeau :", "3 bandes verticales vert, jaune, rouge","une étoile verte au centre","Donne-moi ce drapeau"])
        pays_1.characters[Mr_Red.name]= Mr_Red

        Mr_White =Character("Mr_White", "Un homme mystérie ",pays_2,["Énigme : je suis un pays à cheval sur deux continents","Mon drapeau n'a que 2 couleurs","On y voit un symbole lié au calendrier lunaire… avec un astre","Si tu connais la réponse, donne-moi le bon drapeau."])
        pays_2.characters[Mr_White.name]= Mr_White

        Mr_Blue =Character("Mr_Blue", "Un homme mystérie ",pays_3,["Énigme : mon pays a un emblème au centre.","On y voit un rapace posé sur un cactus.","Le drapeau a 3 bandes verticales.","Donne-moi ce drapeau si tu veux avancer."])
        pays_3.characters[Mr_Blue.name]= Mr_Blue

        # On remplace "PNG" par "L'Historien" (ou le nom que tu as choisi)
        self.pnj_france = Character("L'Historien", "Un personnage érudit apparu après vos 3 victoires", self.hall_1, [
        "L'Historien : 'Tu as résolu les 3 énigmes... dernière question !'",
        "L'Historien : 'Je suis en Europe.'",
        "L'Historien : 'Ma capitale est surnommée la ville lumière.'",
        "L'Historien : 'Tape le nom de mon pays dans le terminal pour gagner.'"
        ])

        pnj_couleurs = Character("Couleurs","Un animateur qui bloque l'accès au niveau 4",terrasse_1,["Couleurs : 'Jeu des couleurs !'","Couleurs : 'Je te donne un ordre de 5 couleurs parmi : R B J V O.'","Couleurs : 'Pour jouer, tape : colors R B J V O (exemple)'","Couleurs : 'Je te dirai combien de couleurs sont bien placées.'"])
        terrasse_1.characters[pnj_couleurs.name] = pnj_couleurs
#########################deplacement#######################################################
        #self.characters.append(boulanger)
        #self.characters.append(garde)
#########################################################################
       #niveau 4
       # 2. Création des PNJ avec leurs dialogues
        barman = Character("barman", "Un mixologue qui attend ses ingrédients.", bar, ["Bienvenue au Bar ! Pour obtenir ma bouteille de collection, il me faut des glaçons frais.","Rapportez-moi de la glace de la cuisine, et on discute."])
        bar.characters[barman.name] = barman
        chef = Character("chef", "Un cuisinier étoilé très exigeant.", cuisine, ["Vite ! J'ai besoin de cet élixir du bar pour finir mon plat !","Apportez-moi la bouteille du barman, et je vous donnerai le secret du restaurant."])
        cuisine.characters[chef.name] = chef
        
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
        #Quete Mr WHite 
        self.quete_mr_white = Quest("Énigme de Mr_White","Résoudre l’énigme de Mr_White en lui donnant le bon drapeau.",["donner avec drapeau_Turquie"],"")
        self.player.quest_manager.add_quest(self.quete_mr_white)
        #Quete Mr Blue 
        self.quete_mr_blue = Quest("Énigme de Mr_Blue","Résoudre l’énigme de Mr_Blue en lui donnant le bon drapeau.",["donner avec drapeau_Mexique"],"")
        self.player.quest_manager.add_quest(self.quete_mr_blue)
        

        self.escape_4 = Quest("Le Protocole du Sommet", "Récupérez les glaçons en cuisine, échangez-les au bar, puis apportez le plat au restaurant.", ["poser plat restaurant"], "Chiffre : 4")
        self.player.quest_manager.add_quest(self.escape_4)

        self.quete_finale = Quest("Le Secret du Sommet", "Trouvez la combinaison historique du coffre pour gagner.", ["unlock 1887"], "Croissant d'Or")
        self.player.quest_manager.add_quest(self.quete_finale)
        # Elle s'activera automatiquement quand le joueur atteindra le 5ème étage
        self.player.quest_manager.activate_quest("Énigme de Mr_Red")
        self.player.quest_manager.activate_quest("Énigme de Mr_White")
        self.player.quest_manager.activate_quest("Énigme de Mr_Blue")
        self.player.quest_manager.activate_quest("Le Protocole du Sommet")
    

    def play(self):
        self.setup()
        self.print_welcome()
        self.setup_quests()

        while not self.finished:
        # Le joueur entre une commande
            command = input("> ")
            self.process_command(command)
        #✅ On active enfin le test de défaite
            if self.loose():
                self.finished = True
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
            print("🎉 Tu remportes le CHIFFRE 8!")
            self.hall_1.exits["U"] = self.hall_2
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
    def reset_niveau_2(self):
        # 1) Message
        print("\n💀 PERDU (niveau 2) : 3 mauvais drapeaux !")
        print("➡️ Retour au hall_1. Le niveau 2 est réinitialisé.\n")

        # 2) Reset des flags / états niveau 2
        self.wrong_flags = 0
        self.mr_red_enigme_donnee = False
        self.mr_white_enigme_donnee = False
        self.mr_blue_enigme_donnee = False

        self.mr_red_enigme_resolue = False
        self.mr_white_enigme_resolue = False
        self.mr_blue_enigme_resolue = False

        # France PNJ reset
        self.final_pnj_spawned = False
        self.france_riddle_unlocked = False
        # si jamais PNG était apparu, on l'enlève de hall_1
        if self.hall_1 and "L'Historien" in self.hall_1.characters:
            del self.hall_1.characters["L'Historien"]

        # 3) Retirer tous les drapeaux de l’inventaire du joueur
        # (on remettra des nouveaux drapeaux dans les rooms)
        self.player.inventaire = [
            item for item in self.player.inventaire
            if not item.nom.lower().startswith("drapeau_")
        ]

        # 4) Réinjecter les drapeaux dans pays_1, pays_2, pays_3
        # (on recrée des Items neufs, c’est le plus simple)
        # On retrouve les rooms par leur name :
        pays_1 = next(r for r in self.rooms if r.name == "pays_1")
        pays_2 = next(r for r in self.rooms if r.name == "pays_2")
        pays_3 = next(r for r in self.rooms if r.name == "pays_3")

        # On vide les inventaires de drapeaux (sans toucher aux autres objets éventuels)
        pays_1.inventaire = [i for i in pays_1.inventaire if not i.nom.lower().startswith("drapeau_")]
        pays_2.inventaire = [i for i in pays_2.inventaire if not i.nom.lower().startswith("drapeau_")]
        pays_3.inventaire = [i for i in pays_3.inventaire if not i.nom.lower().startswith("drapeau_")]

        # On remet les drapeaux
        from item import Item  # si besoin (sinon déjà importé en haut de game.py)

        pays_1.inventaire += [
            Item("drapeau_sénégal","Trois bandes verticales vert, jaune, rouge avec une étoile verte au centre",0.06),
            Item("drapeau_tunisie","Fond rouge avec un disque blanc, croissant et étoile rouges",0.06),
            Item("drapeau_égypte","Trois bandes horizontales rouge, blanc, noir avec un aigle doré au centre",0.06),
        ]
        pays_2.inventaire += [
            Item("drapeau_Turquie","Fond rouge avec un croissant et une étoile blancs",0.06),
            Item("drapeau_Japon","Fond blanc avec un cercle rouge au centre",0.06),
            Item("drapeau_Indonésie","Deux bandes horizontales rouge (haut) et blanche (bas)",0.06),
        ]
        pays_3.inventaire += [
            Item("drapeau_Mexique","Trois bandes verticales vert, blanc, rouge avec un aigle sur un cactus au centre",0.06),
            Item("drapeau_USA","Bandes horizontales rouges et blanches avec un canton bleu étoilé",0.06),
            Item("drapeau_Canada","Deux bandes rouges et une bande blanche centrale avec une feuille d’érable rouge",0.06),
        ]

        # 5) Téléportation du joueur dans hall_1
        self.player.current_room = self.hall_1
        print(self.player.current_room.get_long_description())

    
    
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
        Gère la défaite par le temps (nombre de pas) uniquement pour les niveaux 1 et 4.
        """
        # 1. On définit les zones où le chrono est actif (Niveaux 1 et 4)
        niveau_1 = ["hall_0", "boulangerie", "local_technique", "salle_du_garde"]
        niveau_4 = ["terrasse_2", "bar", "cuisine", "restaurant"]
        
        current_room_name = self.player.current_room.name

        # 2. Test de défaite pour le Niveau 1
        if current_room_name in niveau_1:
            # Limite pour le niveau 1 (ex: 20 pas)
            if self.player.move_count >= 20:
                print("\n" + "!"*40)
                print("⏰ TEMPS ÉCOULÉ - NIVEAU 1")
                print("Le garde s'est endormi et la boulangerie a fermé.")
                print("Vous avez mis trop de temps à réparer la machine !")
                print("!"*40)
                return True

        # 3. Test de défaite pour le Niveau 4
        elif current_room_name in niveau_4:
            # Limite globale pour le niveau 4 (ex: 50 pas car c'est plus long)
            if self.player.move_count >= 20:
                print("\n" + "!"*40)
                print("⏰ TEMPS ÉCOULÉ - NIVEAU 4")
                print("Le service au restaurant est terminé.")
                print("Vous avez mis trop d'allers-retours pour le protocole !")
                print("!"*40)
                return True

        # Dans les autres niveaux (2, 3, 5), on ne perd pas par move_count
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