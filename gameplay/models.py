from django.db import models


class Game(models.Model):
    """Model to store the state of the whole gameplay."""

    created_at = models.DateTimeField(auto_now_add=True)
    player1_name = models.CharField(max_length=30)
    player2_name = models.CharField(max_length=30)
    player1_score = models.PositiveIntegerField(default=0)
    player2_score = models.PositiveIntegerField(default=0)
    with_computer = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.player1_name} ({self.player1_score}) vs {self.player2_name} ({self.player2_score})"


CHOICES = [
    ('Rock', 'Rock'),
    ('Paper', 'Paper'),
    ('Scissors', 'Scissors'),
    ('Lizard', 'Lizard'),
    ('Spock', 'Spock'),
]


class Move(models.Model):
    """Model to store the state of each separate move players make."""

    created_at = models.DateTimeField(auto_now_add=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player1_choice = models.CharField(max_length=8, choices=CHOICES)
    player2_choice = models.CharField(max_length=8, choices=CHOICES)
    winner = models.CharField(max_length=30)

    def save(self, *args, **kwargs):
        is_new = not bool(self.pk)  # check if this is a new object
        super(Move, self).save(*args, **kwargs)  # call the "real" save() method.

        if is_new:
            if self.winner != "Tie":
                if self.winner == self.game.player1_name:
                    self.game.player1_score += 1
                else:
                    self.game.player2_score += 1
            self.game.save()
