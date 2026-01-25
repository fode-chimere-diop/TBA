# 🗼 Projet Tour Eiffel — Text Based Adventure (TBA)

## 🌟Présentation du Jeu🌟

Ce projet est un **jeu d’aventure textuel en Python** (Text-Based Adventure).
Le joueur explore la **Tour Eiffel**, étage par étage, résout des énigmes,
interagit avec des personnages (PNJ), collecte des objets et accomplit des quêtes
dans l'objectif d'atteindre le sommet et décrocher le **Croissant d’Or**.

Le jeu repose sur une architecture **orientée objet** et propose plusieurs
mécaniques de gameplay : inventaire, quêtes, mini-jeux, conditions de victoire
et de défaite.


# ♥️Guide utilisateur♥️

## Installation et lancement

### Prérequis

- Python 3.10 ou supérieur
- Aucun module externe requis (hors `tkinter` pour l’interface graphique)

### Lancer le jeu (mode terminal)
```bash 
python game.py
```
## 🕹️ Principe du jeu 

### Objectif
Vous incarnez un visiteur de la Tour Eiffel à la recherche d’un trésor légendaire.
Chaque étage de la tour correspond à un niveau avec ses propres défis :

-Niveau 1 : réparer la machine de la boulangerie et satisfaire le garde

-Niveau 2 : résoudre des énigmes de drapeaux avec des ambassadeurs

-Niveau 3 : mini-jeu de couleurs

-Niveau 4 : protocole du sommet (bar, cuisine, restaurant)

-Niveau 5 : coffre final avec code historique

### ⚜️Conditions de victoire

-Résoudre toutes les énigmes

-Compléter les quêtes principales

-Trouver le code historique et ouvrir le coffre final

### 💀 Conditions de défaite

-Dépasser le nombre de déplacements autorisés dans certains niveaux

-Faire trop d’erreurs dans certaines énigmes

### Contenue
-Maps:
![(<Map du jeux  (1).png>)])

Nombre de lieu: 15

-Png: 10

-Item:15

### Commandes disponibles

-help : Affiche la liste des commandes

-go <N/E/S/O/U> : Se déplacer

-look : Observer la pièce

-take <objet> : Prendre un objet

-drop <objet> : Déposer un objet

-inventory / check : Afficher l’inventaire

-talk <personnage> : Parler à un PNJ

-give <objet><personnage> : Donner un objet

-quests : Afficher les quêtes

-quest <titre> : Détails d’une quête

-rewards : Voir les récompenses

-colors R B J V O : Mini-jeu des couleurs

-unlock <code> : Ouvrir le coffre final

-quit : Quitter le jeu

# Guide de l'utilisateur 

### Structuration

Il y a pour le moment 8 modules contenant chacun une classe.
Le projet est structuré en plusieurs modules Python, chacun correspondant
à une **classe principale** ayant un rôle bien défini dans le jeu.

- `game.py` / **Game**  
  Gère le moteur principal du jeu : initialisation des salles, création
  des objets et personnages, gestion des commandes, progression du joueur
  et conditions de victoire/défaite.

- `room.py` / **Room**  
  Représente un lieu de la Tour Eiffel.  
  Une salle possède une description, des sorties vers d’autres salles,
  un inventaire d’objets et des personnages présents.

- `player.py` / **Player**  
  Représente le joueur.  
  Gère la position actuelle, l’inventaire, l’historique des déplacements,
  le compteur de mouvements et l’interaction avec le système de quêtes.

- `item.py` / **Item**  
  Représente un objet du jeu.  
  Chaque objet possède un nom, une description et un poids, et peut être
  ramassé, donné ou utilisé par le joueur.

- `character.py` / **Character**  
  Représente les personnages non joueurs (PNJ).  
  Un personnage possède un nom, une description et des dialogues qui
  évoluent au fil des interactions avec le joueur.

- `command.py` / **Command**  
  Définit une commande du jeu (mot-clé, aide, nombre de paramètres et action associée).

- `actions.py` / **Actions**  
  Implémente les actions déclenchées par les commandes du joueur :
  déplacements, interactions avec les objets, dialogues avec les PNJ,
  mini-jeux et progression des quêtes.

- `quest.py` / **Quest** et **QuestManager**  
  Gère le système de quêtes : activation, suivi des objectifs,
  validation des actions et attribution des récompenses.
**************
- Interface graphique (Tkinter)

    Le jeu propose également une **interface graphique développée avec Tkinter**,
    intégrée dans le module `game.py`.

    Cette interface comprend :
        - une zone d’affichage visuel représentant la salle actuelle ;
        - une console textuelle affichant les messages du jeu ;
        - des boutons de commandes (déplacements, aide, quitter) ;
        - un champ de saisie permettant d’entrer des commandes textuelles.

    L’interface graphique communique directement avec la classe `Game` et
    réutilise l’intégralité de la logique du jeu, garantissant ainsi une
    séparation claire entre **logique métier** et **affichage**.
*****************
### Schéma du scénario 

![(<Schema jeux 2.png>)]

