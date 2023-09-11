from django.urls import path
from .views import HomeView, MoveDetailView, CreateGameView, PlayGameView, ContinueGameView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('home', HomeView.as_view(), name='home'),
    path('home/last=<int:last>', HomeView.as_view(), name='home'),
    path('see_moves/gameplay=<int:game_id>/last=<int:last>', MoveDetailView.as_view(), name='see_moves'),
    path('create_game/<option>', CreateGameView.as_view(), name='create_game'),
    path('play_game', PlayGameView.as_view(), name='play_game'),
    path('continue_game/gameplay=<int:game_id>', ContinueGameView.as_view(), name='continue_game'),
]