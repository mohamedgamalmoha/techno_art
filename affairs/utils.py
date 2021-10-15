from typing import List

from django.utils import timezone


MONTHS_DICT = {
    1: ("Jan", "يناير"),
    2: ("Feb", "فبراير"),
    3: ("Mar", "مارس"),
    4: ("Apr", "أبريل"),
    5: ("May", "مايو"),
    6: ("Jun", "يونيو"),
    7: ("Jul", "يوليو"),
    8: ("Aug", "أغسطس"),
    9: ("Sep", "سبتمبر"),
    10: ("Oct", "أكتوبر"),
    11: ("Nov", "نوفمبر"),
    12: ("Dec", "ديسمبر"),
}


def years_range(num_range=5) -> List[int]:
    now_time = timezone.now()
    return list(range((now_time.year - num_range), (now_time.year + num_range + 1)))


MONTHS_NAMES = MONTHS_DICT.values()
MONTHS_NUMBERS = MONTHS_DICT.keys()
YEARS_NUMBERS = ((year, year) for year in years_range())
