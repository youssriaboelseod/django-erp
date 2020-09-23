![django ERP](http://django-erp.github.io/website/static/logo.png "django ERP")
===============================================================================

[![Build Status](https://travis-ci.org/django-erp/django-erp.svg?branch=develop)](https://travis-ci.org/django-erp/django-erp)

**Django ERP** is an _open-source_, _user-oriented_, *ERP system* based on [Django](http://www.djangoproject.com) framework.

 * **Official website:** http://django-erp.github.io/website/
 * **Development:** https://github.com/django-erp/django-erp/
 * **Issue tracker:** https://github.com/django-erp/django-erp/issues/
 * **Wiki:** https://github.com/django-erp/django-erp/wiki/

Pre-requisites
--------------

Make sure you have the following pre-requisites installed:

 * **python** >= 3.5 (required)
   http://www.python.org

 * **pytz** >= 2020.1 (required)
   http://pytz.sourceforge.net/

 * **django** >= 3.1 (required)
   http://www.djangoproject.com

 * **apache2** (optional)
   http://httpd.apache.org

 * **mod_wsgi** (optional)
   http://code.google.com/p/modwsgi

Installation
------------

1. Checkout sources from the GIT repository:

    `git clone https://github.com/django-erp/django-erp.git`
    
   It will clone the entire repository in a folder called **django-erp**:

    `cd django-erp`

    `python -m venv env`

    `source env-django-erp/Scripts/activate ` or `source ../env-django-erp/Scripts/activate ` (if the virtualenv outside the project file )

3. Copy and rename **djangoerp/settings/base.py.tmpl** to  **djangoerp/settings/base.py**.
 
4. Edit the **djangoerp/settings/base.py** content.

5. Initialize the database and all applications:

    `python manage.py migrate`

    `python manage.py makemigrations`  if you create modifications in models or create another module ( don't forget request pull it for        django-erp development after stablitiy stage)

6. Test the installation running the development web-server (http://localhost:8000 on your browser):

    `python manage runserver`

7. create supper user for manage your erp system and you can add more users

    `python manage.py createsuperuser`

[virtualenv]: http://www.virtualenv.org/en/latest/    
[pip]: http://www.pip-installer.org/en/latest/


Compile documentation 
----------------------

1. Install required packages 

    `pip install sphinx sphinx-autobuild`

2. Change to docs directory

    `cd docs`

3. Run builder 

    `make html`

