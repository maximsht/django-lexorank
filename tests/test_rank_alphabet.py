"""Invariant: every rank produced by ``LexoRank`` must use only ``base_symbols`` (a-z).

Out-of-alphabet characters (e.g. ``{`` = ``chr(ord('a') + 26)``) corrupt persisted
ranks and break further ``get_lexorank_in_between`` / ``increment_rank`` calls.
"""
import random

import pytest

from django_lexorank.lexorank import LexoRank


def _assert_in_alphabet(rank: str) -> None:
    bad = [c for c in rank if c not in LexoRank.base_symbols]
    assert not bad, (
        f"rank {rank!r} contains characters outside alphabet "
        f"{LexoRank.base_symbols!r}: {bad}"
    )


class TestGetLexorankInBetweenAlphabet:
    @pytest.mark.parametrize(
        "previous_rank, next_rank, objects_count",
        [
            # Minimal reproducer: total_diff == 2 with previous tail == 'z'.
            # Triggers ``middle_rank_part == cls.base`` (== 26) which the buggy
            # ``> cls.base`` condition fails to carry, producing ``chr(123) == '{'``.
            ("az", "bb", 1),
            ("az", "bb", 2),
            ("aaz", "abb", 1),
            ("yz", "zb", 1),
            ("ay", "ba", 1),
        ],
    )
    def test_returns_only_alphabet_chars(
        self, previous_rank: str, next_rank: str, objects_count: int
    ) -> None:
        result = LexoRank.get_lexorank_in_between(
            previous_rank=previous_rank,
            next_rank=next_rank,
            objects_count=objects_count,
        )
        _assert_in_alphabet(result)
        assert previous_rank < result < next_rank, (
            f"ordering broken: {previous_rank!r} < {result!r} < {next_rank!r}"
        )

    def test_property_random_inputs_never_produce_out_of_alphabet(self) -> None:
        """For 1000 random valid (prev, next) pairs the output stays in [a-z]."""
        rng = random.Random(42)
        checked = 0
        for _ in range(2000):
            length = rng.randint(1, 10)
            prev = "".join(rng.choices(LexoRank.base_symbols, k=length))
            nxt = "".join(rng.choices(LexoRank.base_symbols, k=length))
            if prev >= nxt:
                continue
            count = rng.randint(1, 1000)
            try:
                result = LexoRank.get_lexorank_in_between(
                    previous_rank=prev,
                    next_rank=nxt,
                    objects_count=count,
                )
            except ValueError:
                continue
            _assert_in_alphabet(result)
            checked += 1
        assert checked >= 500, f"expected >=500 valid pairs, only checked {checked}"
