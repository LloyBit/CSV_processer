from main import filtrate, aggregator, sort_datalist
import subprocess

# Мок CSV-данных
datalist = [
    ["name", "brand", "price", "rating"],
    ["iphone 15 pro", "apple", 999, 4.9],
    ["galaxy s23 ultra", "samsung", 1199, 4.8],
    ["redmi note 12", "xiaomi", 199, 4.6],
    ["poco x5 pro", "xiaomi", 299, 4.4],
]

# Фильтрация

def test_filtrate_text_column():
    result = filtrate(datalist, "brand", "xiaomi")
    assert len(result) == 3  # Заголовок + 2 строки
    assert all(row[1] == "xiaomi" for row in result[1:])

def test_filtrate_no_match():
    result = filtrate(datalist, "brand", "nokia")
    assert len(result) == 1  # Только заголовок

# Аггрегация и её подфункции

def test_aggregator_avg():
    result = aggregator(datalist, "price", "avg")
    assert result[0][0] == "avg"
    assert round(result[0][1], 1) == 674.0

def test_aggregator_max():
    result = aggregator(datalist, "rating", "max")
    assert result[0][1] == 4.9
    
def test_aggregator_min():
    result = aggregator(datalist, "rating", "min")
    assert result[0][1] == 4.4

def test_aggregator_invalid_column(capsys):
    broken_datalist = [
        ["name", "brand"],
        ["iphone", "apple"],
        ["galaxy", "samsung"]
    ]
    aggregator(broken_datalist, "brand", "avg")
    captured = capsys.readouterr()
    assert "Ошибка при обработке столбца" in captured.out

# Сортировка
def test_sort_string():
    result = sort_datalist(datalist, "brand", "asc")
    brands = [row[1] for row in result]
    assert brands == sorted(brands)

def test_sort_asc():
    result = sort_datalist(datalist, "price", "ask")
    prices = [row[2] for row in result]
    assert prices == sorted(prices)

def test_sort_desc():
    result = sort_datalist(datalist, "rating", "desc")
    ratings = [row[3] for row in result]
    assert ratings == sorted(ratings, reverse=True)
    

# Тесты ввода в CLI
CSV_PATH = "test_data.csv"
SCRIPT_PATH = "main.py"

def run_cli(args):
    cmd = ["python", SCRIPT_PATH, "-f", CSV_PATH] + args
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout

def test_filter_only():
    output = run_cli(["-w", "brand=apple"])
    assert "apple" in output
    assert "samsung" not in output
    assert "xiaomi" not in output

def test_aggregate_only():
    output = run_cli(["-a", "price=avg"])
    assert "avg" in output
    assert "596" in output  


def test_filter_aggregate():
    output = run_cli(["-w", "brand=xiaomi", "-a", "price=max"])
    assert "max" in output
    assert "379" in output
    assert "1199" not in output  # Общий экстремум

# Помимо кооперации смотрим чтобы перемешка порядка ввода не ломала логику скрипта
def test_order_filter():
    output = run_cli(["-o", "price=ask","-w", "brand=xiaomi"])
    assert "redmi note 12" in output and "poco x5 pro" in output
    assert output.index("199") < output.index("299")

