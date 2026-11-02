
🩸 Blood Bank Management System
A web-based Blood Bank Management System built with Python, Flask,
MySQL, HTML, and CSS. The application helps manage blood donors,
patients, blood stock, and blood requests through a simple web
interface.

Project type: BCA academic project
Repository: https://github.com/shinde-anand/blood-bank

✨ Features
User registration and login
Password hashing using Werkzeug (where configured in the
application)
Dashboard for a quick overview
Add and view blood donors
Add and view patients
Maintain blood-group stock
Create and track blood requests
Responsive pages with a blood-bank-themed interface
MySQL database integration
🧰 Tech Stack
Backend: Python, Flask
Database: MySQL / MariaDB
Frontend: HTML, CSS
Database connector: mysql-connector-python
Local development: VS Code, XAMPP, phpMyAdmin
📁 Project Structure
blood_bank_management/
├── app.py
├── database.py
├── requirements.txt
├── database/
│   └── blood_bank.sql
├── static/
│   ├── blood-bg.png
│   └── style.css
└── templates/
    ├── add_donor.html
    ├── add_patient.html
    ├── add_request.html
    ├── blood_requests.html
    ├── blood_stock.html
    ├── dashboard.html
    ├── donors.html
    ├── edit_donor.html
    ├── login.html
    ├── patients.html
    └── register.html
⚙️ Run Locally
1. Requirements
Install: - Python 3 - Git - XAMPP (for its MySQL/MariaDB service and
phpMyAdmin) - A web browser

2. Clone the repository
git clone https://github.com/shinde-anand/blood-bank.git
cd blood-bank
3. Create and activate a virtual environment
Windows PowerShell:

python -m venv .venv
.\.venv\Scripts\Activate.ps1
If PowerShell blocks activation, you can use Command Prompt:

.venv\Scripts\activate.bat
4. Install dependencies
python -m pip install -r requirements.txt
If the MySQL connector is not listed in requirements.txt, install it
with:

python -m pip install mysql-connector-python
For deployment, also install Gunicorn if it is not already listed:

python -m pip install gunicorn
Then update the dependency file:

python -m pip freeze > requirements.txt
Review the file before committing so that only project dependencies are
included.

5. Create the database
Open XAMPP Control Panel.
Start MySQL.
Open http://localhost/phpmyadmin.
Create the database name expected by database.py.
Select the database, open the Import tab, and import
database/blood_bank.sql.
Important: The database name and table/column names in the SQL
file must match the values and queries used by database.py and
app.py. If your SQL file already creates a database, follow that
file's instructions.

6. Configure database connection
Open database.py and configure the host, username, password, and
database name for your local MySQL setup. A typical local XAMPP
configuration may look like this:

import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="YOUR_DATABASE_NAME"
    )
Replace YOUR_DATABASE_NAME with the actual database name. If your
MySQL root account has a password, use it locally.

Security: Do not commit real database passwords or production
credentials to GitHub. Use environment variables for deployed services.

7. Run the application
python app.py
Open http://127.0.0.1:5000 in your browser.

🚀 Deployment Notes
The Flask application can be hosted as a Python web service on a
platform such as Render. The MySQL database must also be reachable from
the hosted app; a local XAMPP database on your computer is not
automatically accessible to the internet.

Typical Render web-service settings:

Build command: pip install -r requirements.txt
Start command: gunicorn app:app
Before deployment: 1. Add gunicorn to requirements.txt. 2. Update
database.py to read connection settings from environment variables. 3.
Provision a remote MySQL database and import database/blood_bank.sql.
4. Add database connection details and SECRET_KEY in the host's
environment-variable settings. 5. Test login, donor/patient forms, stock
updates, and blood requests on the deployed URL.

See the Render Flask deployment
guide, environment variables
guide, and
MySQL on Render guide.

🔐 Security and Data Disclaimer
Never publish database passwords, Flask secret keys, .env files,
or real donor/patient personal data.
Use a strong, unique secret key in production.
Use HTTPS and restrict database access to trusted services.
This is an academic project starter, not a certified medical or
blood-bank operations platform. Validate data, access controls,
backups, and operational requirements before real-world use.
Keep database backups and test recovery procedures.
🖼️ Screenshots
Add screenshots of the login page, dashboard, donors, blood stock, and
blood requests here. For example:

![Login Page](screenshots/login.png)
![Dashboard](screenshots/dashboard.png)
👨‍💻 Author
Anand Shinde

📄 License
No license has been specified yet. If you want others to reuse or modify
this project, choose and add an appropriate open-source license.

