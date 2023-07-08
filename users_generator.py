import csv
from faker import Faker

fake = Faker()


def generate_random_user(row_id):
    user_id = row_id
    username = fake.user_name()
    birthday = fake.date_of_birth(minimum_age=18, maximum_age=70).strftime('%d/%m/%Y')
    sex = fake.random_element(["M", "F"])

    return [user_id, username, birthday, sex]


# Genera 18000 utenti casuali
users = [generate_random_user(row_id + 1) for row_id in range(18000)]

# Scrive i dati nel file CSV
with open('users.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["id", "username", "birthday", "sex"])  # Scrive l'intestazione delle colonne
    writer.writerows(users)

print("File CSV generato correttamente.")
