import csv
from datetime import datetime

FILENAME = "clients.csv"

def add_client():
    print("\n📇 Add New Client")
    name = input("Client Name: ")
    contact = input("Contact Number: ")
    email = input("Email Address: ")
    purpose = input("Purpose of Engagement: ")
    niche = input("Client Niche/Industry: ")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(FILENAME, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, name, contact, email, purpose, niche])
    print("✅ Client added successfully!")

def view_clients():
    print("\n📋 Client List:")
    try:
        with open(FILENAME, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                print(row)
    except FileNotFoundError:
        print("No client records found.")

def main():
    while True:
        print("\n1. Add Client\n2. View Clients\n3. Exit")
        choice = input("Choose an option: ")
        if choice == '1':
            add_client()
        elif choice == '2':
            view_clients()
        elif choice == '3':
            print("👋 Exiting CRM. See you next time!")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()