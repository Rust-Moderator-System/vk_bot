from typing import Final


class BotTypes:
    MAIN = 'main'


SECONDS_IN_DAY: Final[int] = 86400

# DEFAULT PARAMETERS
DAYS_SHOW_BANS: Final[int] = 60


RUST_SERVERS_NAMES: list[str] = [
    'MAGIC',
    'MR',
    'GRAND',
    'TRAVELER',
    'ULTIMATE',
    'ROOM',
    'BEARZ',
    'BRO',
    'ORION',
    'FUNRUST',
    'BOLOTO',
    'MAGMA',
    'TOFFS',
]

RCC_SERVER_NAMES: list[str] = [
    'rustroom',
]


AVAILABLE_BAN_REASONS: list[str] = [
    'чит',
    'cheat',
    'macro',
    'макро',
    'eac',
    'еак',
    'm-a',
    'm/a',
    'м/а',
    'multiacc',
    'мультиакк',
    'покинул',
    'отказ',
    'disconnect',
    'вышел',
    'выход',
    'leave',
    'игнор',
    'ignore',
    'результатам',
    'просвет',
    'неверные',
    'чистка',
]

NOT_AVAILABLE_BAN_REASONS: list[str] = [
    'игра с читером',
    'game with cheater',
    'you had eac ban on your account',
    'тим чит',
]