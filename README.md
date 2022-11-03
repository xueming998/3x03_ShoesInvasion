# 3x03_ShoesInvasion

## How to set up environment
1. Clone this repository into a desired folder.
2. Open cmd and cd to 3x03_ShoesInvasion folder.
3. Install virtual environment by `pip install virtualenv`, `virtualenv -p python3 venv`.
4. Activate the virtual environment by `venv\Script\activate`.
5. Install required libraries by `pip install -r requirements.txt`.
6. Run the server by doing `python manage.py runserver`.
7. It should run at 127.0.0.1:8000 by default, but use '127.0.0.1:8000/ShoesInvasionApp' to access the website.


## Setup Database
1. Install MySQL Workbench Community (https://dev.mysql.com/downloads/mysql/), may need MySQL Server as well.
2. Create a schema called 'shoesinvasion'.
3. Navigate to '3x03_ShoesInvasion/ShoesInvasion/settings.py'.
4. Find DATABASES and edit to USER, PASSWORD, HOST, PORT according to your setting.
5. In your terminal, CD to 3x03_ShoesInvasion and do ls command.
6. Verify there is a 'manage.py' file.
7. Run `python manage.py makemigrations ShoesInvasionApp` and `python manage.py migrate ShoesInvasionApp` and `python manage.py loaddata data.json`.
8. Under MySQL Workbench shoesinvasion schema, verify that all the tables is created.
