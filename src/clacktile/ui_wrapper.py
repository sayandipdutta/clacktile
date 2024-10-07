from collections.abc import Callable

from textual.app import ComposeResult
from textual.widgets import Footer, Header


type Composer[T] = Callable[[T], ComposeResult]


def wrap_body[T](
    header: bool = True, footer: bool = False
) -> Callable[[Composer[T]], Composer[T]]:
    def deco(
        composer: Composer[T],
    ) -> Composer[T]:
        def inner(app: T) -> ComposeResult:
            if header:
                yield Header()
            yield from composer(app)
            if footer:
                yield Footer()

        return inner

    return deco
