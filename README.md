django ERP
==========

**Django ERP** is an _open-source_, _user-oriented_, *ERP system* based on [Django](http://www.djangoproject.com) framework.

 * **Official website:** http://django-erp.github.io/django-erp/
 * **Development:** https://github.com/django-erp/django-erp/
 * **Issue tracker:** https://github.com/django-erp/django-erp/issues/
 * **Wiki:** https://github.com/django-erp/django-erp/wiki/

Pre-requisites
--------------

Make sure you have the following pre-requisites installed:

 * **python** >= 2.7 (required)
   http://www.python.org

 * **pytz** >= 2015.4 (required)
   http://pytz.sourceforge.net/

 * **django** >= 1.8.x (required)
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

2. Install all **pre-requisities** (better inside a [virtualenv]) using [pip]:

    `pip install -r requirements.txt`

3. Copy and rename **djangoerp/settings/base.py.tmpl** to  **djangoerp/settings/base.py**.
 
4. Edit the **djangoerp/settings/base.py** content.

5. Initialize the database and all applications:

    `python manage migrate`

6. Test the installation running the development web-server (http://localhost:8000 on your browser):

    `python manage runserver`

[virtualenv]: http://www.virtualenv.org/en/latest/    
[pip]: http://www.pip-installer.org/en/latest/
