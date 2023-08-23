import copy

def get_potentials(transport_table, plan):
    count_suppliers = len(transport_table)
    count_buyers = len(transport_table[0])
    u = [None] * count_suppliers
    v = [None] * count_buyers
    u[0] = 0

    flag = True
    while(flag):
        flag = False
        for i in range(count_suppliers):
            for j in range(count_buyers):
                if plan[i][j] != None:
                    if u[i] != None and v[j] == None:
                        v[j] = transport_table[i][j] - u[i]
                        flag = True
                    elif u[i] == None and v[j] != None:
                        u[i] = transport_table[i][j] - v[j]
                        flag = True

    return u, v

def check_optimality(u, v, transport_table):
    # вычислим разности Cij - (Ui + Vj)
    # план оптимален если все разности >= 0
    count_suppliers = len(transport_table)
    count_buyers = len(transport_table[0])

    delta = copy.deepcopy(transport_table)
    for i in range(count_suppliers):
        for j in range(count_buyers):
            delta[i][j] = None

    result_optimal = True
    for i in range(count_suppliers):
        for j in range (count_buyers):
            val =  transport_table[i][j] - (u[i] + v[j])
            if val < -1 * 10**(-10)  :
               result_optimal = False
            delta[i][j] = val

    return result_optimal, delta


def find_cycle(last_plan, cycle, count_suppliers, count_buyers):
    # ищем цикл из начальной ячейки пока не вернемся в нее
    ban = []
    line_number = cycle[0][0]
    column_number = 0
    while(1):
        new_cycle = find_horizontal(last_plan, line_number, cycle, count_buyers, ban)
        if new_cycle == cycle:
            ban.append(new_cycle[-1])
            line_number = cycle[0][0]
            cycle = [cycle[0]]
            continue
        cycle = new_cycle
        column_number = cycle[-1][1]
        new_cycle = find_vertical(last_plan, column_number, cycle, count_suppliers, ban)
        if new_cycle == cycle:
            ban.append(new_cycle[-1])
            line_number = cycle[0][0]
            cycle = [cycle[0]]
            continue
        cycle = new_cycle
        line_number = cycle[-1][0]
        if cycle[0] == cycle[-1] and len(cycle) > 1:
            break
    return cycle


def find_horizontal(last_plan, line_number, cycle, count_buyers, ban):
    # ищем базисную ячейку по-горизонтали
    new_cycle = copy.deepcopy(cycle)
    for j in range(count_buyers):
        if last_plan[line_number][j] != None and ([line_number, j] not in cycle) and ([line_number, j] not in ban):
            new_cycle.append([line_number, j])
            break
    return new_cycle


def find_vertical(last_plan, column_number, cycle, count_suppliers, ban):
    # ищем базисную ячейку по-вертикали
    new_cycle = copy.deepcopy(cycle)
    for i in range(count_suppliers):
        if i == new_cycle[0][0] and column_number == cycle[0][1]:
            new_cycle.append([i, column_number])
            break
        elif last_plan[i][column_number] != None and ([i, column_number] not in new_cycle) and ([i, column_number] not in ban):
            new_cycle.append([i, column_number])
            break
    return new_cycle


def get_new_plan(last_plan, delta):    
    count_suppliers = len(delta)
    count_buyers = len(delta[0])
    minimum = delta[0][0]
    idx_minimum = [0,0]
    for i in range(count_suppliers):
        for j in range(count_buyers):
            if delta[i][j] < minimum:
                minimum = delta[i][j]
                idx_minimum[0] = i
                idx_minimum[1] = j

    # для улучшения плана найдем цикл начиная с ячейки с максимальной разностью
    cycle = [idx_minimum]
    cycle = find_cycle(last_plan, cycle, len(last_plan), len(last_plan[0]))
    
    # удалим из цикла повторяющуюся ячейку
    cycle.pop(-1)

    # присвоим свободной ячейке, которую мы хотим перенести в базис, значение 0
    last_plan[cycle[0][0]][cycle[0][1]] = 0

    # ищем минимальное значение груза
    minimum = last_plan[cycle[1][0]][cycle[1][1]]
    indexes = [cycle[1][0], cycle[1][1]]
    for i in range(len(cycle)):
        if i % 2 != 0 and last_plan[cycle[i][0]][cycle[i][1]] < minimum:
            minimum = last_plan[cycle[i][0]][cycle[i][1]]
            indexes[0] = cycle[i][0]
            indexes[1] = cycle[i][1]
            
    
    # вычитаем и прибавляем к ячейкам цикла минимальное значение груза
    for i in range(len(cycle)):
        if i % 2 != 0:
            last_plan[cycle[i][0]][cycle[i][1]] -= minimum
        else:
            last_plan[cycle[i][0]][cycle[i][1]] += minimum
    
    # делаем свободной базисную клетку с минимальным значением груза
    last_plan[indexes[0]][indexes[1]] = None
    
    return last_plan


def potential_method(plan, transport_table):
    last_plan = plan
    while(1):
        # найдем потенциалы для плана
        u, v = get_potentials(transport_table, last_plan)

        # проверим план на оптимальность
        result, delta = check_optimality(u, v, transport_table)
        
        # в случае неоптимальности - вычислим новый план
        if result == False:
                last_plan = get_new_plan(last_plan, delta)
        else:
            break

    return last_plan
