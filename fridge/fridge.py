from decimal import Decimal
import datetime as dt

DATE_FORMAT = '%Y-%m-%d'


goods = {}


def add(items, title, amount, expiration_date=None):
    if title not in items:
        items[title] = []
    expiration_date = dt.datetime.strptime(
        expiration_date, DATE_FORMAT
    ).date() if expiration_date else expiration_date
    list.append(
        items[title],
        {'amount': amount, 'expiration_date': expiration_date}
    )


def add_by_note(items, note):
    parts = str.split(note, ' ')

    if len(str.split(parts[-1], '-')) == 3:
        expiration_date = parts[-1]
        good_amount = Decimal(parts[-2])
        title = str.join(' ', parts[0:-2])
    else:
        good_amount = Decimal(parts[-1])
        title = str.join(' ', parts[0:-1])
        expiration_date = None
    add(items, title, good_amount, expiration_date)


def find(items, needle):
    result = []

    for key in items:
        if needle.lower() in key.lower():
            result.append(key)
        elif needle.lower() == key.lower():
            result.append(key)
    return result

def get_amount(items, needle):
    product_amount = Decimal('0')

    for poduct in find(items, needle): # Клчюи словаря 
        for i in items[poduct]: # i - элемент в списке значений словаря 
            product_amount += Decimal(i['amount']) # обращение в элементе i (словаре) к ключу 'amount'
    return product_amount


def get_expired(items, in_advance_days=0):
    result = []
    TODAY = dt.date.today()
    exp = TODAY + dt.timedelta(days=in_advance_days)
   
    for key, value in items.items():
        amount = Decimal('0')
        for i in value:
            if i['expiration_date'] is not None:
                if i['expiration_date'] <= exp:
                    amount += i['amount']
        if amount > 0:
            result.append((key, amount))
    return result

def get_stats(items): # функция печати статистики 
    total_items = 0
    total_amount = Decimal('0')
    categories = set()
    expired_count = 0
    
    for p_name, p_items in items.items():
        categories.add(p_name)
        total_items += len(p_name)
        
        for i in p_items:
            total_amount += i['amount']
            if i['expiration_date'] and i['expiration_date'] < dt.date.today():
                expired_count += 1
                
    return {
        'total_categories': len(categories),
        'total_items': total_items,
        'total_amount': total_amount,
        'expired_items': expired_count,
        'categories': sorted(list(categories))
    }
    