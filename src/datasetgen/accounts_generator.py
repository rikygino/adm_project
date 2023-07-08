import csv
from faker import Faker
import datetime

fake = Faker()


def generate_random_user(row_id):
    first_name = fake.first_name()
    last_name = fake.last_name()
    email_domain = fake.free_email_domain()
    email = f"{first_name.lower()}.{last_name.lower()}@{email_domain}"
    birthdate = fake.date_of_birth(minimum_age=18, maximum_age=70).strftime('%d/%m/%Y')
    sex = fake.random_element(["M", "F"])

    return [row_id, email, first_name, last_name, birthdate, sex]


# Genera 10.000 utenti casuali
users = [generate_random_user(row_id + 1) for row_id in range(10000)]

# Scrive i dati nel file CSV
with open('../accounts.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["id", "email", "name", "surname", "birthdate", "sex"])  # Scrive l'intestazione delle colonne
    writer.writerows(users)

print("File CSV generato correttamente.")
