from django.shortcuts import render, redirect

# Abdul write your classes here.

# ---- CLASSES ---- #

class Player:
    def __init__(self, name, is_dead, is_lover):
        self.is_dead = is_dead
        self.name = name
        self.is_lover = is_lover

class Villager(Player):
    def __init__(self, name, is_dead = False, is_lover = False, sleepwalk = False):
        super().__init__(name = name, is_dead = is_dead, is_lover = is_lover)
        self.sleepwalk = sleepwalk

class Werewolf(Player):
    def __init__(self, name, is_dead = False, is_lover = False):
        super().__init__(name = name, is_dead = is_dead, is_lover = is_lover)

class WhiteWerewolf(Player):
    def __init__(self, name, is_dead = False, is_lover = False):
        super().__init__(name = name, is_dead = is_dead, is_lover = is_lover)

class Seer(Player):
    def __init__(self, name, is_dead = False, is_lover = False):
        super().__init__(name = name, is_dead = is_dead, is_lover = is_lover)

class Hunter(Player):
    def __init__(self, name, is_dead = False, is_lover = False):
        super().__init__(name = name, is_dead = is_dead, is_lover = is_lover)

class Witch(Player):
    def __init__(self, name, is_dead = False, is_lover = False):
        super().__init__(name = name, is_dead = is_dead, is_lover = is_lover)

# ---- ---- #

players_li_names = ['Player 1', 'Player 2', 'Player 3', 'Player 4', 'Player 5']
players_li_obj = []


# ---- RETURN TEMPLATES ----#

# get_players.html
def getPlayers(req):
    global players_li_names
    if req.method == 'POST':

        if str(req.POST['Pname']) == '':
            print('cannot make a Player with no name')
            pass

        elif (len(players_li_names) >= 20):
            print('cannot add more players')
            pass

        else:

            if req.POST['Pname'] in players_li_names:
                print('cannot add player with same name in the list')
                pass

            else:

                players_li_names.append(str(req.POST['Pname']))



    context_dict = \
        {
            'players_li_names' : players_li_names
        }

    return render(req, 'get_players.html', context_dict)

# roles.html
def assignRoles(req):

    if req.method == 'POST':
        print(req.POST)
        for name in players_li_names:
            if req.POST[name] == 'Villager':
                players_li_obj.append(Villager(name))
            elif req.POST[name] == 'Werewolf':
                players_li_obj.append(Werewolf(name))
            elif req.POST[name] == 'WhiteWerewolf':
                players_li_obj.append(WhiteWerewolf(name))
            elif req.POST[name] == 'Seer':
                players_li_obj.append(Seer(name))
            elif req.POST[name] == 'Hunter':
                players_li_obj.append(Hunter(name))
            elif req.POST[name] == 'Witch':
                players_li_obj.append(Witch(name))

    context_dict = \
        {
            'players_li' : players_li_names
        }

    return render(req, 'roles.html', context_dict)

# day1.html
def day1(req):
    return render(req, 'day1.html')

# night_template
def night(req):

    werewolves = []

    for person in players_li_obj:
        werewolf = isinstance(person, Werewolf)
        if werewolf == True:
            werewolves.append(person)

    rest_li = list(filter(lambda x: x not in werewolves, players_li_obj))

    counter = 0
    humans_win = False

    for werewolf in werewolves:
        if werewolf.is_dead == True:
            counter+=1
    if len(werewolves) - counter == 0:
        humans_win = True

    if req.method == 'POST':
        print(req.POST['vote'])
        for element in players_li_obj:
            if str(element) == str(req.POST['vote']):
                element.is_dead = True



    context_dict = \
        {
            'werewolves' : werewolves,
            'rest' : rest_li,
            'humans_won' : humans_win
        }

    return render(req, 'night_template.html', context_dict)

def day(req):

    alive = []

    for element in players_li_obj:
        if element.is_dead:
            pass
        else:
            alive.append(element)


    if req.method == 'POST':
        print(req.POST['vote'])
        for element in players_li_obj:
            if str(element) == str(req.POST['vote']):
                element.is_dead = True



    context_dict = \
        {
            'all' : players_li_obj,
            'alive' : alive
        }

    return render(req, 'day_template.html', context_dict)

