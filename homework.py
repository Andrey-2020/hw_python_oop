from dataclasses import dataclass, asdict, fields
from typing import Dict, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Создать сообщение."""
        TEXT_TRAINING_TYPE = ('Тип тренировки: {0}; '
                              'Длительность: {1:.3f} ч.; '
                              'Дистанция: {2:.3f} км; '
                              'Ср. скорость: {3:.3f} км/ч; '
                              'Потрачено ккал: {4:.3f}.')

        return (TEXT_TRAINING_TYPE.format(*asdict(self).values()))


@dataclass
class Training:
    """Базовый класс тренировки."""
    action: int
    duration: float
    weight: float

    LEN_STEP = 0.65
    M_IN_KM = 1000
    HOUR_PER_MINUTES = 60

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Данный функционал класса Training '
                                  'пока не реализован')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    LEN_STEP: float = 0.65
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                 + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight
                / self.M_IN_KM * self.duration * self.HOUR_PER_MINUTES)


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    height: float

    KMH_IN_MSEC = 0.278
    CM_IN_METR = 100
    CALORIES_WEIGHT_FIRST_MULTIPLIER = 0.035
    CALORIES_WEIGHT_SECOND_MULTIPLIER = 0.029
    EXPONENTIATION__MULTIPLIER = 2

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.CALORIES_WEIGHT_FIRST_MULTIPLIER * self.weight
                 + ((self.get_mean_speed() * self.KMH_IN_MSEC)
                    ** self.EXPONENTIATION__MULTIPLIER
                     / (self.height / self.CM_IN_METR))
                 * self.CALORIES_WEIGHT_SECOND_MULTIPLIER
                 * self.weight) * self.duration * self.HOUR_PER_MINUTES)


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    length_pool: float
    count_pool: float

    LEN_STEP = 1.38
    CALORIES_WEIGHT_FIRST_MULTIPLIER = 1.1
    EXPONENTIATION__MULTIPLIER = 2

    def get_mean_speed(self):
        """Получить значение средней скорости
        движения во время тренировки."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self):
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed() + self.CALORIES_WEIGHT_FIRST_MULTIPLIER)
                * self.EXPONENTIATION__MULTIPLIER * self.weight
                * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    WORKOUT_TYPE_CLASSES: Dict[str, Type[Training]] = {
        'SWM': (Swimming, len(fields(Swimming))),
        'RUN': (Running, len(fields(Running))),
        'WLK': (SportsWalking, len(fields(SportsWalking))),
    }

    if workout_type not in WORKOUT_TYPE_CLASSES:
        raise KeyError(f'Нет вида активности {workout_type} в '
                       f'доступных видах тернировок '
                       f'{WORKOUT_TYPE_CLASSES.keys()}')

    if len(data) != WORKOUT_TYPE_CLASSES[workout_type][1]:
        raise ValueError(f'Количество переданных на вход параметров '
                         f'не совпадает с тем, что наш класс готов принять '
                         f'{WORKOUT_TYPE_CLASSES[workout_type][0]}')
    return WORKOUT_TYPE_CLASSES[workout_type][0](*data)


def main(training: Training) -> None:
    """Главная функция."""
    return print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        main(read_package(workout_type, data))
