import random
from secrets import choice
from table import Table
from minimum_element_method import *
from potential_method import *
from risk_calculation import *
import time

def print_results(optimal_plan, transport_table, new_transport_table, transported_goods):
    result_costs = 0
    result_risks = 0

    for i in range(len(transport_table)):
        for j in range(len(transport_table[0])):
            if optimal_plan[i][j] != None and optimal_plan[i][j] != 0:
                print(f'Из пункта A{i+1} в пункт B{j+1} требуется доставить {optimal_plan[i][j]} единиц товара')
                result_costs += optimal_plan[i][j] * costs[i][j]
                result_risks += optimal_plan[i][j] * risks[i][j]
    
    if len(transport_table) < len(new_transport_table):
        print('\nНедостаток ресурсов:')
        for i in range(len(optimal_plan[0])):
            if optimal_plan[-1][i] != None and optimal_plan[-1][i] != 0:
                print(f'Пункт B{i+1} - {optimal_plan[-1][i]} единиц')
    elif len(transport_table[0]) < len(new_transport_table[0]):
        print('\nПереизбыток ресурсов:')
        for i in range(len(optimal_plan)):
            if optimal_plan[i][-1] != None and optimal_plan[i][-1] != 0:
                print(f'Пункт A{i+1} - {optimal_plan[i][-1]} единиц')

    print('')
    print('Общие расходы:', result_costs)
    print('Риски (2 - 13):', result_risks / sum(transported_goods))

def normalize_values(list_of_values):
    values = copy.deepcopy(list_of_values)

    maximum = values[0][0]
    minimum = values[0][0]
    for i in range(len(values)):
        for j in range(len(values[0])):
            if values[i][j] > maximum:
                maximum = values[i][j]
            if values[i][j] < minimum:
                minimum = values[i][j]
    
    for i in range(len(values)):
        for j in range(len(values[0])):
            values[i][j] = (values[i][j] - minimum) / (maximum - minimum)

    return values

def calculate_tariffs(norm_costs, norm_risks, weight_factor_risks, weight_factor_costs):
    transport_table = copy.deepcopy(norm_costs)

    for i in range(len(transport_table)):
        for j in range(len(transport_table[0])):
            transport_table[i][j] = norm_costs[i][j] * weight_factor_costs + norm_risks[i][j] * weight_factor_risks
    
    return transport_table

def random_risks_parameters(count_suppliers, count_buyers):
    road_quality_variants = ['Отличное', 'Хорошее', 'Нормальное', 'Плохое', 'Ужасное']
    weather_variants = ['Отличное', 'Хорошее', 'Плохое']

    road_quality = []
    weather = []
    number_accidents_per_year = []

    for i in range(count_suppliers):
        line_road = []
        line_weather = []
        line_number_accidents = []
        for j in range(count_buyers):
            line_road.append(choice(road_quality_variants))
            line_weather.append(choice(weather_variants))
            line_number_accidents.append(random.randint(0, 110))
        road_quality.append(line_road)
        weather.append(line_weather)
        number_accidents_per_year.append(line_number_accidents)

    return road_quality, weather, number_accidents_per_year

def print_double(arr):
    for i in range(len(arr)):
        print(arr[i])
    print()

def check_degeneracy(plan):
    count_base = 0
    for i in range(len(plan)):
        for j in range(len(plan[0])):
            if plan[i][j] != None:
                count_base += 1

    if len(plan) + len(plan[0]) - 1 > count_base:
        return True
    else:
        return False

def validation_data(data, weight_factor_risks, weight_factor_costs, needs, reserves):
    if weight_factor_risks is None or weight_factor_costs is None:
        return False
    
    if None in needs or None in reserves:
        return False

    for part in data:
        for line in part:
            if None in line:
                return False
    
    return True

if __name__ == "__main__":
    print('Введите количество поставщиков:')
    suppliers = int(input())
    print('Введите количество покупателей:')
    buyers = int(input())    
    table = Table(suppliers, buyers)

    table.createTable()
    table.fillTable()
    input(" Инструкция \n 1. Заполните Excel таблицу в папке с программой \n 2. Сохраните изменения в таблице и закройте ее \n 3. Для продолжения нажмите Enter") 
    
    start_time = time.time()

    table.updateTable()
    table.readTable()

    for _ in range(1):
        print('')
        print(f'Потребности: {table.needs}')
        print(f'Запасы: {table.reserves}')
        print('Сумма потребностей:', sum(table.needs))
        print('Сумма запасов:', sum(table.reserves))
        print(f'Стоимости перевозок: {table.costs}')
        
        needs = table.needs
        reserves = table.reserves
        costs = table.costs
        weight_factor_risks = table.weight_factor_risks
        weight_factor_costs = table.weight_factor_costs
        road_quality = table.road_quality
        weather = table.weather
        number_accidents_per_year = table.number_accidents

        # проверка корректности введенных данных
        data = [costs, road_quality, weather, number_accidents_per_year]
        if validation_data(data, weight_factor_risks, weight_factor_costs, needs, reserves) is False:
            print('Введенные данные некорректны. Проверьте данные в таблицах.')
            break

        # рассчитаем риски по входным параметрам
        risks = risk_calculation(road_quality, weather, number_accidents_per_year)

        print('Риски:', risks)
        print(f'Весовой множитель для стоимостей перевозок: {table.weight_factor_costs}')
        print(f'Весовой множитель для рисков: {table.weight_factor_risks}')
        print('')

        # нормализуем пути
        norm_costs = normalize_values(costs)

        # нормализуем риски
        norm_risks = normalize_values(risks)

        # рассчитаем тарифы транспортной таблицы
        transport_table = calculate_tariffs(norm_costs, norm_risks, weight_factor_risks, weight_factor_costs)

        # получим начальный план задачи методом наименьшего элемента
        initial_plan, new_transport_table = minimum_element_method(transport_table, needs, reserves)

        # проверяем план на вырожденность
        if check_degeneracy(initial_plan) is True:
            print('Начальный план вырожден. Оптимальный план не может быть найден.')
            break

        # получим оптимальный план методом потенциалов
        optimal_plan = potential_method(initial_plan, new_transport_table)

        # получим количество перевезенного товара
        if sum(table.needs) > sum(table.reserves):
            transported_goods = table.reserves
        else:
            transported_goods = table.needs
        
        print_results(optimal_plan, transport_table, new_transport_table, transported_goods)

        print(f"\nВремя работы программы: {time.time() - start_time} сек")
    