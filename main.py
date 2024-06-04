import csv
import re
# читаем адресную книгу в формате CSV в список contacts_list
with open("phonebook_raw.csv", encoding="utf-8") as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)

# Собираем имена
for number, contact in enumerate(contacts_list):
  if contact[0] != 'lastname':
    z = 0
    while z != 2:
        contact_info = contact[z].split(' ')
        if len(contact_info) > 1:
            i = 0 + z
            for c in contact_info:
                contacts_list[number][i] = c
                i += 1
        z += 1

# Убираем дубликаты и собираем инфу в одну сущность
clear_contacts_list = []
for contact in contacts_list:
    for number, clear_contact in enumerate(clear_contacts_list):
        exist = False
        if contact[0] == clear_contact[0] and contact[1] == clear_contact[1]\
            and (contact[2] == clear_contact[2] or not clear_contact[2] or not contact[2]):
            i = 2
            while i != 7:
                if not clear_contact[i]:
                    clear_contacts_list[number][i] = contact[i]
                i += 1
            exist = True
            break
    if not clear_contacts_list or not exist:
        clear_contacts_list.append(contact)

# Форматируем телефоны
for number, contact in enumerate(clear_contacts_list):
    pattern = r"^(8|\+7)?(\D*?)(\d{3})(\D*?)(\d{3})(\D?)(\d{2})(\D?)(\d{2})(\D*)(\d*)(\)|)$"
    if 'доб.' in contact[5]:
        result = re.sub(pattern, r"+7(\3)\5-\7-\9 доб.\11", contact[5])
    else:
        result = re.sub(pattern, r"+7(\3)\5-\7-\9", contact[5])
    contact[5] = result

# код для записи файла в формате CSV
with open("phonebook.csv", "w", encoding="utf-8") as f:
  datawriter = csv.writer(f, delimiter=',')
  # Вместо contacts_list подставьте свой список
  datawriter.writerows(clear_contacts_list)