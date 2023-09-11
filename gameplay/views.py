import random

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView

from gameplay.models import Game, Move


def permission_denied_view(request):
    return render(request, "errors/403.html", {})


def get_referer(request):
    """To prevent a user from opening game without continuing an existing game or creating a new one."""
    referer = request.META.get('HTTP_REFERER')
    if not referer:
        return None
    return referer


def get_winner(move1, move2, player1_name, player2_name):
    """Determines the winner of a round."""
    if move1 == move2:
        return "Tie"

    winning_combinations = {
        "Rock": ["Scissors", "Lizard"],
        "Scissors": ["Paper", "Lizard"],
        "Paper": ["Rock", "Spock"],
        "Lizard": ["Spock", "Paper"],
        "Spock": ["Rock", "Scissors"]
    }

    # Check if move1 beats move2
    if move2 in winning_combinations[move1]:
        return player1_name

    # Otherwise, player2 wins
    return player2_name


class HomeView(ListView):
    """Renders the home view that displays previous game results."""
    model = Game
    template_name = 'home.html'
    context_object_name = 'games'
    ordering = ['-id']


class MoveDetailView(ListView):
    """Renders the moves detail view for a particular game."""
    model = Move
    template_name = 'moves.html'
    context_object_name = 'moves'

    def get_queryset(self):
        game_id = self.kwargs['game_id']
        last = self.kwargs['last']
        return Move.objects.filter(game_id=game_id).order_by('-id')[:last]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['game'] = get_object_or_404(Game, id=self.kwargs['game_id'])
        return context


class CreateGameView(View):
    """Handles the creation of new games."""

    def get(self, request, option):
        # passing with_computer boolean variable to template to only show one player in this case
        with_computer = option == "computer"
        return render(request, 'input_names.html', context={'with_computer': with_computer})

    def post(self, request, option):
        name1 = request.POST.get('name1')
        with_computer = option == "computer"
        name2 = "Computer" if with_computer else request.POST.get('name2')
        game = Game(player1_name=name1, player2_name=name2, with_computer=with_computer)
        game.save()

        # clearing the session from previous games
        request.session.flush()
        request.session['game'] = game.pk
        return redirect("play_game")


class PlayGameView(View):
    """Handles the main game logic."""

    template_name = 'game.html'

    def dispatch(self, request, *args, **kwargs):
        """Prevents a user from opening game without continuing an existing game or creating a new one."""
        if not get_referer(request):
            return permission_denied_view(request)

        """Sets up common variables before handling GET or POST."""
        self.game = Game.objects.get(pk=request.session['game'])
        self.turn = self.game.player1_name
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, context={'game_description': str(self.game), 'turn': self.turn})

    def post(self, request, *args, **kwargs):
        round_completed = False
        if 'player1_move' in request.session or self.game.with_computer:
            move1 = request.session.get('player1_move') if not self.game.with_computer else request.POST.get('move')
            move2 = random.choice(
                ["Rock", "Paper", "Scissors", "Lizard", "Spock"]) if self.game.with_computer else request.POST.get(
                'move')

            messages.info(request, f"{self.game.player1_name}: {move1}  |  {self.game.player2_name}: {move2}")
            winner = get_winner(move1, move2, self.game.player1_name, self.game.player2_name)

            new_move = Move(game=self.game, player1_choice=move1, player2_choice=move2, winner=winner)
            new_move.save()

            messages.success(request, 'It is a tie!' if winner == "Tie" else f'{winner} wins!')
            round_completed = True

            if "player1_move" in request.session:
                del request.session["player1_move"]
        else:
            request.session['player1_move'] = request.POST.get('move')
            self.turn = self.game.player2_name

        return render(request, self.template_name, context={'round_completed': round_completed,
                                                            'game_description': str(self.game),
                                                            'turn': self.turn})


class ContinueGameView(View):
    """Handles continuing an existing game."""

    def get(self, request, game_id):
        request.session.flush()
        request.session['game'] = game_id
        return redirect("play_game")
