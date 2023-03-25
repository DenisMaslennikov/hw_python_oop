
from dataclasses import asdict, dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Получить информацию о тренировке."""
        info_message: str = ('Тип тренировки: {training_type}; Длительность: '
                             '{duration:.3f} ч.; Дистанция: {distance:.3f}'
                             ' км; Ср. скорость: {speed:.3f} км/ч; Потрачено '
                             'ккал: {calories:.3f}.')
        return (info_message.format(**asdict(self)))


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65  # длинна шага в метрах
    M_IN_KM: int = 1000
    HOURS_IN_MIN: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> None:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Abstract method')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        """Получить количество потраченных на бег калории"""
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight
                / self.M_IN_KM * self.duration * self.HOURS_IN_MIN)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_WEIGHT_SECOND_MULTIPLIER: float = 0.029
    KMH_IN_MS: float = 0.278
    CM_IN_M = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество потраченных на ходьбу калории"""
        return ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                + ((self.get_mean_speed() * self.KMH_IN_MS) ** 2 / (self.height
                 / self.CM_IN_M)) * self.CALORIES_WEIGHT_SECOND_MULTIPLIER
                * self.weight) * self.duration * self.HOURS_IN_MIN)


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38  # Длинна гребка при плавание
    CALORIES_MEAN_SPEED_SHIFT: float = 1.1
    CALORIES_SPEED_MULTIPLIER: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость плавания."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        '''Получить количество потраченных на плавание калорий'''
        return ((self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.CALORIES_SPEED_MULTIPLIER * self.weight * self.duration)


def read_package(workout_type: str, data: list[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_type_to_class = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking, }
    training = training_type_to_class.get(workout_type, None)
    if training:
        return training(*data)
    raise KeyError('Valid workout type only: \'SWM\' - Swimming, \'RUN\' - '
                   'Running, \'WLK\' - SportsWalking,')


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages: list[tuple[str, list[int]]] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
