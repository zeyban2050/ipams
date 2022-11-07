# IPAMS

**Intellectual Property Asset Management System** -   is a tool for managing and organizing intellectual properties which are an essential part to the institution.

**Frameworks and tools**

-   Framework: Django >= 3.0.7 Language: Python 3.8.7^
-   Database: Mysql/Sqlite3(Default)
-   Deployment History:
-   Heroku, GCP (March 16)


![image](https://user-images.githubusercontent.com/53965169/200242362-33b96d3d-b750-4ea7-b7a9-6a7e3886a91b.png)

**Dependencies**

-   After cloning, and creating a branch for IPAMS, refer to requirements.txt.

**Source Code**

-   [https://github.com/jurydelrama/ipamsojt](https://github.com/jurydelrama/ipamsojt)
    -   Clone this repository via Github Desktop or CLI (follow instructions on the github upon cloning).
    -   After cloning, create a branch. Format: git branch -c lastname-branch.
    -   Execute the command, git checkout lastname-branch to be redirected to the created branch
    -   Execute the command, git push origin HEAD to save your branch to the github repository.
    -   For requirements.txt installation, and database connection, refer to the link above.

# **Design and Architecture**
**MVT Architecture**


![MVT Architecture drawio](https://user-images.githubusercontent.com/53965169/200243046-0a598498-8e70-4c4e-b598-3065ad011598.png)


-   Django MVT Structure (Model-View-Template)The image above shows the MVT Structure. In the client side, the client can access templates through IPAMS' user inputs to be received in the views to apply its functionalities, but auxfunctions, and decorators will also be applied within the views for additional functionality to update the data within the model.
   -   In the server side, the model will send data to the views (auxfunctions, and decorators may apply if functions within the views refers to auxfunctions and decorators) where the views will apply functionalities to be displayed towards the template or client.
   


## Database
**-FOR WINDOWS** 
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
