from typing import final

from pyhephaestus import FuncInstrumentator


def some_function(text: str) -> None:
    print(text)


@final
class AddNotification(FuncInstrumentator):
    target = some_function.__code__

    on_enter = 'print("start instrumentation")'
    on_exit = r'print("end instrumentation", end="\n\n")'


def main() -> None:
    origin_code = some_function.__code__

    some_function.__code__ = AddNotification
    some_function('with instrumentation')

    some_function.__code__ = origin_code
    some_function('without instrumentation')


if __name__ == '__main__':
    main()
