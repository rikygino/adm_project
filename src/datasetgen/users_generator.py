import csv
from faker import Faker

fake = Faker()


def generate_random_user(row_id):
    user_id = row_id
    username = fake.user_name()
    birthday = fake.date_of_birth(minimum_age=18, maximum_age=70).strftime('%Y-%m-%d')
    return [user_id,username,birthday]

def generate_users():
    users = [(generate_random_user(row_id + 1)) for row_id in range(20)]

    with open('../users.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["id", "username", "birthdate"])
        writer.writerows(users)

def read_users_from_csv():
    filename = '../users.csv'
    users = []
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            user = {
                'id': int(row['id']),
                'username': row['username'],
                'birthdate': row['birthdate']
            }
            users.append(user)
    return users

if __name__ == "__main__":
    generate_users()
    print(read_users_from_csv())


