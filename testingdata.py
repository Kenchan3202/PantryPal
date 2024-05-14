import datetime

items = [
    {"name": "Milk", "expiry_date": "2024-05-10", 'quantity': '2', 'calories': 200},
    {"name": "jelly", "expiry_date": "2024-05-11", 'quantity': '5', 'calories': 250},
    {"name": "pork", "expiry_date": "2024-05-12", 'quantity': '4', 'calories': 350},
    {"name": "chocolate", "expiry_date": "2024-05-12", 'quantity': '4', 'calories': 360},
    {"name": "Goat Milk", "expiry_date": "2024-05-13", 'quantity': '2', 'calories': 200},
    {"name": "Bread", "expiry_date": "2024-05-12", 'quantity': '2', 'calories': 100},
    {"name": "Apple", "expiry_date": "2024-04-28", 'quantity': '5', 'calories': 60},
    {"name": "Beef", "expiry_date": "2024-06-30", 'quantity': '5', 'calories': 500},
    {"name": "Lamb", "expiry_date": "2024-09-28", 'quantity': '3', 'calories': 450},
    {"name": "Apple juice", "expiry_date": "2024-05-04", 'quantity': '1', 'calories': 150},
]
used_items = [
    {"name": "Milk", 'calories': 200},
    {"name": "Bread", 'calories': 100},
    {"name": "Apple", 'calories': 60},
    {"name": "Beef", 'calories': 500},
]
used_calories = set()

for item in used_items:
    used_calories.add(item['calories'])

expiry_dates = set()

for item in items:
    expiry_dates.add(item['expiry_date'])

today = datetime.date.today()

seven_days_later = today + datetime.timedelta(days=7)

soon_to_expire = set()
soon_to_expire_seven = []

expired = set()

# not_yet_expire = set()

for item in items:
    # 将字符串日期转换为datetime.date对象
    expiry_date = datetime.datetime.strptime(item['expiry_date'], "%Y-%m-%d").date()

    if expiry_date <= today:
        # 如果是，将物品名称添加到集合中
        expired.add(item['name'])

not_yet_expire = [item for item in items if
                  datetime.datetime.strptime(item['expiry_date'], "%Y-%m-%d").date() > today]

for item in items:
    # 将字符串日期转换为datetime.date对象
    expiry_date = datetime.datetime.strptime(item['expiry_date'], "%Y-%m-%d").date()

    # 检查该日期是否在今天和7天后之间
    if today <= expiry_date <= seven_days_later:
        # 如果是，将物品名称添加到集合中
        soon_to_expire.add(item['name'])

for item in items:
    # 将字符串日期转换为datetime.date对象
    expiry_date = datetime.datetime.strptime(item['expiry_date'], "%Y-%m-%d").date()

    # 检查该日期是否在今天和7天后之间
    if today <= expiry_date <= seven_days_later:
        soon_to_expire_seven.append({"name": item['name'], "expiry_date": item['expiry_date']})
