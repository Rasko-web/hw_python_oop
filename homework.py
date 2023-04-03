class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:

        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    MIN_IN_HOU = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float = 0
                 ) -> None:
        self.action = action
        self.duration = duration
        self.height = height
        self.weight = weight

    def get_distance(self) -> float:
        if self.__class__.__name__ == 'Swimming':
            self.LEN_STEP = 1.38
            return self.action * self.LEN_STEP / self.M_IN_KM
        else:
            return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_type = self.__class__.__name__
        duration = self.duration
        distance = self.get_distance()
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()

        Information = InfoMessage(training_type,
                                  duration,
                                  distance,
                                  speed,
                                  calories)
        return Information


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def __init__(self, action: int,
                 duration: float,
                 weight: float):
        super().__init__(action, duration, weight)

    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self):
        return ((Running.CALORIES_MEAN_SPEED_MULTIPLIER
                * super().get_mean_speed()
                + Running.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM
                * (self.duration * self.MIN_IN_HOU))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    FIRST_CONST = 0.035
    SECOND_CONST = 0.029
    SPEED_SEC = 0.278
    SAN_IN_METRS = 100

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height) -> None:
        super().__init__(action, duration, weight, height)
        self.height: float = self.height / self.SAN_IN_METRS

    def get_spent_calories(self) -> float:
        return (((SportsWalking.FIRST_CONST
                * self.weight + (((super().get_mean_speed()
                 * SportsWalking.SPEED_SEC) ** 2) / self.height)
                 * SportsWalking.SECOND_CONST * self.weight)
                 * self.duration * self.MIN_IN_HOU))


class Swimming(Training):
    """Тренировка: плавание."""
    CONST_FOR_SWIM = 1.1
    MULTIPLIER = 2
    LEN_STEP = 1.38

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 length_pool,
                 count_pool) -> None:
        super().__init__(action, duration, weight)
        self.count_pool = count_pool
        self.length_pool = length_pool

    def get_mean_speed(self) -> float:
        return ((self.length_pool * self.count_pool)
                / self.M_IN_KM) / (self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + Swimming.CONST_FOR_SWIM)
                * Swimming.MULTIPLIER * self.weight * (self.duration))


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    comands = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
    }

    if workout_type in comands:
        cmd = comands[workout_type]
        workout_type = cmd(*data)
        return workout_type
    else:
        print("ERROR")


def main(training: Training) -> None:
    """Главная функция."""

    info = Training.show_training_info(training)
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
