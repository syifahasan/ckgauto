from typing import Optional

from src.utils.random_exam_utils import (
    generate_weight_height,
    generate_waist,
    generate_blood_pressure,
    generate_blood_sugar,
)


def normalize_exam_values(
    jk: str,
    umur: int,
    bb: Optional[float],
    tb: Optional[float],
    sistol: Optional[int],
    diastol: Optional[int],
    gds: Optional[int],
) -> dict:
    # fallback gizi
    auto_bb, auto_tb = generate_weight_height(jk, umur)
    final_bb = int(bb) if bb is not None else auto_bb
    final_tb = int(tb) if tb is not None else auto_tb
    final_lp = generate_waist(jk, final_tb)

    # fallback tekanan darah
    auto_sistol, auto_diastol = generate_blood_pressure(jk, umur)
    final_sistol = sistol if sistol is not None else auto_sistol
    final_diastol = diastol if diastol is not None else auto_diastol

    # fallback gula darah
    final_gds = gds if gds is not None else generate_blood_sugar()

    return {
        "bb": final_bb,
        "tb": final_tb,
        "lp": final_lp,
        "sistol": final_sistol,
        "diastol": final_diastol,
        "gds": final_gds,
    }