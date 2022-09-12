# 3x03_ShoesInvasion

## How to set up environment
1. (Optional) You can choose to purge your pip of all previous installations.
2. Install Django with `pip install django` verify the installation by running `python -m django --version` in terminal.
3. Clone this repository into a desired folder.
4. Open your IDE.
5. Open new terminal and type in 'python manage.py runserver'
6. It should run at 127.0.0.1:8000 by default, but use '127.0.0.1:8000/ShoesInvasionApp' to access the website
7. '127.0.0.1:8000/admin' is the admin portal for Django
8. Do what is necessary for the grades!


## Setup Database
1. Install MySQL Workbench Community (https://dev.mysql.com/downloads/mysql/), may need MySQL Server as well.
2. Create a schema called 'shoesinvasion'
3. Navigate to '3x03_ShoesInvasion/ShoesInvasion/settings.py'
4. Find DATABASES and edit to USER, PASSWORD, HOST, PORT according to your setting
5. In your terminal, CD to 3x03_ShoesInvasion and do ls command
6. Verify there is a 'manage.py' file
7. Install mysqlclient and mysql-connector-python by `pip install mysqlclient` and `pip install mysql-connector-python`
8. Run `python manage.py makemigrations ShoesInvasionApp` and `python manage.py migrate`
9. Under MySQL Workbench shoesinvasion schema, verify that all 7 tables is created