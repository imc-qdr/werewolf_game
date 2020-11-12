from django.shortcuts import render, redirect
import re as regular
import random


# ---- CLASSES ---- #

class Player:
    """
    main superclass that other roles inherit
    """

    def __init__(self, name, is_dead, is_lover):
        self.is_dead = is_dead
        self.name = name
        self.is_lover = is_lover


# classes for roles are below
class Villager(Player):
    def __init__(self, name, is_dead=False, is_lover=False, sleepwalk=False):
        super().__init__(name=name, is_dead=is_dead, is_lover=is_lover)
        self.sleepwalk = sleepwalk


class Werewolf(Player):
    def __init__(self, name, is_dead=False, is_lover=False):
        super().__init__(name=name, is_dead=is_dead, is_lover=is_lover)


class WhiteWerewolf(Player):
    def __init__(self, name, is_dead=False, is_lover=False):
        super().__init__(name=name, is_dead=is_dead, is_lover=is_lover)


class Seer(Player):
    def __init__(self, name, is_dead=False, is_lover=False):
        super().__init__(name=name, is_dead=is_dead, is_lover=is_lover)


class Hunter(Player):
    def __init__(self, name, is_dead=False, is_lover=False):
        super().__init__(name=name, is_dead=is_dead, is_lover=is_lover)


class Witch(Player):
    def __init__(self, name, is_dead=False, is_lover=False, healing_potion=True, poison_potion=True, is_killed=False):
        super().__init__(name=name, is_dead=is_dead, is_lover=is_lover)
        self.poison_potion = poison_potion
        self.healing_potion = healing_potion
        self.is_killed = is_killed


# ---- METHODS ---- #

def killPlayer(PlayerObj):
    PlayerObj.is_dead = True
    if PlayerObj.is_lover:
        amor_li[0].is_dead = True
        amor_li[1].is_dead = True


# ---- VARIABLES ---- #

players_li_names = ['Werewolf', 'Villager1', 'Villager2', 'Villager3', 'Villager4', 'Sophie', 'Werewolf2', 'White']
players_li_obj = []
seer_person = None        # The person the seer chooses to see or the person who the sleepwalking villager chooses to see
person_to_heal = None     # The person the witch heals
person_to_kill = None     # The person the witch kills
hunter_killed_at = None   # The time when the hunter was killed, during the night or after voting
hunter_died = False       # The hunter died is declared so it doesn't loop it during the day
white_werewolf_token = 0  # The token that decides whether to render witch(1) or white werewolf(2)
sleepwalk_person = None   # The person that chooses which players role they're going to see
amor_li = []
isReadyToStart = False



# ---- RETURN TEMPLATES ----#

# index.html
def index(req):
    return render(req, 'index.html')


# renders get_players.html template
def getPlayers(req):
    """
    gets players name and appends them to players_li_names and renders them back
    in the template
    """
    global players_li_names
    if req.method == 'POST':

        if 'p_to_remove' in req.POST:
            print('got a player to remove ', req.POST['p_to_remove'])
            players_li_names.remove(str(req.POST['p_to_remove']))

        if str(req.POST['Pname']).strip() == '':
            print('cannot make a Player with no name')
            pass

        elif len(players_li_names) >= 20:
            print('cannot add more players')
            pass

        else:
            if req.POST['Pname'] not in players_li_names:
                players_li_names.append(str(req.POST['Pname']))

    context_dict = \
        {
            'players_li_names': players_li_names
        }

    return render(req, 'get_players.html', context_dict)


# renders roles.html template
def assignRoles(req):
    """
    renders the names in player_li_names to the template and assign
    them roles based on conditionals.
    """
    global amor_li
    global isReadyToStart

    if req.method == 'POST':
        print(req.POST)
        isReadyToStart = True
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

        if 'amor' in req.POST:
            if req.POST['amor']:
                amors = req.POST.getlist('amor')
                for amor in amors:
                    for person in players_li_obj:
                        if amor == person.name:
                            person.is_lover = True
                            amor_li.append(person)

        if 'csrfmiddlewaretoken' in req.POST:
            return redirect('day1')

    context_dict = \
        {
            'players_li': players_li_names,
            'isReadyToStart': isReadyToStart
        }

    return render(req, 'roles.html', context_dict)


# renders day1.html template
def day1(req):
    global players_li_names
    players_li_names.clear()
    return render(req, 'day1.html')


# renders seer.html template
def seer(req):
    """
    if the seer is not dead, renders the template to allow the seer to discover the role
    if the seer is dead or not assigned, redirect to sleepwalking phase
    """
    global seer_person
    rest = []

    if req.method == 'POST':
        seer_person = req.POST['vote']

    for person in players_li_obj:
        if isinstance(person, Seer):
            pass
        elif person.is_dead:
            pass
        else:
            rest.append(person)

    for person in players_li_obj:
        if isinstance(person, Seer) and not person.is_dead:
            context_dict = \
                {
                    'seer': person,
                    'rest': rest,
                }
            return render(req, 'seer.html', context_dict)

    return redirect('sleepwalking')


