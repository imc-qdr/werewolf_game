from django.test import TestCase, Client
from django.urls import reverse
from werewolf import views


class TestViews(TestCase):

    def setUp(self):
        """
        setup data for test cases. the setup is called before each test case.
        the client simulates a client and the rest are reverse objects that are used for client requests.
        views variables sets up the environment for multiple tests.
        """
        self.client = Client()
        self.getPlayers = reverse('getPlayers')
        self.assignRoles = reverse('roles')
        self.day1 = reverse('day1')
        self.seer = reverse('seer')
        self.seer1 = reverse('seer1')
        self.sleepwalking = reverse('sleepwalking')
        self.sleepwalking1 = reverse('sleepwalking1')
        self.sleepwalking2 = reverse('sleepwalking2')
        self.night = reverse('night_template')
        self.witch = reverse('witch')
        self.white = reverse('whiteWerewolf')
        self.day = reverse('day_template')
        views.players_li_names = []
        views.players_li_obj = []
        views.sleepwalk_person = None

    def test_get_players_add(self):
        """
        post request: post three players and assert that they are added
        assert the used template and the status code 200
        """

        response = self.client.post(self.getPlayers, {
            'Pname': 'abdulkader',
        })
        self.client.post(self.getPlayers, {
            'Pname': 'vassili',
        })
        self.client.post(self.getPlayers, {
            'Pname': 'filip kasic',
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'get_players.html')

        self.assertEqual(views.players_li_names[2], 'filip kasic')
        self.assertEqual(views.players_li_names[1], 'vassili')
        self.assertEqual(views.players_li_names[0], 'abdulkader')

    def test_get_players_NO_PLAYERS(self):
        """
        if no players were added, assert an http response code Error 204
        """
        views.players_li_names = []

        response = self.client.post(self.getPlayers)
        self.assertEqual(response.status_code, 204)

    def test_assignRoles(self):
        """
        assign there players name to three role objects
        assert the objects in views, the status status code and template used
        """
        views.players_li_names = ['abdulkader', 'vassili', 'filip']
        response = self.client.post(self.assignRoles, {
            'abdulkader': 'Villager',
            'vassili': 'Werewolf',
            'filip': 'Seer'
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'roles.html')
        self.assertEqual(views.players_li_obj[0].name, 'abdulkader')
        self.assertIsInstance(views.players_li_obj[0], views.Villager)
        self.assertEqual(views.players_li_obj[1].name, 'vassili')
        self.assertIsInstance(views.players_li_obj[1], views.Werewolf)
        self.assertEqual(views.players_li_obj[2].name, 'filip')
        self.assertIsInstance(views.players_li_obj[2], views.Seer)

    def test_day1(self):
        """
        assert the stats code 200, and the template day1.html
        the template has no POST method
        """
        response = self.client.get(self.day1)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'day1.html')

    def test_seer_alive_choice_no_redirection(self):
        """
        seer player choose a player role to discover
        creates the role objects and the post request
        assert the value in views, status code 200, and template used
        """
        seer = views.Seer('filip')
        werewolf = views.Werewolf('abdulkader')
        views.players_li_obj += [seer, werewolf]
        response = self.client.post(self.seer, {
            'vote': werewolf
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'seer.html')
        self.assertEqual(views.seer_person, str(werewolf))

    def test_seer_dead_redirection(self):
        """
        if seer is dead, assert redirection code 302 and URL
        """
        seer = views.Seer('filip', is_dead=True)
        werewolf = views.Werewolf('abdulkader')
        villager = views.Villager('vassili')
        views.players_li_obj = [seer, werewolf, villager]
        response = self.client.get(self.seer)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/sleepwalk')

    def test_seer1(self):
        """
        assert the role of discovered player by seer as rendered inside the template
        status code 200 and template used
        """
        views.seer_person = views.Villager('player')
        response = self.client.get(self.seer1)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'seer1.html')
        self.assertEqual(response.context['selected'], 'Villager')

    def test_sleepwalking_all_yes(self):
        """
        creates objects and POST request.
        assert that a random player died, status code 200 and redirection to night URL
        """
        player1 = views.Villager('abdulkader')
        player2 = views.Villager('vassili')
        player3 = views.Villager('afif')
        views.players_li_obj = [player1, player2, player3]
        response = self.client.post(self.sleepwalking, {
            "Decide": [
                "Yes",
                "Yes",
                "Yes"
            ]
        })
        value = sum(1 for x in views.players_li_obj if not x.is_dead and isinstance(x, views.Villager))
        self.assertEqual(value, len(views.players_li_obj) - 1)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/night')

    def test_sleepwalking_one_yes(self):
        """
        creates roles objects and POST requests.
        assert sleepwalking villager in views, status code 302 and redirection URL
        """
        player1 = views.Villager('abdulkader')
        player2 = views.Villager('vassili')
        player3 = views.Villager('afif')
        self.assertIsNone(views.sleepwalk_person)
        views.players_li_obj = [player1, player2, player3]
        response = self.client.post(self.sleepwalking, {
            "Decide": [
                "No",
                "Yes",
                "No"
            ]
        })
        self.assertEqual(player2, views.sleepwalk_person)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/sleepwalk1')

    def test_sleepwalking_more_yes(self):
        """
        creates objects and POST request.
        assert redirection to night, sleepwalker is None, and status code 302 (redirection)
        """
        player1 = views.Villager('abdulkader')
        player2 = views.Villager('vassili')
        player3 = views.Villager('afif')
        views.players_li_obj = [player1, player2, player3]
        response = self.client.post(self.sleepwalking, {
            "Decide": [
                "Yes",
                "Yes",
                "No"
            ]
        })

        self.assertIsNone(views.sleepwalk_person)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/night')

    def test_sleepwalking1_choose_to_reveal(self):
        """
        creates objects and POST request.
        asserts the object of chosen player by sleepwalking player, redirection URL and status code
        """
        player1 = views.Villager("abdulkader")
        player2 = views.Villager("filip")
        player3 = views.Werewolf("vassili")
        views.sleepwalk_person = player2
        views.players_li_obj = [player1, player2, player3]
        response = self.client.post(self.sleepwalking1, {
            'vote': str(player3)
        })
        self.assertEqual(views.seer_person, str(player3))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/sleepwalk2')

    def test_sleepwalking2_get(self):
        """
        creates objects and POST requests
        assert rendering of revealed player in the template, status code 200, and template used
        """
        views.seer_person = str(views.Villager('abdulkader'))
        views.sleepwalk_person = views.Villager('vassili')
        response = self.client.get(self.sleepwalking2)

        self.assertEqual(response.context['villager'], views.sleepwalk_person)
        self.assertEqual(response.context['role'], 'Villager')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sleepwalking2.html')

    def test_night_redirection_to_win(self):
        """
        creates objects and get requests
        assert winning condition of werewolves and redirection to werewolves winning URL
        """
        player1 = views.Werewolf('Abdulkader')
        player2 = views.Villager('Filip')
        views.players_li_obj = [player1, player2]
        response = self.client.get(self.night)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/werewolves_win')

    def test_night_werewolf_kill(self):
        """
        creates roles objects and POST request.
        assert is_dead of player object chosen by werewolf
        """
        werewolf1 = views.Werewolf('Abdulkader')
        villager1 = views.Villager('Filip')
        villager2 = views.Villager('Vassili')
        views.players_li_obj = [werewolf1, villager1, villager2]
        response = self.client.post(self.night, {
            'vote': villager1
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'night_template.html')
        self.assertEqual(villager1.is_dead, True)
        self.assertEqual(villager2.is_dead, False)

    def test_witch_redirection_to_day(self):
        """
        assert redirection if witch is dead and redirection status code 302
        """
        views.players_li_obj = [views.Villager('filip'),
                                views.Villager('vassili'),
                                views.Werewolf('abdulkader'),
                                views.Witch('afif', is_dead=True)]
        response = self.client.get(self.witch)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/day')

    def test_witch_cure_and_kill(self):
        """
        creates roles objects and POST requests.
        assert is_dead for players objects chosen by the witch to heal or kill
        assert template used and status code 200
        """
        views.players_li_obj = [views.Werewolf('filip'),
                                views.Villager('vassili'),
                                views.Villager('player'),
                                views.Villager('player2', is_dead=True),
                                views.Villager('abdulkader'),
                                views.Witch('afif')]
        response = self.client.post(self.witch, {
            'healing': str(views.players_li_obj[3]),
        })
        self.client.post(self.witch, {
            'kill': str(views.players_li_obj[4])
        })

        self.assertEqual(response.status_code, 200)
        self.assertFalse(views.players_li_obj[3].is_dead)
        self.assertTrue(views.players_li_obj[4].is_dead)
        self.assertTemplateUsed(response, 'witch.html')

    def test_white_kill(self):
        """
        creates player roles objects and POST requests.
        assert is_dead for werewolf chosen by white werewolf
        """
        views.players_li_obj = [
            views.Villager('player1'),
            views.Villager('abdulkader'),
            views.Seer('vassili'),
            views.WhiteWerewolf('afif'),
            views.Werewolf('filip')
        ]
        response = self.client.post(self.white,{
            'vote': str(views.players_li_obj[-1])
        })
        self.assertTrue(views.players_li_obj[-1].is_dead)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'white_werewolf.html')

    def test_day_redirect_to_werewolves_win(self):
        """
        creates objects and get requests.
        assert winning condition of werewolves and redirection to URL and code status
        """
        werewolf1 = views.Werewolf('filip')
        werewolf2 = views.Werewolf('afif')
        villager1 = views.Villager('vassili')
        villager2 = views.Villager('abdulkader')
        views.players_li_obj = [werewolf1, werewolf2, villager1, villager2]
        response = self.client.get(self.day)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/werewolves_win')

    def test_day_redirect_to_humans_win(self):
        """
        creates objects and get requests.
        assert winning condition of humans and redirection to humans winning URL and code status
        """
        witch = views.Witch('filip')
        seer = views.Seer('afif')
        villager1 = views.Villager('abdulkader')
        villager2 = views.Villager('vassili')
        views.players_li_obj = [witch, seer, villager1, villager2]
        response = self.client.get(self.day)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/humans_win')
