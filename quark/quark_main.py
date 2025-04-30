from invoke import Program

from .tasks import namespace

program = Program(namespace=namespace, name="quark")

if __name__ == "__main__":
    program.run()
