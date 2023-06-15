from random import Random

from pytest import fixture

from .utils import generate_random_hex


@fixture()
def seed(pytestconfig):
    return pytestconfig.getoption("randomly_seed")


@fixture()
def rng(seed):
    return Random(seed)


@fixture()
def random_rgb(rng):
    return tuple((rng.randint(0, 255) for _ in range(3)))


@fixture()
def random_hex(rng):
    return generate_random_hex(rng)
