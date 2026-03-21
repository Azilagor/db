import uuid
import random
from datetime import date, timedelta
from faker import Faker

fake = Faker('ru_RU')

def uid():
    return str(uuid.uuid4())

def rand_date(start: date, end: date) > date:
    delta = (end  start).days
    return start + timedelta(days=random.randint(0, delta))

def sql_str(val):
    if val is None:
        return 'NULL'
    val = str(val).replace("'", "''")
    return f"'{val}'"

def sql_bool(val):
    return 'TRUE' if val else 'FALSE'


# Fixed IDs


LEVEL_IDS = [
    '11111111000000000000000000000001',  # beginner
    '11111111000000000000000000000002',  # intermediate
    '11111111000000000000000000000003',  # expert
]

SEASON_IDS = [
    '22222222000000000000000000000001',  # spring
    '22222222000000000000000000000002',  # summer
    '22222222000000000000000000000003',  # autumn
    '22222222000000000000000000000004',  # winter
]

ROUTE_IDS = [
    '55555555000000000000000000000001',
    '55555555000000000000000000000002',
    '55555555000000000000000000000003',
    '55555555000000000000000000000004',
]

INVENTORY_IDS = [
    '77777777000000000000000000000001',
    '77777777000000000000000000000002',
    '77777777000000000000000000000003',
    '77777777000000000000000000000004',
    '77777777000000000000000000000005',
    '77777777000000000000000000000006',
    '77777777000000000000000000000007',
    '77777777000000000000000000000008',
]

TRANSPORT_IDS = [
    '88888888000000000000000000000001',
    '88888888000000000000000000000002',
    '88888888000000000000000000000003',
    '88888888000000000000000000000004',
    '88888888000000000000000000000005',
]

ROUTE_POINT_IDS = [
    '66666666000000000000000000000001',
    '66666666000000000000000000000002',
    '66666666000000000000000000000003',
    '66666666000000000000000000000004',
    '66666666000000000000000000000005',
    '66666666000000000000000000000006',
    '66666666000000000000000000000007',
    '66666666000000000000000000000008',
]


# init_data.sql


