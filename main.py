import argparse
from tabulate import tabulate
import csv
from statistics import mean

# Фильтрация по колонке
def filtrate(datalist, column, value):
    column_index = datalist[0].index(column)
    filtry = [datalist[0]]+[i for i in datalist if i[column_index] == value]
    return filtry
# print(filtrate(datalist, "brand", "apple"))


# Функция среднего арифметического
def avg(lst):
    return mean(lst)

# Словарь для функций аггрегации
func_name_dict = {
    "min":min,
    "max":max,
    "avg":avg
}

# Аггрегация по числовым значениям
def aggregator(datalist, column, agg_func):
    try:
        column_index = datalist[0].index(column)
        true_func = func_name_dict[agg_func]
        preaggry = [i[column_index] for i in datalist[1:]]
        aggry = [[agg_func, true_func(preaggry)]]
        return aggry
    except:
        print("Ошибка при обработке столбца. Он содержит необрабатываемый формат данных")
# print(aggregate(datalist, "rating", "avg"))


# Сортировка по значению и направлению(Возрастание по умолчанию)
def sort_datalist(datalist, column, way):
    desc = False
    if way == "desc":
        desc = True
    sorty = sorted(datalist[1:], key=lambda x: x[datalist[0].index(column)], reverse=desc)
    return sorty
# print(sort_datalist(datalist, "price", "ask"))


# Задаем параметры запуска скрипта
parser = argparse.ArgumentParser(description='Filtering and aggregation')

parser.add_argument('-f', '--file', default="data.csv", type=argparse.FileType('r'), help='Path to csv-file')
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
        
# print(tabulate(datalist, tablefmt="grid", numalign="right"))


# Извлекаем параметры из запроса и сразу применяем их
if args.where:
    where = args.where.split("=") 
    datalist = filtrate(datalist, where[0], where[1])
if args.aggregate:  
    aggregate = args.aggregate.split("=")
    datalist = aggregator(datalist, aggregate[0], aggregate[1])
elif args.order_by:
    order_by = args.order_by.split("=")
    datalist = sort_datalist(datalist, order_by[0], order_by[1])
    
print(tabulate(datalist, tablefmt="grid", numalign="right"))