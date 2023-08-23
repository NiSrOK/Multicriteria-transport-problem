import copy

def make_close_task_add_needs(needs, reserves, transport_table):
    # приведем задачу к закрытой при избытке запасов
    big_transport_tariff = 3

    new_needs = copy.deepcopy(needs)
    new_transport_table = copy.deepcopy(transport_table)
    new_needs.append(sum(reserves) - sum(needs))
    for i in range(len(new_transport_table)):
        new_transport_table[i].append(big_transport_tariff)

    return new_needs, new_transport_table

def make_close_task_add_reserves(needs, reserves, transport_table):
    # приведем задачу к закрытой при недостатке запасов
    big_transport_tariff = 3

    new_reserves = copy.deepcopy(reserves)
    new_transport_table = copy.deepcopy(transport_table)
    new_reserves.append(sum(needs) - sum(reserves))
    new_transport_table.append([big_transport_tariff] * len(transport_table[0]))
    
    return new_reserves, new_transport_table

def minimum_element_method(transport_table, needs, reserves):
    copy_needs = copy.deepcopy(needs)
    copy_reserves = copy.deepcopy(reserves)
    copy_transport_table = copy.deepcopy(transport_table)

    #сведем задачу к закрытой
    if sum(needs) > sum(reserves):
        copy_reserves, copy_transport_table = make_close_task_add_reserves(copy_needs, copy_reserves, copy_transport_table)
    elif sum(reserves) > sum(needs):
        copy_needs, copy_transport_table = make_close_task_add_needs(copy_needs, copy_reserves, copy_transport_table)

    transport_table_for_return = copy.deepcopy(copy_transport_table)

    count_suppliers = len(copy_transport_table)
    count_buyers = len(copy_transport_table[0])

    plan = copy.deepcopy(copy_transport_table)
    for i in range(count_suppliers):
        for j in range(count_buyers):
            plan[i][j] = None

    while sum(copy_needs) != 0:
        indexes = [0, 0]
        minimum = None
        for i in range(count_suppliers):
            for j in range(count_buyers):
                if minimum == None and copy_transport_table[i][j] != None:
                    minimum = copy_transport_table[i][j]
                    indexes[0] = i
                    indexes[1] = j

                if copy_transport_table[i][j] != None and minimum > copy_transport_table[i][j]:
                    indexes[0] = i
                    indexes[1] = j

        if copy_reserves[indexes[0]] > copy_needs[indexes[1]]:
            plan[indexes[0]][indexes[1]] = copy_needs[indexes[1]]
            copy_reserves[indexes[0]] -= copy_needs[indexes[1]]
            copy_needs[indexes[1]] = 0
            for i in range(count_suppliers):
                copy_transport_table[i][indexes[1]] = None
        elif copy_reserves[indexes[0]] == copy_needs[indexes[1]]:
            plan[indexes[0]][indexes[1]] = copy_needs[indexes[1]]
            copy_needs[indexes[1]] = 0
            copy_reserves[indexes[0]] = 0
            for j in range(count_buyers):
                copy_transport_table[indexes[0]][j] = None
            for i in range(count_suppliers):
                copy_transport_table[i][indexes[1]] = None
        else:
            plan[indexes[0]][indexes[1]] = copy_reserves[indexes[0]]
            copy_needs[indexes[1]] -= copy_reserves[indexes[0]]
            copy_reserves[indexes[0]] = 0
            for j in range(count_buyers):
                copy_transport_table[indexes[0]][j] = None

    return plan, transport_table_for_return