def gen_init_data():
    lines = []

    # experience_level
    lines.append(' experience_level')
    lines.append("INSERT INTO experience_level (id, name, level_number, description) VALUES")
    lines.append("    ('11111111000000000000000000000001', 'beginner',     1, 'Опыт походов не требуется'),")
    lines.append("    ('11111111000000000000000000000002', 'intermediate', 2, 'Требуется небольшой опыт походов'),")
    lines.append("    ('11111111000000000000000000000003', 'expert',       3, 'Требуется большой опыт походов')")
    lines.append("ON CONFLICT DO NOTHING;\n")

    # season
    lines.append(' season')
    lines.append("INSERT INTO season (id, name, start_date, end_date, extremality_influence) VALUES")
    lines.append("    ('22222222000000000000000000000001', 'spring', '20240301', '20240531', 1.2),")
    lines.append("    ('22222222000000000000000000000002', 'summer', '20240601', '20240831', 1.0),")
    lines.append("    ('22222222000000000000000000000003', 'autumn', '20240901', '20241130', 1.5),")
    lines.append("    ('22222222000000000000000000000004', 'winter', '20241201', '20250228', 2.0)")
    lines.append("ON CONFLICT DO NOTHING;\n")

    # route
    lines.append(' route')
    lines.append("INSERT INTO route (id, level_id, name, length_km, travel_type) VALUES")
    lines.append("    ('55555555000000000000000000000001', '11111111000000000000000000000001', 'Утренняя тропа',  5.5,  'hiking'),")
    lines.append("    ('55555555000000000000000000000002', '11111111000000000000000000000002', 'Речной сплав',    12.0, 'rafting'),")
    lines.append("    ('55555555000000000000000000000003', '11111111000000000000000000000003', 'Горный экстрим',  18.5, 'hiking'),")
    lines.append("    ('55555555000000000000000000000004', '11111111000000000000000000000002', 'Зимний маршрут',  9.0,  'snowmobile')")
    lines.append("ON CONFLICT DO NOTHING;\n")

    # route_point
    lines.append(' route_point')
    lines.append("INSERT INTO route_point (id, route_id, name, latitude, longitude, order_id, short_description, purpose) VALUES")
    lines.append("    ('66666666000000000000000000000001', '55555555000000000000000000000001', 'Перевал Фролова',    43.150000, 77.050000, 1, 'Главная точка перевала',          'pass'),")
    lines.append("    ('66666666000000000000000000000002', '55555555000000000000000000000001', 'Лесная поляна',      43.155000, 77.060000, 2, 'Место для привала',               'rest'),")
    lines.append("    ('66666666000000000000000000000003', '55555555000000000000000000000001', 'Смотровая площадка',43.162000, 77.072000, 3, 'Вид на долину',                   'excursion'),")
    lines.append("    ('66666666000000000000000000000004', '55555555000000000000000000000002', 'Верхняя стоянка',   43.200000, 77.100000, 1, 'Начало сплава',                   'rest'),")
    lines.append("    ('66666666000000000000000000000005', '55555555000000000000000000000002', 'Речной порог',      43.190000, 77.120000, 2, 'Опасный участок реки',            'pass'),")
    lines.append("    ('66666666000000000000000000000006', '55555555000000000000000000000003', 'База клуба',        43.140000, 77.040000, 1, 'Отправная точка',                 'rest'),")
    lines.append("    ('66666666000000000000000000000007', '55555555000000000000000000000003', 'Ночная стоянка',    43.170000, 77.080000, 2, 'Место для ночлега',               'overnight'),")
    lines.append("    ('66666666000000000000000000000008', '55555555000000000000000000000003', 'Вершина Фролова',   43.195000, 77.095000, 3, 'Конечная точка экстрим маршрута', 'pass')")
    lines.append("ON CONFLICT DO NOTHING;\n")

    # inventory
    lines.append(' inventory')
    lines.append("INSERT INTO inventory (id, name, type, size, weight_kg, volume_l, rental_cost, stock_quantity) VALUES")
    lines.append("    ('77777777000000000000000000000001', 'Рюкзак туристический 60л', 'equipment',  'large',  1.80, 60.0, 500.00,  10),")
    lines.append("    ('77777777000000000000000000000002', 'Палатка двухместная',      'equipment',  'large',  2.50, 15.0, 800.00,  5),")
    lines.append("    ('77777777000000000000000000000003', 'Спальный мешок',           'equipment',  'medium', 1.20, 8.0,  400.00,  15),")
    lines.append("    ('77777777000000000000000000000004', 'Каска защитная',           'safety',     'medium', 0.45, NULL, 200.00,  20),")
    lines.append("    ('77777777000000000000000000000005', 'Спасательный жилет',       'safety',     'medium', 0.80, NULL, 300.00,  12),")
    lines.append("    ('77777777000000000000000000000006', 'Термос 1л',                'small',      'small',  NULL, NULL, 100.00,  30),")
    lines.append("    ('77777777000000000000000000000007', 'Рафт 6местный',           'watercraft', 'large',  35.0, NULL, 2000.00, 3),")
    lines.append("    ('77777777000000000000000000000008', 'Альпинистская верёвка 50м','equipment',  'large',  3.50, NULL, 600.00,  8)")
    lines.append("ON CONFLICT DO NOTHING;\n")

    # transport
    lines.append(' transport')
    lines.append("INSERT INTO transport (id, name, kind, capacity, luggage_volume_l, cost, service_cost, ownership_type) VALUES")
    lines.append("    ('88888888000000000000000000000001', 'УАЗ Патриот №1',    'car',        7,  500.0, 15000.00, 3000.00, 'own'),")
    lines.append("    ('88888888000000000000000000000002', 'УАЗ Патриот №2',    'car',        7,  500.0, 15000.00, 3000.00, 'own'),")
    lines.append("    ('88888888000000000000000000000003', 'Снегоход Буран №1', 'snowmobile', 2,  100.0, 8000.00,  2000.00, 'own'),")
    lines.append("    ('88888888000000000000000000000004', 'Снегоход Буран №2', 'snowmobile', 2,  100.0, 8000.00,  2000.00, 'rented'),")
    lines.append("    ('88888888000000000000000000000005', 'Рафткатер',        'boat',       10, 200.0, 12000.00, 2500.00, 'own')")
    lines.append("ON CONFLICT DO NOTHING;\n")

    # route_season
    lines.append(' route_season')
    lines.append("INSERT INTO route_season (route_id, season_id, scenery, extremality, cost) VALUES")
    lines.append("    ('55555555000000000000000000000001', '22222222000000000000000000000001', 8, 2, 4500.00),")
    lines.append("    ('55555555000000000000000000000001', '22222222000000000000000000000002', 9, 2, 5000.00),")
    lines.append("    ('55555555000000000000000000000001', '22222222000000000000000000000003', 7, 3, 4000.00),")
    lines.append("    ('55555555000000000000000000000002', '22222222000000000000000000000002', 9, 7, 12000.00),")
    lines.append("    ('55555555000000000000000000000002', '22222222000000000000000000000001', 7, 5, 10000.00),")
    lines.append("    ('55555555000000000000000000000003', '22222222000000000000000000000002', 9, 9, 20000.00),")
    lines.append("    ('55555555000000000000000000000003', '22222222000000000000000000000003', 7, 8, 18000.00),")
    lines.append("    ('55555555000000000000000000000004', '22222222000000000000000000000004', 5, 7, 15000.00)")
    lines.append("ON CONFLICT DO NOTHING;\n")

    # route_point_season
    lines.append(' route_point_season')
    lines.append("INSERT INTO route_point_season (route_point_id, season_id, scenery, extremality) VALUES")
    lines.append("    ('66666666000000000000000000000001', '22222222000000000000000000000002', 9, 2),")
    lines.append("    ('66666666000000000000000000000001', '22222222000000000000000000000004', 4, 8),")
    lines.append("    ('66666666000000000000000000000002', '22222222000000000000000000000002', 9, 1),")
    lines.append("    ('66666666000000000000000000000003', '22222222000000000000000000000002', 9, 2),")
    lines.append("    ('66666666000000000000000000000005', '22222222000000000000000000000002', 7, 8),")
    lines.append("    ('66666666000000000000000000000007', '22222222000000000000000000000002', 8, 5),")
    lines.append("    ('66666666000000000000000000000008', '22222222000000000000000000000002', 9, 9)")
    lines.append("ON CONFLICT DO NOTHING;\n")

    return lines



