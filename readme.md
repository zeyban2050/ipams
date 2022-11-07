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
```

# Database Migration

**Database Migration from dbsqlite3 to MySQL Step-by-step guide**

> **Step1.** Delete all migration history from **app/migrations** except 
     __init__.py.
> **Step2.** In the **settings.py** change the dbsqlite3 connection in the **DATABASES** and change configuration for MySQL.
``` bash 
DATABASES = {

    'default': {

        'ENGINE': 'django.db.backends.mysql',

        'NAME': 'ipamsdjango',

        'OPTIONS': {

    'read_default_file': os.path.join(BASE_DIR, 'my.ini'),

    'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",

        },

    }

}

```
>In the terminal, execute **python [manage.py](http://manage.py) makemigrations records** 
> In the terminal, execute **python [manage.py](http://manage.py/) makemigrations notifications**
>  In the terminal, execute **python [manage.py](http://manage.py/) makemigrations accounts**
    Execute **python [manage.py](http://manage.py) migrate --run-syncdb**

Observe line 67. In the decode() method, add "UTF-16". Follow the link found below the [json.py](http://json.py) tab to open [json.py](http://json.py).

>C:\Users\User\AppData\Roaming\Python\Python310\site-packages\django\core\serializers

```bash 
def Deserializer(stream_or_string, **options):

    """Deserialize a stream or string of JSON data."""

    if not isinstance(stream_or_string, (bytes, str)):

        stream_or_string = stream_or_string.read()

    if isinstance(stream_or_string, bytes):

        stream_or_string = stream_or_string.decode("UTF-16")

    try:

        objects = json.loads(stream_or_string)

        yield from PythonDeserializer(objects, **options)

    except (GeneratorExit, DeserializationError):

        raise

    except Exception as exc:

        raise DeserializationError() from exc
```
>In the terminal, execute **python [manage.py](http://manage.py/) loaddata datadump.json**
>In the terminal, execute**python [manage.py](http://manage.py) runserver**

**app names**
notifications
records
accounts
