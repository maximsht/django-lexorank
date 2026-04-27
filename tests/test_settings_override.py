import pytest
from django.apps import apps
from django.test import override_settings

from django_lexorank.lexorank import LexoRank


@pytest.fixture
def restore_lexorank_attrs():
    saved = {
        "default_rank_length": LexoRank.default_rank_length,
        "rebalancing_length": LexoRank.rebalancing_length,
        "max_rank_length": LexoRank.max_rank_length,
    }
    yield
    for attr, value in saved.items():
        setattr(LexoRank, attr, value)


def _run_ready():
    apps.get_app_config("django_lexorank").ready()


def test_rebalancing_length_overridden_from_settings(restore_lexorank_attrs):
    with override_settings(LEXORANK_REBALANCING_LENGTH=20):
        _run_ready()
        assert LexoRank.rebalancing_length == 20


def test_default_rank_length_overridden_from_settings(restore_lexorank_attrs):
    with override_settings(LEXORANK_DEFAULT_RANK_LENGTH=8):
        _run_ready()
        assert LexoRank.default_rank_length == 8


def test_max_rank_length_overridden_from_settings(restore_lexorank_attrs):
    with override_settings(LEXORANK_MAX_RANK_LENGTH=300):
        _run_ready()
        assert LexoRank.max_rank_length == 300


def test_defaults_preserved_when_no_settings(restore_lexorank_attrs):
    _run_ready()
    assert LexoRank.default_rank_length == 6
    assert LexoRank.rebalancing_length == 128
    assert LexoRank.max_rank_length == 200


def test_other_attrs_unchanged_on_partial_override(restore_lexorank_attrs):
    with override_settings(LEXORANK_REBALANCING_LENGTH=20):
        _run_ready()
        assert LexoRank.rebalancing_length == 20
        assert LexoRank.default_rank_length == 6
        assert LexoRank.max_rank_length == 200
