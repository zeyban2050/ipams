-for windows


## Database
Install [XAMPP](https://www.apachefriends.org/download.html) for the database.
After installing XAMPP, do the following tasks:
* Before Starting MySQL, click the "Config" button and choose "my.ini".
* Under [mysqld], add the following line, typically at line 45:
```text
skip-grant-tables
```
* Save the file.
* Start MySQL and in XAMPP.
* Create a database named "ipamsdjango" without quotes

## Development
* install python from this site: https://www.python.org/downloads/windows/
* install the package manager [pip](https://pip.pypa.io/en/stable/) to install the required modules for this app.
* install required modules from requirements.txt using this command in cmd: pip install -r requirements.txt
 
## Server
In order to run the application in Django, do the following in your command prompt:
```bash
python manage.py migrate
python manage.py runserver