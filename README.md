<div align="left">
  <h1><code>PYHephaestus - WIP</code></h1>
</div>


### Example

```python
from typing import final

from pyhephaestus import FuncInstrumentator


def some_function():
    print('Do work')


@final
class AddNotification(FuncInstrumentator):
    target = some_function.__code__

    on_enter = 'print("start instrumentation")'
    on_exit = 'print("end instrumentation")'


def main():
    some_function.__code__ = AddNotification
    some_function()


if __name__ == '__main__':
    main()
```