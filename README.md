<div align="left">
  <h1><code>PYHephaestus - WIP</code></h1>
</div>


### Example

```python
from pyhephaestus import instrumentation_wraps


@instrumentation_wraps(
    on_enter='print("start instrumentation")',
    on_exit='print("end instrumentation")',
)
def some_function():
    print('Do work')

    
if __name__ == '__main__':
    some_function()
```