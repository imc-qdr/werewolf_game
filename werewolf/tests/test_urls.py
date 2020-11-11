from django.test import SimpleTestCase
from django.urls import reverse, resolve
import werewolf.views


class TestUrls(SimpleTestCase):
    """
    asserts the correct mapping
    between views functions and URLs in urls.py file
    for all urls and view functions
    """
    def test_players_url(self):
        url = reverse('getPlayers')
        self.assertEqual(werewolf.views.getPlayers, resolve(url).func)

    def test_roles_url(self):
        url = reverse('roles')
        self.assertEqual(werewolf.views.assignRoles, resolve(url).func)

    def test_first_day_url(self):
        url = reverse('day1')
        self.assertEqual(werewolf.views.day1, resolve(url).func)

    def test_seer_url(self):
        url = reverse('seer')
        self.assertEqual(werewolf.views.seer, resolve(url).func)

    def test_seer1_url(self):
        url = reverse('seer1')
        self.assertEqual(werewolf.views.seer1, resolve(url).func)

    def test_sleepwalk_url(self):
        url = reverse('sleepwalking')
        self.assertEqual(werewolf.views.sleepwalking, resolve(url).func)

    def test_sleepwalk1_url(self):
        url = reverse('sleepwalking1')
        self.assertEqual(werewolf.views.sleepwalking1, resolve(url).func)

    def test_sleepwalking2_url(self):
        url = reverse('sleepwalking2')
        self.assertEqual(werewolf.views.sleepwalking2, resolve(url).func)

    def test_night_url(self):
        url = reverse('night_template')
        self.assertEqual(werewolf.views.night, resolve(url).func)

    def test_witch_url(self):
        url = reverse('witch')
        self.assertEqual(werewolf.views.witch, resolve(url).func)

    def test_white_url(self):
        url = reverse('whiteWerewolf')
        self.assertEqual(werewolf.views.whiteWerewolf, resolve(url).func)

    def test_day_url(self):
        url = reverse('day_template')
        self.assertEqual(werewolf.views.day, resolve(url).func)

    def test_human_win_url(self):
        url = reverse('humans_win')
        self.assertEqual(werewolf.views.humans_win, resolve(url).func)

    def test_werewolves_win_url(self):
        url = reverse('werewolves_win')
        self.assertEqual(werewolf.views.werewolves_win, resolve(url).func)

    def test_hunter_url(self):
        url = reverse('hunter')
        self.assertEqual(werewolf.views.hunter, resolve(url).func)



