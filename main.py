from typing import Union
from tabulate import tabulate
import argparse
import csv

# Фильтрация по колонке
def filtrate(datalist, column, value) -> list:
    column_index = datalist[0].index(column)
    filtry = [datalist[0]]+[i for i in datalist if i[column_index] == value]
    return filtry


# Функция среднего арифметического
def avg(lst: list[Union[int, float]]) -> float:
    return sum(lst) / len(lst)

# Словарь для функций аггрегации
func_name_dict = {
    "min":min,
    "max":max,
    "avg":avg
}

# Аггрегация по числовым значениям
def aggregator(datalist:list, column:str, agg_func:str) -> Union[list, None]:
    try:
        column_index = datalist[0].index(column)
        true_func = func_name_dict[agg_func]
        preaggry = [i[column_index] for i in datalist[1:]]
        aggry = [[agg_func, true_func(preaggry)]]
        return aggry
    except:
        print("Ошибка при обработке столбца. Он содержит необрабатываемый формат данных")


# Сортировка по значению и направлению(Возрастание по умолчанию)
def sort_datalist(datalist:list, column:str, way:str) -> list:
    desc = False
    if way == "desc":
        desc = True
    sorty = sorted(datalist[1:], key=lambda x: x[datalist[0].index(column)], reverse=desc)
    return sorty

# Изолируем инициализацию от сторонних модулей(тестов)
if __name__ == "__main__":
    # Задаем параметры запуска скрипта
    parser = argparse.ArgumentParser(description='Filtering and aggregation')
    parser.add_argument('-f', '--file', default="test_data.csv", type=argparse.FileType('r'), help='Path to csv-file')
    parser.add_argument('-w', '--where', default=False, type=str, help='Filter by column')
    parser.add_argument('-a', '--aggregate', default=False, type=str, help='Parametrize aggregation')
    parser.add_argument('-o', '--order-by', default=False, type=str, help='Ask/desc ordering')
    args = parser.parse_args()

    # Парсинг csv-файла в список datalist
    with args.file as csvfile:
        csvreader = csv.reader(csvfile)
        datalist = []
        
        for row in csvreader:
            # Конвертируем строки в числа или float если можем
            for id, value in enumerate(row):
                try:
                    row[id] = int(value)
                except:
                    try: 
                        row[id] = float(value)
                    except:
                        pass
                    
            datalist.append(row)

    # Извлекаем параметры из запроса и сразу применяем их
    if args.where:
        where = args.where.split("=") 
        # Возможна сортировка по числовым значениям, преобразуем если можем
        for id, value in enumerate(where):
                try:
                    where[id] = int(value)
                except:
                    try: 
                        where[id] = float(value)
                    except:
                        pass
        datalist = filtrate(datalist, where[0], where[1])
        
    if args.aggregate and not(args.order_by):  
        aggregate = args.aggregate.split("=")
        datalist = aggregator(datalist, aggregate[0], aggregate[1])
        
    if args.order_by and not(args.aggregate):
        order_by = args.order_by.split("=")
        datalist = sort_datalist(datalist, order_by[0], order_by[1])
        
    if args.order_by and args.aggregate:
        raise Exception("Недопустимое сочетание аргументов")
    
    # Конечный вывод
    print(tabulate(datalist, tablefmt="grid", numalign="right"))