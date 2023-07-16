import csv
from faker import Faker
import datetime

fake = Faker()


def generate_random_user(row_id):
    first_name = fake.first_name()
    last_name = fake.last_name()
    email_domain = fake.free_email_domain()
    email = f"{first_name.lower()}.{last_name.lower()}@{email_domain}"
    birthdate = fake.date_of_birth(minimum_age=18, maximum_age=70).strftime('%Y-%m-%d')

    return [row_id, email, first_name, last_name, birthdate]

def generate_accounts():
    users = [generate_random_user(row_id + 1) for row_id in range(8)]

    with open('../accounts.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["id", "email", "name", "surname", "birthdate"])
        writer.writerows(users)
def read_account_from_csv():
    filepath = '../accounts.csv'
    accounts = []
    with open(filepath, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            account = {
                'id': int(row['id']),
                'email': row['email'],
                'name': row['name'],
                'surname': row['surname'],
                'birthdate': row['birthdate'],
            }
            accounts.append(account)
    return accounts

if __name__ == "__main__":
    generate_accounts()
    print(read_account_from_csv())