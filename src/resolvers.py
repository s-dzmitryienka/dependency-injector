import inspect
from functools import wraps
from typing import Annotated, get_origin

from src.depends import Depends

InspectEmpty = inspect._empty  # noqa


def resolve_signature(f_sig: inspect.Signature, resolved_dependencies: dict = None) -> dict:
    if resolved_dependencies is None:
        resolved_dependencies = {}

    if not f_sig.parameters:
        return resolved_dependencies

    for p_value in f_sig.parameters.values():
        if p_value.default is InspectEmpty:
            # resolves not default Annotated types
            if get_origin(p_value.annotation) is Annotated:
                for annotated_dep in p_value.annotation.__metadata__:
                    if type(annotated_dep) == Depends:
                        assert callable(annotated_dep.dependency)
                        r_deps: dict = resolve_signature(inspect.signature(annotated_dep.dependency))
                        resolved_dependencies[p_value.name] = annotated_dep(**r_deps)
                        break

        # resolves default dependencies
        elif type(p_value.default) == Depends:
            assert callable(p_value.default.dependency)
            r_deps: dict = resolve_signature(inspect.signature(p_value.default.dependency))
            print(r_deps)
            resolved_dependencies[p_value.name] = p_value.default(**r_deps)
    return resolved_dependencies


def inject_deps(func):
    f_sig = inspect.signature(func)
    resolved_dependencies: dict = resolve_signature(f_sig)

    @wraps(func)
    def decorator(*args, **kwargs):
        bound = f_sig.bind_partial(*args, **kwargs)
        deps_bound = f_sig.bind_partial(**resolved_dependencies)
        default_arguments, resolved_arguments = bound.arguments, deps_bound.arguments
        resolved_arguments.update(default_arguments)
        return func(**resolved_arguments)
    return decorator
