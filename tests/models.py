from django.db import models

from django_lexorank.fields import RankField
from django_lexorank.models import RankedModel


class Team(RankedModel):
    name = models.CharField(max_length=255)


class User(RankedModel):
    name = models.CharField(max_length=255)
    rank = RankField(insert_to_bottom=True)

    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="users")
    order_with_respect_to = "team"


class Board(RankedModel):
    name = models.CharField(max_length=255)


class Task(RankedModel):
    name = models.CharField(max_length=255)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="tasks")
    order_with_respect_to = "board"

    assigned_to = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="tasks"
    )


class CardStates(models.TextChoices):
    TODO = "TODO", "To do"
    DOING = "DOING", "Doing"
    DONE = "DONE", "Done"


class Card(RankedModel):
    """RankedModel grouped by a CharField (not a FK).

    Reproduces the configuration where ``order_with_respect_to`` points at a
    plain scalar field (e.g. TextChoices/state column) — verifies that the
    library doesn't blindly call ``.pk`` on the value.
    """

    name = models.CharField(max_length=255)
    state = models.CharField(
        max_length=16, choices=CardStates.choices, default=CardStates.TODO
    )
    order_with_respect_to = "state"
