<h1 align="center">
  <br>🛠️ PYHephaestus - WIP</br>
</h1>


### Example

```python
from pyhephaestus import instrumentation_wraps
from pyhephaestus.experemental import Call, Local


def insert_fn():
    print('inserted')


@instrumentation_wraps(
    on_enter=insert_fn.__code__,
    on_exit=Call(Local(name=insert_fn.__name__)),
)
def some_function():
    print('Do work')


if __name__ == '__main__':
    some_function()
```