# test_data.sql
def gen_guides(n=10):
    lines = []
    used_names = set()
    used_passports = set()
    ids = []

    for _ in range(n):
        gid = uid()
        ids.append(gid)
        level_id = random.choice(LEVEL_IDS[1:])

        while True:
            name = fake.last_name() + ' ' + fake.first_name() + ' ' + fake.middle_name()
            if name not in used_names:
                used_names.add(name)
                break

        while True:
            passport = fake.bothify(text='??#######', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ')
            if passport not in used_passports:
                used_passports.add(passport)
                break

        phone = fake.phone_number()[:20]
        age = random.randint(22, 55)
        hike_count = random.randint(0, 100)
        can_drive = sql_bool(random.choice([True, False]))
        can_raft = sql_bool(random.choice([True, False]))
        experience = fake.sentence(nb_words=6)

        lines.append(
            f"INSERT INTO guide (id, level_id, full_name, passport_data, phone, age, hike_count, can_drive, can_raft, experience) VALUES ("
            f"{sql_str(gid)}, {sql_str(level_id)}, {sql_str(name)}, {sql_str(passport)}, "
            f"{sql_str(phone)}, {age}, {hike_count}, {can_drive}, {can_raft}, {sql_str(experience)}) ON CONFLICT DO NOTHING;"
        )

    return lines, ids


def gen_tourists(n=30):
    lines = []
    used_names = set()
    used_passports = set()
    used_emails = set()
    ids = []

    for _ in range(n):
        tid = uid()
        ids.append(tid)
        level_id = random.choice(LEVEL_IDS)

        while True:
            name = fake.last_name() + ' ' + fake.first_name() + ' ' + fake.middle_name()
            if name not in used_names:
                used_names.add(name)
                break

        while True:
            passport = 'KZ' + str(random.randint(1000000, 9999999))
            if passport not in used_passports:
                used_passports.add(passport)
                break

        while True:
            email = fake.email()
            if email not in used_emails:
                used_emails.add(email)
                break

        gender = sql_str(random.choice(['M', 'F']))
        age = random.randint(16, 65)
        experience = fake.sentence(nb_words=5)

        lines.append(
            f"INSERT INTO tourist (id, level_id, full_name, passport_data, email, gender, age, experience) VALUES ("
            f"{sql_str(tid)}, {sql_str(level_id)}, {sql_str(name)}, {sql_str(passport)}, "
            f"{sql_str(email)}, {gender}, {age}, {sql_str(experience)}) ON CONFLICT DO NOTHING;"
        )

    return lines, ids


def gen_hikes(n=20, guide_ids=None, tourist_ids=None):
    hike_lines = []
    trail_lines = []
    tourist_hike_lines = []
    guide_hike_lines = []
    hike_inventory_lines = []
    hike_transport_lines = []

    statuses = ['planned', 'started', 'completed', 'cancelled']

    for _ in range(n):
        hid = uid()
        route_id = random.choice(ROUTE_IDS)
        start = rand_date(date(2024, 1, 1), date(2025, 6, 1))
        duration = random.randint(1, 7)
        end = start + timedelta(days=duration)
        status = random.choice(statuses)
        cost = round(random.uniform(3000, 30000), 2)

        hike_lines.append(
            f"INSERT INTO hike (id, route_id, start_date, end_date, status, cost) VALUES ("
            f"{sql_str(hid)}, {sql_str(route_id)}, {sql_str(start)}, {sql_str(end)}, {sql_str(status)}, {cost}) ON CONFLICT DO NOTHING;"
        )

        trail_lines.append(
            f"INSERT INTO trail_book (id, hike_id, start_date, end_date, status) VALUES ("
            f"{sql_str(uid())}, {sql_str(hid)}, {sql_str(start)}, {sql_str(end)}, {sql_str(status)}) ON CONFLICT DO NOTHING;"
        )

        selected_tourists = random.sample(tourist_ids, min(random.randint(2, 8), len(tourist_ids)))
        for t_id in selected_tourists:
            tourist_hike_lines.append(
                f"INSERT INTO tourist_hike (tourist_id, hike_id) VALUES ({sql_str(t_id)}, {sql_str(hid)}) ON CONFLICT DO NOTHING;"
            )

        num_guides = 2 if random.random() < 0.3 else 1
        selected_guides = random.sample(guide_ids, min(num_guides, len(guide_ids)))
        for i, g_id in enumerate(selected_guides):
            role = 'lead' if i == 0 else 'assistant'
            guide_hike_lines.append(
                f"INSERT INTO guide_hike (hike_id, guide_id, role) VALUES ({sql_str(hid)}, {sql_str(g_id)}, {sql_str(role)}) ON CONFLICT DO NOTHING;"
            )

        selected_inv = random.sample(INVENTORY_IDS, random.randint(2, 5))
        for inv_id in selected_inv:
            qty = random.randint(1, 5)
            hike_inventory_lines.append(
                f"INSERT INTO hike_inventory (hike_id, inventory_id, quantity) VALUES ({sql_str(hid)}, {sql_str(inv_id)}, {qty}) ON CONFLICT DO NOTHING;"
            )

        if random.random() < 0.7:
            selected_trans = random.sample(TRANSPORT_IDS, random.randint(1, 2))
            for tr_id in selected_trans:
                hike_transport_lines.append(
                    f"INSERT INTO hike_transport (hike_id, transport_id) VALUES ({sql_str(hid)}, {sql_str(tr_id)}) ON CONFLICT DO NOTHING;"
                )

    return hike_lines, trail_lines, tourist_hike_lines, guide_hike_lines, hike_inventory_lines, hike_transport_lines


# Main
def main():
    #  init_data.sql 
    init_lines = gen_init_data()
    with open('init_data.sql', 'w', encoding='utf8') as f:
        f.write(' INIT DATA\n\n')
        f.write('\n'.join(init_lines))
    print('init_data.sql — готово')

    #  test_data.sql 
    guide_lines, guide_ids = gen_guides(10)
    tourist_lines, tourist_ids = gen_tourists(30)
    (
        hike_lines, trail_lines,
        tourist_hike_lines, guide_hike_lines,
        hike_inventory_lines, hike_transport_lines
    ) = gen_hikes(20, guide_ids, tourist_ids)

    with open('test_data.sql', 'w', encoding='utf8') as f:
        f.write(' AUTOGENERATED TEST DATA\n\n')
        f.write(' guides\n')
        f.write('\n'.join(guide_lines) + '\n\n')
        f.write(' tourists\n')
        f.write('\n'.join(tourist_lines) + '\n\n')
        f.write(' hikes\n')
        f.write('\n'.join(hike_lines) + '\n\n')
        f.write(' trail_books\n')
        f.write('\n'.join(trail_lines) + '\n\n')
        f.write(' tourist_hike\n')
        f.write('\n'.join(tourist_hike_lines) + '\n\n')
        f.write(' guide_hike\n')
        f.write('\n'.join(guide_hike_lines) + '\n\n')
        f.write(' hike_inventory\n')
        f.write('\n'.join(hike_inventory_lines) + '\n\n')
        f.write(' hike_transport\n')
        f.write('\n'.join(hike_transport_lines) + '\n\n')

    print('test_data.sql — готово')
    print(f'  Гидов:        {len(guide_lines)}')
    print(f'  Туристов:     {len(tourist_lines)}')
    print(f'  Походов:      {len(hike_lines)}')
    print(f'  Походных книг:{len(trail_lines)}')
    print(f'  Участий:      {len(tourist_hike_lines)}')
    print(f'  Назначений:   {len(guide_hike_lines)}')
    print(f'  Инвентарь:    {len(hike_inventory_lines)}')
    print(f'  Транспорт:    {len(hike_transport_lines)}')


if __name__ == '__main__':
    main()