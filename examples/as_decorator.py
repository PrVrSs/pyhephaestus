from pyhephaestus import instrumentation_wraps


@instrumentation_wraps(
    on_enter='print("start instrumentation")',
    on_exit='print("end instrumentation")',
)
def some_function():
    print('Do work')


def main():
    some_function()


if __name__ == '__main__':
    some_function()
