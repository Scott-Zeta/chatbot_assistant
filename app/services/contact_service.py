from datetime import datetime
import json
import os

class ContactService:
    def __init__(self):
        self.storage_dir = "data/contacts"
        self.contacts_file = os.path.join(self.storage_dir, "contacts.json")
        self._ensure_storage_exists()
    
    def _ensure_storage_exists(self):
        """Ensure the storage directory and contacts file exist"""
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir)
        if not os.path.exists(self.contacts_file):
            with open(self.contacts_file, 'w') as f:
                json.dump([], f)
    
    def _read_contacts(self) -> list:
        """Read all contacts from the JSON file"""
        try:
            with open(self.contacts_file, 'r') as f:
                return json.load(f)
        except Exception:
            return []
    
    def _write_contacts(self, contacts: list) -> bool:
        """Write contacts to the JSON file"""
        try:
            with open(self.contacts_file, 'w') as f:
                json.dump(contacts, f, indent=2)
            return True
        except Exception as e:
            print(f"Error writing contacts: {str(e)}")
            return False
    
    def save_contact(self, contact_data: dict) -> bool:
        """Append new contact information to the contacts file"""
        try:
            contacts = self._read_contacts()
            
            # Add timestamp to contact data
            contact_data.update({
                "id": len(contacts) + 1,
                "submission_time": datetime.now().isoformat()
            })
            
            contacts.append(contact_data)
            return self._write_contacts(contacts)
            
        except Exception as e:
            print(f"Error saving contact: {str(e)}")
            return False
    
    def get_contacts(self, limit: int = 100) -> list:
        """Retrieve recent contact submissions"""
        try:
            contacts = self._read_contacts()
            return contacts[-limit:] if limit else contacts
        except Exception as e:
            print(f"Error retrieving contacts: {str(e)}")
            return []