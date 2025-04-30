from functools import wraps

from invoke import Collection, task


def check_framework(func):
    """
    Decorator to check that the `framework` argument is either 'torch' or 'tensorflow'.
    """

    @wraps(func)
    def wrapper(ctx, framework=None, *args, **kwargs):
        if framework is None:
            print("Error: The `framework` argument is required.")
            print("       Use --framework='torch' or 'tensorflow' to specify.")
            return

        if framework not in ["torch", "tensorflow"]:
            print(
                f"Error: Invalid framework '{framework}'. Must be 'torch' or 'tensorflow'."
            )
            print(f"       use --framework='torch' or 'tensorflow' to specify.")
            return

        return func(ctx, framework=framework, *args, **kwargs)

    return wrapper