### diagramme de classes
classDiagram
        Game --|> Player
        Game --|> Room
        Game --|> Command
        Command --|> Actions
        Game --|> Item
        Game --|> character
        Game --|> Quest
        Game --|> QuestManager
        Game --|> _StdoutRedirector
        Game --|> GameGUI
        Game : Finished -> bool
        Game : rooms -> list
        Game : commands -> dict
        Game : player -> Player 
        Game : start.room -> Room  
        Game : machine_reparee -> bool
        Game : eclair_donne_au_garde -> bool
        Game : wrong_flags -> int
        Game : mr_red_enigme_donnee -> bool 
        Game : mr_white_enigme_donnee -> bool
        Game : mr_blue_enigme_donnee -> bool
        Game : mr_red_enigme_resolue -> bool 
        Game : mr_white_enigme_resolue -> bool 
        Game : mr_blue_enigme_resolue -> bool 
        Game : acces_niveau_4 -> bool
        Game : couleurs_code -> list[str] 
        Game : hall_1 -> Room  
        Game : unlock_attelots ->init
        Game : __init__() 
        Game : setup()
        Game : play()
        Game : process_command(command_string ) -> None
        Game : print_welcome()
        Game : try_spawn_france_pnj() -> None
        Game : reset_niveau_2() -> None
        Game : win() -> bool
        Game : loose() -> bool
        Game : setup_quests()
        class Player {
          nom -> str
          current_room -> Room
          inventaire -> list
          history -> list
          nombre -> bool   
          nord -> int
          eclair_choco -> bool
          tournevis -> bool
          max_weight -> float
          move_count -> int 
          quest_maager -> QuestManager
          reward -> list
          __init__(nom )
          move(direction) -> bool
          current_weight() -> float 
          get_history() -> str
          check() -> str
          show_rewards() -> None
          get_inventory() ->
          add_reward(reward) -> None
          show_rewards() -> None       
        }
        class Room {
            name -> str
            description -> str
            exits -> dict
            inventaire -> list
            characters -> dict
            image -> str
            __init__(name, description, image)
            get_exit(direction) -> Room | None
            set_exit(direction , room) -> None 
            get_exit_string() -> str
            get_long_description() -> str  
            get_inventory() -> str
        }
        class Command {
          command_word -> str
          help_string -> str
          action -> function 
          number_of_parameters -> int
           __init__(command_word ,help_string ,action,number_of_parameters)
           __str__() -> str
        }
        class Actions{
            go(game ,list_of_words ,number_of_parameters) -> bool
            quit(game, list_of_words, number_of_parameters) -> bool
            help(game, list_of_words, number_of_parameters) -> bool
            history(game, list_of_words, n) -> bool
            back(game, list_of_words, n) -> bool
            look(game, list_of_words, n) -> bool 
            take(game, list_of_words, n) -> bool 
            inventory(game, list_of_words, n) -> bool 
            drop(game, list_of_words, n) -> bool 
            check(game, list_of_words, n) -> bool  
            talk(game, list_of_words, n) -> bool
            give(game, list_of_words, n) -> bool
            quests(game, list_of_words, n) -> bool
            quest(game, list_of_words, n) -> bool
            activate(game, list_of_words, n) -> bool 
            rewards(game, list_of_words, n) -> bool
            colors(game, list_of_words, n) -> bool
            unlock(game, words, n) -> bool
        }
       class Item {
            nom -> str
            description -> str
            poids -> float

            __init__(nom , description, poids)
            __str__() -> str
        }
        class Quest {
            title : str
            description : str
            objectives : list[str]
            completed_objectives : list[str]
            is_completed : bool
            is_active : bool
            reward : str

            __init__(title, description, objectives=None, reward=None)
            activate() : None
            complete_objective(objective, player=None) : bool
            complete_quest(player=None) : None
            get_status() : str
            get_details(current_counts=None) : str
            check_room_objective(room_name, player=None) : bool
            check_action_objective(action, target=None, player=None) : bool
            check_counter_objective(counter_name, current_count, player=None) : bool
          }

        class QuestManager {
            quests : list[Quest]
            active_quests : list[Quest]
            player : Player

            __init__(player=None)
            add_quest(quest) : None
            activate_quest(quest_title) : bool
            complete_objective(objective_text) : bool
            check_room_objectives(room_name) : None
            check_action_objectives(action, target, item=None) : None
            check_counter_objectives(counter_name, current_count) : None
            show_quests() : None
            show_quest_details(quest_title, current_counts=None) : None
            get_quest_by_title(title) : Quest
            check_quest_completion() : None
          }
        class GameGUI {
            game : Game
            canvas : Canvas
            text_output : Text
            entry : Entry

            __init__()
            _build_layout() : None
            _update_room_image() : None
            _send_command(command) : None
            _on_enter(event) : None
            _on_close() : None
          } 

        class _StdoutRedirector {
            text_widget : Text
            __init__(text_widget)
            write(msg) : None
            flush() : None
           }
        class character {
          name : str
          description : str
          current_room : Room
          msgs : list[str]
          _msgs_queue : list[str]
          _msgs_done : list[str]

          __init__(name, description, current_room, msgs)
          __str__() : str
          get_msg() : None
          talk(player) : None
          }
![!(<Text Adventure Architecture-2026-01-25-160415.png>)]

# Amélioration Possible 

-Amélioration de l'interface graphique: *Amélioration des commandes sur l'interface graphique
                                          *Faire une animation pour le jeux 

-Moder notre jeux pour qu'il soit plus dur à certain moment

-Génération aléatoire: Le code du coffre (1887) et l'ordre des couleurs du Mastermind (R B J V O) sont fixes. On pourrait utiliser le module random pour générer un nouveau code à chaque partie, rendant le jeu rejouable.

-Gestion des erreurs de frappe : Si le joueur écrit "colros" au lieu de "colors", le jeu ne comprend pas. Utiliser une bibliothèque pour tolérer les petites fautes d'orthographe rendrait l'interface plus fluide

-Inventaire Visuel : Remplacer la liste textuelle par des icônes cliquables