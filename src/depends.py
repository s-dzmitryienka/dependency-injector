from typing import Dict, Callable, Any


class Depends:
    cache: Dict[Callable, Any] = {}

    def __init__(self, dependency: Callable, use_cache: bool = True):
        self.dependency = dependency
        self.use_cache = use_cache

    def __call__(self, *args, **kwargs) -> Any:
        if not self.use_cache:
            return self.dependency(*args, **kwargs)

        if self.dependency in Depends.cache:
            return Depends.cache[self.dependency]

        result = self.dependency(*args, **kwargs)
        Depends.cache[self.dependency] = result
        return result
