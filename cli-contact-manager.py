import json
import os
from typing import Dict, Any


class ContactManager:
    def __init__(self):
        self.filename = "contactbook.json"
        self.contactbook = self._load_contacts()

    def _load_contacts(self) -> Dict[str, Dict[str, str]]:
        """Load contacts from JSON file or return empty dict if file doesn't exist."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as contacts:
                    return json.load(contacts)
            except (json.JSONDecodeError, FileNotFoundError):
                return {}
        return {}

    def _save_contacts(self) -> None:
        """Save contacts to JSON file."""
        with open(self.filename, 'w') as contacts:
            json.dump(self.contactbook, contacts, indent=4)

    def add_contact(self, name: str, phone: str, email: str) -> str:
        """Add a new contact if it doesn't exist."""
        if name in self.contactbook:
            return f"⚠️ Contact '{name}' already exists!"

        self.contactbook[name] = {"phone": phone, "email": email}
        self._save_contacts()
        return f"✅ {name} saved successfully!"

    def update_contact(self, name: str, phone: str = None, email: str = None) -> str:
        """Update an existing contact's details."""
        if name not in self.contactbook:
            return f"⚠️ Contact '{name}' not found!"

        if phone:
            self.contactbook[name]["phone"] = phone
        if email:
            self.contactbook[name]["email"] = email

        self._save_contacts()
        return f"✅ {name} updated successfully!"

    def search_contact(self, search_term: str) -> Dict[str, Dict[str, str]]:
        """Search for contacts by partial name match (case-insensitive)."""
        results = {
            name: details
            for name, details in self.contactbook.items()
            if search_term.lower() in name.lower()
        }
        return results if results else "No matching contacts found."

    def delete_contact(self, name: str) -> str:
        """Delete a contact by name."""
        if name not in self.contactbook:
            return f"⚠️ Contact '{name}' does not exist!"

        del self.contactbook[name]
        self._save_contacts()
        return f"✅ {name} deleted successfully!"

    def view_contacts(self) -> Dict[str, Dict[str, str]]:
        """Return all contacts."""
        return self.contactbook if self.contactbook else "No contacts found."


def display_menu():
    print("\n📞 Contact Manager Menu:")
    print("1. Add New Contact\t2. Update Contact\t"
          "3. Delete Contact\t4. Search Contact\t"
          "5. View All Contacts\t6. Exit")


def get_contact_details():
    name = input("Enter name: ").strip()
    phone = input("Enter phone number: ").strip()
    email = input("Enter email: ").strip()
    return name, phone, email


def start():
    manager = ContactManager()

    while True:
        display_menu()
        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":  # Add Contact
            name, phone, email = get_contact_details()
            print(manager.add_contact(name, phone, email))

        elif choice == "2":  # Update Contact
            name = input("Enter name of contact to update: ").strip()
            if name not in manager.contactbook:
                print(f"⚠️ Contact '{name}' not found!")
                continue

            print("Leave blank to keep current value")
            phone = input(f"New phone [{manager.contactbook[name]['phone']}]: ").strip()
            email = input(f"New email [{manager.contactbook[name]['email']}]: ").strip()

            phone = phone if phone else None
            email = email if email else None
            print(manager.update_contact(name, phone, email))

        elif choice == "3":  # Delete Contact
            name = input("Enter name of contact to delete: ").strip()
            print(manager.delete_contact(name))

        elif choice == "4":  # Search Contact
            search_term = input("Enter name or part of name to search: ").strip()
            results = manager.search_contact(search_term)
            if isinstance(results, str):
                print(results)
            else:
                print("\n🔍 Search Results:")
                for name, details in results.items():
                    print(f"{name}: Phone: {details['phone']}, Email: {details['email']}")

        elif choice == "5":  # View All Contacts
            contacts = manager.view_contacts()
            if isinstance(contacts, str):
                print(contacts)
            else:
                print("\n📒 All Contacts:")
                for name, details in contacts.items():
                    print(f"{name}: Phone: {details['phone']}, Email: {details['email']}")

        elif choice == "6":  # Exit
            print("👋 Goodbye!")
            break

        else:
            print("⚠️ Invalid choice. Please enter a number between 1-6.")


if __name__ == '__main__':
    print("🌟 Welcome to Contact Manager! 🌟")
    start()