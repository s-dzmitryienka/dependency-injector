from typing import Annotated

from src.depends import Depends
from src.resolvers import inject_deps
from tests.fake_deps import get_one, get_text1, get_text2


@inject_deps
def f(dep1: Annotated[int, Depends(get_one, use_cache=False)], dep2: str = Depends(get_text1, use_cache=False), dep3: str = Depends(get_text2, use_cache=False)):
    return dep1, dep2, dep3


def test_injection():
    result = f()
    assert result == (1, "T1__0", "T2__T1__0")
