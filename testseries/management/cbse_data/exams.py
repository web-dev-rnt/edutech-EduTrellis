"""Competitive-exam pattern mocks (see seed_exam_series). Each exam name is also its 'Explore Exams' category."""
from .exams_banking import EXAMS as BANKING
from .exams_defence import EXAMS as DEFENCE
from .exams_engg_medical import EXAMS as ENGG_MEDICAL
from .exams_entrance import EXAMS as ENTRANCE
from .exams_govt_jobs import EXAMS as GOVT_JOBS
from .exams_other import EXAMS as OTHER
from .exams_professional import EXAMS as PROFESSIONAL
from .exams_school_olympiad import EXAMS as SCHOOL_OLYMPIAD
from .exams_ssc_railway import EXAMS as SSC_RAILWAY
from .exams_teaching_school import EXAMS as TEACHING_SCHOOL

EXAMS = (
    ENGG_MEDICAL + DEFENCE + SSC_RAILWAY + BANKING + OTHER
    + ENTRANCE + PROFESSIONAL + GOVT_JOBS + TEACHING_SCHOOL + SCHOOL_OLYMPIAD
)
