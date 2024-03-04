from typing import Annotated

from depends import Depends


def get_one():
    return 1


def get_zero() -> int:
    return 0


def get_text1(n_dep: Annotated[int, Depends(get_zero)]):
    return f"T1__{n_dep}"


def get_text2(k_dep: Annotated[str, Depends(get_text1)]):
    return f"T2__{k_dep}"
