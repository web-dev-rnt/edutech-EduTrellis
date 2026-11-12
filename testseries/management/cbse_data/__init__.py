"""Question banks for the board-wise, class-wise test series (see seed_school_series)."""
from . import icse, senior, up_board
from .primary import CLASSES as PRIMARY
from .middle import CLASSES as MIDDLE
from .secondary import CLASSES as SECONDARY

CBSE_CLASSES = {**PRIMARY, **MIDDLE, **SECONDARY}

# board -> {'classes': {grade: tests}, 'streams': {grade: {stream: tests}}, 'senior_name': name used for 11-12}
BOARDS = {
    'CBSE': {'classes': CBSE_CLASSES, 'streams': senior.STREAMS, 'senior_name': 'CBSE'},
    'ICSE': {'classes': icse.CLASSES, 'streams': icse.STREAMS, 'senior_name': 'ISC'},
    'UP Board': {'classes': up_board.CLASSES, 'streams': up_board.STREAMS, 'senior_name': 'UP Board'},
}
