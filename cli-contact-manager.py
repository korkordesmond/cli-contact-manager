import json
import os
import re
from typing import Dict, Any, Tuple


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

    def _validate_email(self, email: str) -> bool:
        """Validate email format using regex."""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_pattern, email) is not None

    def _validate_phone(self, phone: str) -> bool:
        """Validate phone number - should be 10 digits or 12 digits with country code."""
        # Remove all non-digit characters
        digits_only = re.sub(r'\D', '', phone)

        # Check if it's exactly 10 digits (domestic) or 12 digits (with country code)
        if len(digits_only) == 10:
            return True
        elif len(digits_only) == 12:
            return True
        else:
            return False

    def _format_phone(self, phone: str) -> str:
        """Format phone number for consistent storage."""
        digits_only = re.sub(r'\D', '', phone)

        if len(digits_only) == 10:
            # Format as (XXX) XXX-XXXX
            return f"({digits_only[:3]}) {digits_only[3:6]}-{digits_only[6:]}"
        elif len(digits_only) == 12:
            # Format as +XX (XXX) XXX-XXXX
            return f"+{digits_only[:2]} ({digits_only[2:5]}) {digits_only[5:8]}-{digits_only[8:]}"
        return phone

    def add_contact(self, name: str, phone: str, email: str) -> str:
        """Add a new contact if it doesn't exist."""
        if name in self.contactbook:
            return f"⚠️ Contact '{name}' already exists!"

        # Validate email
        if not self._validate_email(email):
            return f"❌ Invalid email format! Please enter a valid email address."

        # Validate phone
        if not self._validate_phone(phone):
            return f"❌ Invalid phone number! Please enter 10 digits (domestic) or 12 digits (with country code)."

        # Format phone number
        formatted_phone = self._format_phone(phone)

        self.contactbook[name] = {"phone": formatted_phone, "email": email}
        self._save_contacts()
        return f"✅ {name} saved successfully!"

    def update_contact(self, name: str, phone: str = None, email: str = None) -> str:
        """Update an existing contact's details."""
        if name not in self.contactbook:
            return f"⚠️ Contact '{name}' not found!"

        # Validate phone if provided
        if phone and not self._validate_phone(phone):
            return f"❌ Invalid phone number! Please enter 10 digits (domestic) or 12 digits (with country code)."

        # Validate email if provided
        if email and not self._validate_email(email):
            return f"❌ Invalid email format! Please enter a valid email address."

        if phone:
            self.contactbook[name]["phone"] = self._format_phone(phone)
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


def get_contact_details() -> Tuple[str, str, str]:
    """Get contact details with input validation loop."""
    name = input("Enter name: ").strip()

    # Phone input with validation
    while True:
        phone = input("Enter phone number (10 digits domestic or 12 digits with country code): ").strip()
        digits_only = re.sub(r'\D', '', phone)
        if len(digits_only) in [10, 12]:
            break
        print(
            "❌ Invalid phone format! Use 10 digits (e.g., 1234567890) or 12 digits with country code (e.g., 911234567890)")

    # Email input with validation
    while True:
        email = input("Enter email: ").strip()
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(email_pattern, email):
            break
        print("❌ Invalid email format! Please enter a valid email address (e.g., user@example.com)")

    return name, phone, email


def get_updated_contact_details(current_phone: str, current_email: str) -> Tuple[str, str]:
    """Get updated contact details with validation."""
    print("Leave blank to keep current value")

    # Phone update
    while True:
        phone = input(f"New phone [{current_phone}]: ").strip()
        if not phone:  # Keep current value
            phone = None
            break
        digits_only = re.sub(r'\D', '', phone)
        if len(digits_only) in [10, 12]:
            break
        print("❌ Invalid phone format! Use 10 digits or 12 digits with country code")

    # Email update
    while True:
        email = input(f"New email [{current_email}]: ").strip()
        if not email:  # Keep current value
            email = None
            break
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(email_pattern, email):
            break
        print("❌ Invalid email format! Please enter a valid email address")

    return phone, email


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

            current_phone = manager.contactbook[name]['phone']
            current_email = manager.contactbook[name]['email']
            phone, email = get_updated_contact_details(current_phone, current_email)
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
    print("📝 Phone Format: 10 digits (domestic) or 12 digits (with country code)")
    print("📧 Email Format: Valid email address (e.g., user@example.com)")
    start()