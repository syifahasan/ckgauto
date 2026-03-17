import random


def generate_weight_height(jk: str, umur: int) -> tuple[int, int]:
    jk = jk.lower()
    if 18 <= umur < 60:
        return (random.randint(60, 80), random.randint(165, 175)) if jk == "laki-laki" else (random.randint(50, 70), random.randint(155, 170))
    return (random.randint(55, 75), random.randint(160, 170)) if jk == "laki-laki" else (random.randint(45, 65), random.randint(150, 165))


def generate_waist(jk: str, tb: int) -> int:
    base = tb * 0.45
    return int(base + random.randint(-8, 12)) if jk.lower() == "laki-laki" else int(base + random.randint(-6, 10))


def generate_blood_pressure(jk: str, umur: int) -> tuple[int, int]:
    if umur < 40:
        return (random.randint(120, 130), random.randint(75, 85)) if jk.lower() == "laki-laki" else (random.randint(110, 130), random.randint(70, 85))
    return random.randint(120, 150), random.randint(80, 95)


def generate_blood_sugar() -> int:
    return random.randint(90, 140)
