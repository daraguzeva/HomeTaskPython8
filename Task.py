import csv
import pandas as pd
from reportlab.pdfgen import canvas
import qrcode


# Функция выбора опций
# Основная функция для работы с телефонным справочником
def choose_option():
    # Открыть файл с телефонным справочником
    with open('phonebook.csv', 'a+') as file:
        # Предложить пользователю выбрать действие
        while True:
            print('Выберите действие:')
            print('1. Добавить контакт')
            print('2. Удалить контакт')
            print('3. Изменить контакт')
            print('4. Найти контакт')
            print('5. Экспорт карточки контакта')
            print('6. Экспорт всего содержимого справочника')
            print('7. Выйти из программы')
            choice = input('Введите номер действия: ')

            # Выполнить выбранное действие
            if choice == '1':
                add_contact()
            elif choice == '2':
                delete_contact()
            elif choice == '3':
                edit_contact()
            elif choice == '4':
                search_contacts()
            elif choice == '5':
                export_contact_found_to_pdf()
            elif choice == '6':
                export_all_contacts_to_pdf()
            elif choice == '7':
                break
            else:
                print('Нет такой опции')


# Функция для добавления контакта
def add_contact():
    with open("phonebook.csv", "a") as file:
        columnNAMEs = ["NAME", "LASTNAME", "PHONE",
                       "EMAIL", "TELEGRAM", "ORGANIZATION NAME"]
        NAME = input("Введите имя: ").strip().upper()
        LASTNAME = input("Введите Фамилию: ").strip().upper()
        PHONE_number = input("Введите номер телефона: ").strip()
        EMAIL = input("Введите EMAIL: ")
        TELEGRAM_ID = input("Введите TELEGRAM_ID: ").strip()
        ORGANIZATION = input("Введите имя организации: ").strip().upper()
        writer = csv.DictWriter(file, columnNAMEs)
        writer.writerow({"NAME": NAME, "LASTNAME": LASTNAME, "PHONE": PHONE_number,
                        "EMAIL": EMAIL, "TELEGRAM": TELEGRAM_ID, "ORGANIZATION NAME": ORGANIZATION})
    print('Контакт добавлен!')


# Функция для поиска контакта (визитка)
def search_contacts():
    # считываем данные из CSV файла в DataFrame
    df = pd.read_csv('phonebook.csv')
    # запрашиваем у пользователя строку для поиска
    search_term = input("Поиск контакта: ")
    # фильтруем DataFrame по запросу пользователя
    filtered_df = df[df.apply(lambda row: search_term.lower() in row.astype(str).str.lower().str.cat(sep=' '), axis=1)]
    # выводим найденные данные в форме визитной карточки
    for index, row in filtered_df.iterrows():
        print('===============================')
        print('NAME:', row['NAME'])
        print('LASTNAME:', row['LASTNAME'])
        print('PHONE:', row['PHONE'])
        print("EMAIL:", row["EMAIL"])
        print("TELEGRAM:", row["TELEGRAM"])
        print("ORGANIZATION NAME:", row["ORGANIZATION NAME"])
        print('===============================')


# требует pip install qrcode
# требует pip install reportlab
def export_contact_found_to_pdf():
    # считываем данные из CSV файла в DataFrame
    df = pd.read_csv('phonebook.csv')

    # запрашиваем у пользователя строку для поиска
    search_term = input("Search: ")

    # фильтруем DataFrame по запросу пользователя
    filtered_df = df[df.apply(lambda row: search_term.lower(
    ) in row.astype(str).str.lower().str.cat(sep=' '), axis=1)]

    # создаем PDF-файл
    pdf_file = canvas.Canvas("Visit Card.pdf")
    y = 750  # начальная координата для вывода информации

    # выводим найденные данные в форме визитной карточки и добавляем QR-код с телеграм ай ди
    for index, row in filtered_df.iterrows():
        pdf_file.drawString(100, y, 'NAME: ' + str(row['NAME']))
        pdf_file.drawString(100, y-20, 'LASTNAME: ' + str(row['LASTNAME']))
        pdf_file.drawString(100, y-40, 'PHONE: ' + str(row['PHONE']))
        pdf_file.drawString(100, y-60, 'EMAIL: ' + str(row['EMAIL']))
        pdf_file.drawString(100, y-80, 'TELEGRAM: ' + str(row['TELEGRAM']))
        pdf_file.drawString(
            100, y-100, 'ORGANIZATION NAME: ' + str(row['ORGANIZATION NAME']))
# генерируем QR-код с телеграммом
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data('TELEGRAM.me/' + row['TELEGRAM'])
        qr.make(fit=True)
        img = qr.make_image(fill_color='black', back_color='white')
        img.save('qrcode.png')

        # добавляем QR-код в PDF
        pdf_file.drawImage('qrcode.png', 400, y-60, wIDth=100, height=100)

        y -= 150  # смещаем координату по y для следующего контакта

    pdf_file.save()


