from django.test import TestCase, Client
from django.urls import reverse
from werewolf import views


class TestViews(TestCase):

    def setUp(self):
        """
        setup data for test cases.
        client simulates a client and the rest are reverse objects that are used for client requests
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

    def test_get_players_add(self):
        """
        post three players and assert that they are added, the template and the status code
        """
        views.players_li_names = []
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
        if no players were added, assert an http response code 204
        """
        views.players_li_names = []

        response = self.client.post(self.getPlayers)
        self.assertEqual(response.status_code, 204)

    def test_assignRoles(self):
        """
        assign there players to three roles, assert the objects, status and template
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
        """assert the stats code, and the template"""
        response = self.client.get(self.day1)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'day1.html')

    def test_seer_alive_choice_no_redirection(self):
        """
        seer choose a player to discover, assert the object, status code 200, and template
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
        if seer doesn't exist, assert redirection code 302 and URL
        """
        response = self.client.get(self.seer)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/sleepwalk')

    def test_seer1(self):
        """
        assert the role of discovered player by seer, status code 200 and template used
        """
        views.seer_person = views.Villager('player')
        response = self.client.get(self.seer1)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'seer1.html')
        self.assertEqual(response.context['selected'], 'Villager')

    def test_sleepwalking_all_yes(self):
        """
        assert redirection, status code, and a random player is dead if all chose yes
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
        assert redirection to reveal, random sleepwalker, and status code
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
        assert redirection to night, None sleepwalker, and status code
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
        assert chosen player object, redirection, and redirection status code
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
        assert rendering of revealed player, status code, and template
        """
        views.seer_person = str(views.Villager('abdulkader'))
        views.sleepwalk_person = views.Villager('vassili')
        response = self.client.get(self.sleepwalking2)

        self.assertEqual(response.context['villager'], views.sleepwalk_person)
        self.assertEqual(response.context['role'], 'Villager')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sleepwalking2.html')

    def test_night_redirection_to_win(self):
        player1 = views.Werewolf('Abdulkader')
        player2 = views.Villager('Filip')
        views.players_li_obj = [player1, player2]
        response = self.client.get(self.night)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/werewolves_win')

    def test_night_werewolf_kill(self):
        werewolf1 = views.Werewolf('Abdulkader')
        villager1 = views.Villager('Filip')
        villager2 = views.Villager('Vassili')
        views.players_li_obj += [werewolf1, villager1, villager2]
        response = self.client.post(self.night, {
            'vote': villager1
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'night_template.html')
        self.assertEqual(villager1.is_dead, True)
        self.assertEqual(villager2.is_dead, False)

    def test_witch_redirection_to_day(self):
        views.players_li_obj = [views.Villager('filip'),
                                views.Villager('vassili'),
                                views.Werewolf('abdulkader'),
                                views.Witch('afif', is_dead=True)]
        response = self.client.get(self.witch)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/day')

    def test_white(self):
        response = self.client.get(self.white)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'white_werewolf.html')

    def test_day(self):
        response = self.client.get(self.day)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'day_template.html')
