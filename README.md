# 📞 Contact Manager (Python)

A terminal-based contact management system that lets users store, update, search, and delete contacts with persistent JSON storage.

---

## ✅ Features

- 👥 **Contact Management**  
  - Add new contacts (name, phone, email)  
  - Update existing contact information  
  - Delete contacts permanently  

- 🔍 **Smart Search**  
  - Partial name matching (case-insensitive)  
  - View all matching results at once  

- 💾 **Persistent Storage**  
  - Automatically saves contacts to `contactbook.json`  

- 🖥️ **User-Friendly Interface**  
  - Clear menu prompts  
  - Success/error feedback with emojis  

---

## 🧠 How It Works

1. Contacts are stored in a dictionary with names as keys  
2. All data persists between sessions using JSON  
3. Users interact via simple terminal prompts  
4. Partial search matches make finding contacts effortless  

---

## 🖥️ Usage

### 1. Clone the repository or download the script
Open your terminal and run:
```bash
git clone https://github.com/korkordesmond/cli-contact-manager.git
cd cli-contact-manager
python cli-contact-manager.py