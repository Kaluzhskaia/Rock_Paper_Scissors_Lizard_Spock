from django.test import TestCase, Client
from django.urls import reverse
from gameplay.models import Game, Move


class ModelTestCase(TestCase):
    def setUp(self):
        self.game = Game.objects.create(player1_name='Alice', player2_name='Bob', with_computer=False)
        self.move = Move.objects.create(game=self.game, player1_choice='Rock', player2_choice='Paper', winner='Bob')

    def test_game_creation(self):
        self.assertEqual(self.game.player1_name, 'Alice')
        self.assertEqual(self.game.player2_name, 'Bob')
        self.assertEqual(self.game.with_computer, False)

    def test_move_creation(self):
        self.assertEqual(self.move.game, self.game)
        self.assertEqual(self.move.player1_choice, 'Rock')
        self.assertEqual(self.move.player2_choice, 'Paper')
        self.assertEqual(self.move.winner, 'Bob')


class ViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.game = Game.objects.create(player1_name='Alice', player2_name='Bob', with_computer=False)
        self.move = Move.objects.create(game=self.game, player1_choice='Rock', player2_choice='Paper', winner='Bob')

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Alice')
        self.assertContains(response, 'Bob')

    def test_move_detail_view(self):
        response = self.client.get(reverse('see_moves', args=[self.game.id, 15]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Rock')
        self.assertContains(response, 'Paper')
        self.assertContains(response, 'Bob')

    def test_create_game_view_with_friends(self):
        response = self.client.get(reverse('create_game', args=["friends"]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Player 1')
        self.assertContains(response, 'Player 2')

    def test_create_game_view_with_computer(self):
        response = self.client.get(reverse('create_game', args=["computer"]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['with_computer'])

    def test_play_game_view(self):
        session = self.client.session
        session['game'] = self.game.id
        session.save()
        response = self.client.get(reverse('play_game'), HTTP_REFERER=reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Alice')
        self.assertContains(response, 'Bob')

