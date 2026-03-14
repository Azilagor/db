import uuid
import random
from datetime import date, timedelta
from faker import Faker

fake = Faker('ru_RU')

# =============================================
# Helpers
# =============================================

def uid():
    return str(uuid.uuid4())

def rand_date(start: date, end: date) -> date:
    delta = (end - start).days
    return start + timedelta(days=random.randint(0, delta))

def sql_str(val):
    if val is None:
        return 'NULL'
    val = str(val).replace("'", "''")
    return f"'{val}'"

def sql_bool(val):
    return 'TRUE' if val else 'FALSE'

# =============================================
# Fixed IDs from init_data (не трогаем)
# =============================================

LEVEL_IDS = [
    '11111111-0000-0000-0000-000000000001',  # beginner
    '11111111-0000-0000-0000-000000000002',  # intermediate
    '11111111-0000-0000-0000-000000000003',  # expert
]

SEASON_IDS = [
    '22222222-0000-0000-0000-000000000001',  # spring
    '22222222-0000-0000-0000-000000000002',  # summer
    '22222222-0000-0000-0000-000000000003',  # autumn
    '22222222-0000-0000-0000-000000000004',  # winter
]

ROUTE_IDS = [
    '55555555-0000-0000-0000-000000000001',
    '55555555-0000-0000-0000-000000000002',
    '55555555-0000-0000-0000-000000000003',
    '55555555-0000-0000-0000-000000000004',
]

INVENTORY_IDS = [
    '77777777-0000-0000-0000-000000000001',
    '77777777-0000-0000-0000-000000000002',
    '77777777-0000-0000-0000-000000000003',
    '77777777-0000-0000-0000-000000000004',
    '77777777-0000-0000-0000-000000000005',
    '77777777-0000-0000-0000-000000000006',
    '77777777-0000-0000-0000-000000000007',
    '77777777-0000-0000-0000-000000000008',
]

TRANSPORT_IDS = [
    '88888888-0000-0000-0000-000000000001',
    '88888888-0000-0000-0000-000000000002',
    '88888888-0000-0000-0000-000000000003',
    '88888888-0000-0000-0000-000000000004',
    '88888888-0000-0000-0000-000000000005',
]

# =============================================
# Generators
# =============================================

def gen_guides(n=10):
    lines = []
    used_names = set()
    used_passports = set()
    ids = []

    for _ in range(n):
        gid = uid()
        ids.append(gid)
        level_id = random.choice(LEVEL_IDS[1:])  # guides are intermediate or expert

        # unique full_name
        while True:
            name = fake.last_name() + ' ' + fake.first_name() + ' ' + fake.middle_name()
            if name not in used_names:
                used_names.add(name)
                break

        # unique passport
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
            f"{sql_str(phone)}, {age}, {hike_count}, {can_drive}, {can_raft}, {sql_str(experience)});"
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
            f"{sql_str(email)}, {gender}, {age}, {sql_str(experience)});"
        )

    return lines, ids


def gen_hikes(n=20, guide_ids=None, tourist_ids=None):
    hike_lines = []
    trail_lines = []
    tourist_hike_lines = []
    guide_hike_lines = []
    hike_inventory_lines = []
    hike_transport_lines = []
    hike_ids = []

    statuses = ['planned', 'started', 'completed', 'cancelled']

    for _ in range(n):
        hid = uid()
        hike_ids.append(hid)
        route_id = random.choice(ROUTE_IDS)
        start = rand_date(date(2024, 1, 1), date(2025, 6, 1))
        duration = random.randint(1, 7)
        end = start + timedelta(days=duration)
        status = random.choice(statuses)
        cost = round(random.uniform(3000, 30000), 2)

        hike_lines.append(
            f"INSERT INTO hike (id, route_id, start_date, end_date, status, cost) VALUES ("
            f"{sql_str(hid)}, {sql_str(route_id)}, {sql_str(start)}, {sql_str(end)}, {sql_str(status)}, {cost});"
        )

        # trail_book (1:1)
        trail_lines.append(
            f"INSERT INTO trail_book (id, hike_id, start_date, end_date, status) VALUES ("
            f"{sql_str(uid())}, {sql_str(hid)}, {sql_str(start)}, {sql_str(end)}, {sql_str(status)});"
        )

        # tourist_hike — от 2 до 8 туристов
        selected_tourists = random.sample(tourist_ids, min(random.randint(2, 8), len(tourist_ids)))
        for t_id in selected_tourists:
            tourist_hike_lines.append(
                f"INSERT INTO tourist_hike (tourist_id, hike_id) VALUES ({sql_str(t_id)}, {sql_str(hid)});"
            )

        # guide_hike — 1 или 2 гида
        num_guides = 2 if random.random() < 0.3 else 1
        selected_guides = random.sample(guide_ids, min(num_guides, len(guide_ids)))
        for i, g_id in enumerate(selected_guides):
            role = 'lead' if i == 0 else 'assistant'
            guide_hike_lines.append(
                f"INSERT INTO guide_hike (hike_id, guide_id, role) VALUES ({sql_str(hid)}, {sql_str(g_id)}, {sql_str(role)});"
            )

        # hike_inventory — от 2 до 5 видов
        selected_inv = random.sample(INVENTORY_IDS, random.randint(2, 5))
        for inv_id in selected_inv:
            qty = random.randint(1, 5)
            hike_inventory_lines.append(
                f"INSERT INTO hike_inventory (hike_id, inventory_id, quantity) VALUES ({sql_str(hid)}, {sql_str(inv_id)}, {qty});"
            )

        # hike_transport — 0 или 1-2 транспорта
        if random.random() < 0.7:
            selected_trans = random.sample(TRANSPORT_IDS, random.randint(1, 2))
            for tr_id in selected_trans:
                hike_transport_lines.append(
                    f"INSERT INTO hike_transport (hike_id, transport_id) VALUES ({sql_str(hid)}, {sql_str(tr_id)});"
                )

    return hike_lines, trail_lines, tourist_hike_lines, guide_hike_lines, hike_inventory_lines, hike_transport_lines


# =============================================
# Main
# =============================================

def main():
    output_file = 'test_data.sql'

    guide_lines, guide_ids = gen_guides(10)
    tourist_lines, tourist_ids = gen_tourists(30)
    (
        hike_lines, trail_lines,
        tourist_hike_lines, guide_hike_lines,
        hike_inventory_lines, hike_transport_lines
    ) = gen_hikes(20, guide_ids, tourist_ids)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('-- AUTO-GENERATED TEST DATA\n\n')

        f.write('-- guides\n')
        f.write('\n'.join(guide_lines) + '\n\n')

        f.write('-- tourists\n')
        f.write('\n'.join(tourist_lines) + '\n\n')

        f.write('-- hikes\n')
        f.write('\n'.join(hike_lines) + '\n\n')

        f.write('-- trail_books\n')
        f.write('\n'.join(trail_lines) + '\n\n')

        f.write('-- tourist_hike\n')
        f.write('\n'.join(tourist_hike_lines) + '\n\n')

        f.write('-- guide_hike\n')
        f.write('\n'.join(guide_hike_lines) + '\n\n')

        f.write('-- hike_inventory\n')
        f.write('\n'.join(hike_inventory_lines) + '\n\n')

        f.write('-- hike_transport\n')
        f.write('\n'.join(hike_transport_lines) + '\n\n')

    print(f'Готово! Файл сохранён: {output_file}')
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