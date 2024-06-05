from typing import Iterable

from sqlmodel import SQLModel


def require(model: SQLModel, *which: Iterable[str]):
    if not which:  # require all
        which = model.schema()["properties"].keys()
    new_model = type(
        f"{model.__name__}__{'_'.join(which)}",
        model.__bases__,
        dict(model.__dict__),
    )
    for field in list(new_model.__fields__.keys()):
        if field not in which:
            del new_model.__fields__[field]
    return new_model