# seer1.html
def seer1(req):
    """
    renders the template to show the identity of the player
    chosen by the seer
    """
    role = str(seer_person)
    back = regular.findall(r"\w+", role)

    context_dict = \
        {
            'selected': back[2]
        }
    return render(req, 'seer1.html', context_dict)


# sleepwalking.html
def sleepwalking(req):
    """
    renders sleep walking template to allow players to decide whether
    they will go sleep walking. if all decided to sleep walk, kill a random player
    if one only decide, give him an ability to be seer for one round.
    """
    global position_in_list, sleepwalk_person, players_li_names
    alive = []
    for person in players_li_obj:
        if isinstance(person, Villager) and not person.is_dead:
            alive.append(person)

    if req.method == 'POST':
        answers = req.POST.getlist('Decide')
        if len(set(answers)) == 1 and answers[0] == 'No':  # if all answers are the same 'No'
            return redirect('night_template')
        if len(answers) == 1 and answers[0] == 'Yes':
            return redirect('night_template')
        else:
            if len(set(answers)) == 1 and answers[0] == 'Yes':  # if all answers are the same 'Yes'
                selected_person = random.choice(alive)
                if selected_person.is_lover:
                    players_li_names.append(amor_li[0])
                    players_li_names.append(amor_li[1])
                else:
                    players_li_names.append(selected_person)
                for person in players_li_obj:
                    if str(selected_person) == str(person):
                        killPlayer(person)
                        return redirect('night_template')
        counter = 0
        for element in answers:
            if str(element) == 'Yes':
                counter += 1
                position_in_list = answers.index('Yes')

        if counter == 1:
            sleepwalk_person = alive[int(position_in_list)]
            return redirect('sleepwalking1')
        else:
            return redirect('night_template')

    context_dict = \
        {
            'alive': alive
        }

    return render(req, 'sleepwalking.html', context_dict)


# sleepwalking1.html
def sleepwalking1(req):
    """
    renders the template for the sleepwalking player
    to choose a player to reveal his identity.
    """
    global seer_person, sleepwalk_person
    rest = []

    for person in players_li_obj:
        if not person.is_dead:
            rest.append(person)

    rest.remove(sleepwalk_person)

    if req.method == 'POST':
        seer_person = req.POST['vote']
        return redirect('sleepwalking2')

    context_dict = \
        {
            'person': sleepwalk_person,
            'alive': rest
        }

    return render(req, 'sleepwalking1.html', context_dict)


# sleepwalking2.html
def sleepwalking2(req):
    """
    renders the template the show the identity of the player
    that was chosen by the sleepwalking player
    """
    global sleepwalk_person, seer_person

    role = str(seer_person)
    back = regular.findall(r"\w+", role)

    context_dict = \
        {
            'villager': sleepwalk_person,
            'role': back[2]
        }

    return render(req, 'sleepwalking2.html', context_dict)


# night_template.html
def night(req):
    """
    renders the night template and checks for winning conditions.
    if werewolves are equal or more than villagers, redirect to winning werewolves
    static page. otherwise allow the werewolves to vote on the kill.
    if hunter was killed it redirects to hunter template
    """
    global white_werewolf_token, players_li_names, person
    werewolves = []
    alive_werewolves = []
    white_werewolf = None

    for person in players_li_obj:
        werewolf = isinstance(person, Werewolf)
        white = isinstance(person, WhiteWerewolf)
        if werewolf or white:
            werewolves.append(person)
        if (werewolf and not person.is_dead) or (white and not person.is_dead):
            alive_werewolves.append(person)
        if white:
            white_werewolf = person


    rest_li = list(filter(lambda x: x not in werewolves, players_li_obj))
    for person in rest_li:
        if person.is_dead:
            rest_li.remove(person)

    if len(alive_werewolves) >= len(rest_li):
        return redirect('werewolves_win')

    if req.method == 'POST':
        for element in players_li_obj:
            if str(element) == str(req.POST['vote']):
                if isinstance(element, Witch):
                    element.is_killed = True
                else:
                    killPlayer(element)
                if element.is_lover:
                    players_li_names.append(amor_li[0])
                    players_li_names.append(amor_li[1])
                else:
                    players_li_names.append(element)
        if white_werewolf is None or white_werewolf.is_dead:
            print('ayy')
            pass
        else:
            white_werewolf_token += 1
            if white_werewolf_token == 3:
                white_werewolf_token = 1
            print(white_werewolf_token)

    context_dict = \
        {
            'werewolves': werewolves,
            'rest': rest_li,
            'token': white_werewolf_token
        }

    return render(req, 'night_template.html', context_dict)


