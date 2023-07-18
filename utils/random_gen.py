import random


def gen_steamid() -> str:
    return f'76561198{random.randint(10000000, 99999999)}'
