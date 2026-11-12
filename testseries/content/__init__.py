"""Question content engine for the 2026 test series (see the build_test_content management command)."""


def load_all():
    """Import every generator and bank so TOPICS is complete, then fold in the legacy seed questions."""
    from . import (bank_careers, bank_extra, bank_gk, bank_india, bank_professional, gen_computing, gen_english,  # noqa: F401
                   gen_math_school, gen_quant, gen_reasoning, gen_science, legacy, school)
    legacy.load()
    from .core import TOPICS
    return TOPICS
