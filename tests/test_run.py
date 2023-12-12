import os

from pytest_bdd import scenarios

scenarios(os.path.join(os.path.dirname(os.path.abspath(__file__)), "ui/features"))