# требует pip install qrcode
# требует pip install reportlab
# требует pip install qrcode
# требует pip install reportlab
def export_all_contacts_to_pdf():
    # считываем данные из CSV файла в DataFrame
    df = pd.read_csv('phonebook.csv')

    # создаем PDF-файл
    pdf_file = canvas.Canvas("all_contacts.pdf")
    y = 750  # начальная координата для вывода информации

    # выводим данные в форме визитной карточки и добавляем QR-код с телеграмм
    for index, row in df.iterrows():
        pdf_file.drawString(100, y, 'NAME: ' + str(row['NAME']))
        pdf_file.drawString(100, y-20, 'LASTNAME: ' + str(row['LASTNAME']))
        pdf_file.drawString(100, y-40, 'PHONE: ' + str(row['PHONE']))
        pdf_file.drawString(100, y-60, 'EMAIL: ' + str(row['EMAIL']))
        pdf_file.drawString(100, y-80, 'TELEGRAM: ' + str(row['TELEGRAM']))
        pdf_file.drawString(
            100, y-100, 'ORGANIZATION NAME: ' + str(row['ORGANIZATION NAME']))
        y -= 150  # смещаем координату по y для следующего контакта

    pdf_file.save()


# Функция удаления контакта
def delete_contact():
    search_term = input("Поиск контакта: ")
    search = []
    with open("phonebook.csv", "r", newline='') as file:
        filereader = csv.DictReader(file)
        for row in filereader:
            search.append({"NAME": row["NAME"], "LASTNAME": row["LASTNAME"], "PHONE": row["PHONE"],
                          "EMAIL": row["EMAIL"], "TELEGRAM": row["TELEGRAM"], "ORGANIZATION NAME": row["ORGANIZATION NAME"]})
        matching_contacts = []
        for person in search:
            if any(search_term.lower() in value.lower() for value in person.values()):
                matching_contacts.append(person)
        if len(matching_contacts) == 0:
            print("Контактов с такими данными не найдено.")
            return
        print("Совпадающие контакты:")
        for i, contact in enumerate(matching_contacts):
            print(
                f"{i}: {contact['NAME']} {contact['LASTNAME']}, {contact['PHONE']}, {contact['EMAIL']}, {contact['TELEGRAM']}, {contact['ORGANIZATION NAME']}")
        index = int(input("Введите порядковый номер контакта для удаления: "))
        fieldNAMEs = ["NAME", "LASTNAME", "PHONE",
                      "EMAIL", "TELEGRAM", "ORGANIZATION NAME"]
        writer = csv.DictWriter(file, fieldNAMEs=fieldNAMEs)
        writer.writeheader()
        for person in search:
            if person not in matching_contacts or person != matching_contacts[index]:
                writer.writerow(person)
    print("Контакт удален.")


# Функция изменения контакта
def edit_contact():
    search_term = input("Поиск контакта: ")
    search_result = []
    with open("phonebook.csv", "r", newline='') as file:
        filereader = csv.DictReader(file)
        for row in filereader:
            search_result.append({"NAME": row["NAME"], "LASTNAME": row["LASTNAME"], "PHONE": row["PHONE"],
                                 "EMAIL": row["EMAIL"], "TELEGRAM": row["TELEGRAM"], "ORGANIZATION NAME": row["ORGANIZATION NAME"]})
        matching_contacts = []
        for contact in search_result:
            if any(search_term.lower() in value.lower() for value in contact.values()):
                matching_contacts.append(contact)
        if len(matching_contacts) == 0:
            print("Контактов с такими данными не найдено.")
            return
        print("Совпадающие контакты:")
        for i, contact in enumerate(matching_contacts):
            print(
                f"{i}: {contact['NAME']} {contact['LASTNAME']}, {contact['PHONE']}, {contact['EMAIL']}, {contact['TELEGRAM']}, {contact['ORGANIZATION NAME']}")
        index = int(input("Введите порядковый номер контакта для изменения: "))
        print(
            f"{matching_contacts[index]['NAME']} {matching_contacts[index]['LASTNAME']}")
        print(
            f"Изменение {matching_contacts[index]['NAME']} {matching_contacts[index]['LASTNAME']}...")
        print("Выберите поле, которое вы хотите отредактировать:")
        print("1. Номер телефона")
        print("2. EMAIL")
        print("3. TELEGRAM ID")
        print("4. Название организации")
        field_choice = input("Введите номер поля: ")
        if field_choice == "1":
            new_PHONE_number = input(
                f"Введите новый номер для {matching_contacts[index]['NAME']} {matching_contacts[index]['LASTNAME']}: ").strip()
            matching_contacts[index]["PHONE"] = new_PHONE_number
        elif field_choice == "2":
            new_EMAIL = input(
                f"Введите новый EMAIL для {matching_contacts[index]['NAME']} {matching_contacts[index]['LASTNAME']}: ").strip()
            matching_contacts[index]["EMAIL"] = new_EMAIL
        elif field_choice == "3":
            new_TELEGRAM_ID = input(
                f"Введите новый TELEGRAM ID для {matching_contacts[index]['NAME']} {matching_contacts[index]['LASTNAME']}: ").strip()
            matching_contacts[index]["TELEGRAM"] = new_TELEGRAM_ID
        elif field_choice == "4":
            new_ORGANIZATION = input(
                f"Введите наименование организации {matching_contacts[index]['NAME']} {matching_contacts[index]['LASTNAME']}: ").strip()
            matching_contacts[index]["ORGANIZATION NAME"] = new_ORGANIZATION
        else:
            print("Некорректный выбор.")
            return
        with open("phonebook.csv", "w", newline='') as file:
            writer = csv.DictWriter(file, fieldNAMEs=[
                                    "NAME", "LASTNAME", "PHONE", "EMAIL", "TELEGRAM", "ORGANIZATION NAME"])
            writer.writeheader()
            for contact in search_result:
                if contact in matching_contacts:
                    writer.writerow(contact)
                else:
                    writer.writerow(contact)
            print(
                f"Контакт {matching_contacts[index]['NAME']} {matching_contacts[index]['LASTNAME']} обновлен.")


choose_option()
