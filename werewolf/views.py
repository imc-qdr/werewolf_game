from django.shortcuts import render, redirect
import re as regular

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
    def __init__(self, name, is_dead = False, is_lover = False, healing_potion = True, poison_potion = True):
        super().__init__(name = name, is_dead = is_dead, is_lover = is_lover)
        self.poison_potion = poison_potion
        self.healing_potion = healing_potion


# ---- VARIABLES ---- #

players_li_names = ['Vasilli', 'Abdul', 'Sophie', 'Teo', 'Dio', 'Jotaro']
players_li_obj = []
seer_person = None
person_to_heal = None
person_to_kill = None


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

# seer.html
def seer(req):

    global seer_person
    rest = []

    if req.method == 'POST':
        seer_person = req.POST['vote']

    for person in players_li_obj:
        if isinstance(person, Seer) == True:
            pass
        elif person.is_dead == True:
            pass
        else:
            rest.append(person)


    for person in players_li_obj:
        if isinstance(person, Seer) == True and person.is_dead != True:
            context_dict =  \
            {
                'seer' : person,
                'rest' : rest,
            }
            return render(req, 'seer.html', context_dict)

    return redirect('night_template')

#seer1.html
def seer1(req):

    role = str(seer_person)
    back = regular.findall(r"\w+", role)

    context_dict = \
        {
            'selected' : back[2]
        }
    return render(req, 'seer1.html', context_dict)

# night_template.html
def night(req):

    werewolves = []

    for person in players_li_obj:
        werewolf = isinstance(person, Werewolf)
        if werewolf == True:
            werewolves.append(person)

#    counter = 0
#    for person in werewolves:
#        if person.is_dead == True:
#            counter += 1
#    if counter == len(werewolves):
#        return redirect('humans_win')

    rest_li = list(filter(lambda x: x not in werewolves, players_li_obj))
    for person in rest_li:
        if person.is_dead == True:
            rest_li.remove(person)

    if req.method == 'POST':
        for element in players_li_obj:
            if str(element) == str(req.POST['vote']):
                element.is_dead = True

    context_dict = \
        {
            'werewolves' : werewolves,
            'rest' : rest_li,
        }

    return render(req, 'night_template.html', context_dict)

# witch.html
def witch(req):

    global person_to_heal, person_to_kill, witch
    rest = []

    if req.method == 'POST':
        word = str(req.POST)

        if 'kill' not in word:
            person_to_heal = req.POST['healing']
            witch.healing_potion = False
            for person in rest:
                if str(person) == person_to_heal:
                    person.is_dead = False
                    person_to_heal = None

        else:
            person_to_kill = req.POST['kill']
            witch.poison_potion = False
            for person in players_li_obj:
                if str(person) == person_to_kill:
                    person.is_dead = True
                    person_to_kill = None

    for person in players_li_obj:
        if isinstance(person, Witch) == True:
            pass
        elif person.is_dead == True:
            pass
        else:
            rest.append(person)

    for person in players_li_obj:
        if isinstance(person, Witch) == True and person.is_dead != True and (person.healing_potion == True or person.poison_potion == True):
            witch = person

            context_dict = \
                {
                    'witch': person,
                    'rest' : rest,
                    'all' : players_li_obj,
                }
            return render(req, 'witch.html', context_dict)


    return redirect('day_template')

#day_template.html
def day(req):

    werewolves = []
    werewolves_left_li = []
    alive = []
    counter = 0

    for element in players_li_obj:
        if element.is_dead:
            pass
        else:
            alive.append(element)

    if req.method == 'POST':
        for element in players_li_obj:
            werewolf = isinstance(element, Werewolf)
            if werewolf == True:
                werewolves_left_li.append(element)
            if str(element) == str(req.POST['vote']):
                element.is_dead = True
        for werewolf in werewolves_left_li:
            if werewolf.is_dead == True:
                werewolves_left_li.remove(werewolf)
        if werewolves_left_li == []:
            return redirect('humans_win')

    for person in players_li_obj:
        if isinstance(person, Werewolf):
            werewolves.append(person)

    for werewolf in werewolves:
        if werewolf.is_dead == True:
            counter += 1

    if counter == len(werewolves):
        return redirect('humans_win')


    context_dict = \
        {
            'all' : players_li_obj,
            'alive' : alive
        }

    return render(req, 'day_template.html', context_dict)

#humans_win.html
def humans_win(req):
    return render(req, 'humans_win.html')