# witch.html
def witch(req):
    """
    if witch is dead or unassigned, redirect to day template
    otherwise the witch choose a player to heal or kill.
    if hunter was killed, it redirects to hunter template.
    it checks for winning conditions
    """
    global person_to_heal, person_to_kill, witch, players_li_names, players_li_obj
    rest = []

    for person in players_li_obj:
        if person.is_dead == False:
            rest.append(person)

    if req.method == 'POST':
        word = str(req.POST)

        if 'kill' not in word:
            person_to_heal = req.POST['healing']
            witch.healing_potion = False
            for person in players_li_obj:
                if str(person) == person_to_heal:
                    person.is_dead = False
                    person_to_heal = None

        else:
            person_to_kill = req.POST['kill']
            witch.poison_potion = False
            for person in players_li_obj:
                if str(person) == person_to_kill:
                    killPlayer(person)
                    person_to_kill = None


    for person in players_li_obj:
        if isinstance(person, Witch) and not person.is_dead and (person.healing_potion or person.poison_potion):
            witch = person
            if witch.is_killed == True:
                witch.is_dead = True


            context_dict = \
                {
                    'witch': person,
                    'rest': rest,
                    'all': players_li_names,
                }
            return render(req, 'witch.html', context_dict)


    return redirect('day_template')


# day_template.html
def day(req):
    """
    renders the day template and allow them to vote.
    checks for winning condition of humans and werewolves and redirects to the
    static pages.
    if hunter was killed, it redirects to the hunter template
    """
    global hunter_killed_at, hunter_died, players_li_names
    players_li_names.clear()
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
            white = isinstance(element, WhiteWerewolf)
            if werewolf or white:
                werewolves_left_li.append(element)
            if str(element) == str(req.POST['vote']):
                killPlayer(element)
                if isinstance(element, Hunter):  # If the villagers decide to kill the hunter
                    hunter_killed_at = 'day'
                    return redirect('hunter')
        for werewolf in werewolves_left_li:
            if werewolf.is_dead:
                werewolves_left_li.remove(werewolf)
        if werewolves_left_li == []:
            return redirect('humans_win')

    for person in players_li_obj:
        if isinstance(person, Werewolf) or isinstance(person, WhiteWerewolf):
            werewolves.append(person)
        if isinstance(person, Hunter) and person.is_dead:  # If hunter is dead before the morning starts
            hunter_killed_at = 'night'
            if hunter_died:
                pass
            else:
                return redirect('hunter')

    alive_no_werewolves = list(filter(lambda x: x not in werewolves, alive))

    for werewolf in werewolves:
        if werewolf.is_dead:
            counter += 1

    if counter == len(werewolves):
        return redirect('humans_win')
    elif len(werewolves) - counter >= len(alive_no_werewolves):
        return redirect('werewolves_win')

    context_dict = \
        {
            'all': players_li_obj,
            'alive': alive
        }

    return render(req, 'day_template.html', context_dict)


# hunter.html
def hunter(req):
    """
    renders the hunter template to allow the hunter to kill a player
    """
    global person_to_kill, hunter_died, hunter_killed_at
    alive = []

    for element in players_li_obj:
        if element.is_dead:
            pass
        else:
            alive.append(element)

    if req.method == 'POST':
        person_to_kill = req.POST['vote']
        for person in alive:
            if str(person) == person_to_kill:
                killPlayer(person)
                person_to_kill = None
                hunter_died = True

    context_dict = \
        {
            'alive': alive,
            'killed': hunter_killed_at
        }

    return render(req, 'hunter.html', context_dict)


# white_werewolf.html
def whiteWerewolf(req):
    """
    renders white werewolf template and allow him to kill a werewolf.
    if the white werewolf is the only werewolf, redirects to witch template
    """
    global person_to_kill

    werewolves = []
    for person in players_li_obj:
        if isinstance(person, WhiteWerewolf) and person.is_dead:
           return redirect('witch')
        if isinstance(person, Werewolf) and not person.is_dead:
            werewolves.append(person)

    if werewolves == []:
        return redirect('witch')

    if req.method == 'POST':
        person_to_kill = str(req.POST['vote'])
        for person in players_li_obj:
            if person_to_kill == str(person):
                killPlayer(person)
                if person.is_lover:
                    players_li_names.append(amor_li[0])
                    players_li_names.append(amor_li[1])
                else:
                    players_li_names.append(person)
                person_to_kill = None

    print(werewolves)

    context_dict = \
        {
            'werewolves': werewolves
        }

    return render(req, 'white_werewolf.html', context_dict)


# humans_win.html
def humans_win(req):
    return render(req, 'humans_win.html')


# werewolves_win
def werewolves_win(req):
    return render(req, 'werewolves_win.html')
