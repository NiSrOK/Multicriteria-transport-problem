import copy

def center_of_gravity_method(risk_m_list, quality):
    numerator = 0
    denominator = 0
    for i in range(3):
        numerator += risk_m_list[quality][i][0] * risk_m_list[quality][i][1]
        denominator += risk_m_list[quality][i][1]
    return numerator / denominator


def convert_road_quality(road_quality):
    road_quality_variants = ['Отличное', 'Хорошее', 'Нормальное', 'Плохое', 'Ужасное']
    risk_m_list = [[[0.5, 1], [1, 1], [1.5, 0.5]], [[1.5, 0.5], [2, 1], [2.5, 0.5]], [[2.5, 0.5], [3, 1], [3.5, 0.5]], [[3.5, 0.5], [4, 1], [4.5, 0.5]], [[4.33, 0.35], [4.5, 0.5], [5, 1]]]

    for i in range(len(road_quality)):
        for j in range(len(road_quality[0])):
            if road_quality[i][j] == road_quality_variants[0]:
                road_quality[i][j] = center_of_gravity_method(risk_m_list, 0)
            elif road_quality[i][j] == road_quality_variants[1]:
                road_quality[i][j] = center_of_gravity_method(risk_m_list, 1)
            elif road_quality[i][j] == road_quality_variants[2]:
                road_quality[i][j] = center_of_gravity_method(risk_m_list, 2)
            elif road_quality[i][j] == road_quality_variants[3]:
                road_quality[i][j] = center_of_gravity_method(risk_m_list, 3)
            elif road_quality[i][j] == road_quality_variants[4]:
                road_quality[i][j] = center_of_gravity_method(risk_m_list, 4)
    
    return road_quality

def convert_weather(weather):
    weather_variants = ['Отличное', 'Хорошее', 'Плохое']
    risk_m_list = [[[0.5, 1], [1, 1], [1.5, 0.5]], [[1.5, 0.5], [2, 1], [2.5, 0.5]], [[2.33, 0.3], [2.5, 0.5], [3, 1]]]

    for i in range(len(weather)):
        for j in range(len(weather[0])):
            if weather[i][j] == weather_variants[0]:
                weather[i][j] = center_of_gravity_method(risk_m_list, 0)
            elif weather[i][j] == weather_variants[1]:
                weather[i][j] = center_of_gravity_method(risk_m_list, 1)
            elif weather[i][j] == weather_variants[2]:
                weather[i][j] = center_of_gravity_method(risk_m_list, 2)

    return weather

def convert_number_accidents_per_year(number_accidents_per_year):
    accident_variants = ['Мало', 'Немного', 'Много', 'Очень много']
    accident_m_list = [[[5, 1], [10, 1], [15, 0.5]], [[20, 0.5], [30, 1], [35, 0.5]], [[45, 0.5], [60, 1], [65, 0.5]], [[80, 0.5], [100, 1], [110, 1]]]

    for i in range(len(number_accidents_per_year)):
        for j in range(len(number_accidents_per_year[0])):
            if number_accidents_per_year[i][j] == accident_variants[0]:
                number_accidents_per_year[i][j] = center_of_gravity_method(accident_m_list, 0)
            elif number_accidents_per_year[i][j] == accident_variants[1]:
                number_accidents_per_year[i][j] = center_of_gravity_method(accident_m_list, 1)
            elif number_accidents_per_year[i][j] == accident_variants[2]:
                number_accidents_per_year[i][j] = center_of_gravity_method(accident_m_list, 2)
            elif number_accidents_per_year[i][j] == accident_variants[3]:
                number_accidents_per_year[i][j] = center_of_gravity_method(accident_m_list, 3)

    for i in range(len(number_accidents_per_year)):
        for j in range(len(number_accidents_per_year[0])):
            if number_accidents_per_year[i][j] <= 10:
                number_accidents_per_year[i][j] = 1
            elif number_accidents_per_year[i][j] <= 30:
                number_accidents_per_year[i][j] = 2
            elif number_accidents_per_year[i][j] <= 60:
                number_accidents_per_year[i][j] = 3
            elif number_accidents_per_year[i][j] <= 100:
                number_accidents_per_year[i][j] = 4
            elif number_accidents_per_year[i][j] > 100:
                number_accidents_per_year[i][j] = 5

    return number_accidents_per_year

def risk_calculation(road_quality, weather, number_accidents_per_year):
    risks = copy.deepcopy(road_quality)
    road_quality = convert_road_quality(road_quality)
    weather = convert_weather(weather)
    number_accidents_per_year = convert_number_accidents_per_year(number_accidents_per_year)

    for i in range(len(risks)):
        for j in range(len(risks[0])):
            risks[i][j] = road_quality[i][j] + weather[i][j] + number_accidents_per_year[i][j]
    
    return risks
