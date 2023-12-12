from classes import Car


def time_diff(car_object: Car, elapsed_time: int, timing_data: dict) -> int:
    if  elapsed_time > timing_data[car_object.brand][car_object.model]:
        time_diff = elapsed_time - timing_data[car_object.brand][car_object.model]
        timing_data[car_object.brand][car_object.model] = elapsed_time
    elif elapsed_time < timing_data[car_object.brand][car_object.model]:
        time_diff = timing_data[car_object.brand][car_object.model] - elapsed_time
        timing_data[car_object.brand][car_object.model] = elapsed_time
    else:
        time_diff = 0
    return time_diff, timing_data