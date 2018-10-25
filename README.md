[![Build Status](https://travis-ci.org/dizak/django-mothulity.svg?branch=master)](https://travis-ci.org/dizak/django-mothulity)

# mothulity - web interface

Web Interface and database/job scheduler for [mothulity](https://github.com/dizak/mothulity).

The main principle is to:
1. Present HTML front-end to the user which gathers submission data.
2. Run a separate sched.py script which takes care of reading what was gathered in the database, submits it to [SLURM](https://slurm.schedmd.com/) and watches the submitted process.

### Installation for Production (virtual environment is advised, as always)

1. ```pip install numpy```.

1. ```pip install -r requirements.txt```.

1. ```pip install django-mothulity-*.tar.gz``` - the project will most probably NOT be distributed.

1. ```django-admin startproject <name_of_project>```.

1. Add ```'django.contrib.sites',``` and ```'mothulity,'``` to ```<name_of_project>/settings.py INSTALLED_APPS```.

1. Add ```'localhost'``` and ```'<your.domain.com>'``` to ```<name_of_project>/settings.py ALLOWED_HOSTS```.

1. ```python manage.py tests```. You can continue if all the tests are passed.

1. ```python manage.py createsuperuser```

1. In the Admin Panel:

  - Add <your.domain.com> to Sites.

  - Add Path settings and Hpc settings. The default ones should be OK.

### Installation for Development


1. Clone ```dizak/django-mothulity```

1. Run ```pip install -r django-mothulity/requirements.txt```, virtual environment recommended.

1. Type ```django-admin startproject <name_of_project> django-mothulity``` - this will create a Django project **WITHIN** the the cloned repo. This is intended.

1. Add ```'django.contrib.sites',``` and ```mothulity.apps.MothulityConfig``` to ```<name_of_project>/<name_of_project>/settings.py INSTALLED_APPS``` list.

1. Add ```'localhost'``` and ```'<your.domain.com>'``` to ```<name_of_project>/settings.py ALLOWED_HOSTS```.

1. Add ```from django.conf.urls import include, url``` to ```<name_of_project>/<name_of_project>/urls.py```.

1. Add ```url(r"^mothulity/", include("mothulity.urls"))``` to ```<name_of_project>/<name_of_project>/urls.py```.

1. Run ```python manage.py makemigrations && python manage.py migrate```.

1. Run ```python manage.py test```.

1. In the Admin Panel:

  - Add <your.domain.com> to Sites.

  - Add Path settings and Hpc settings. The default ones should be OK.

1. Run ```python manage.py runserver```.

  - This starts the development HTTP server.

1. Run ```python sched.py <name_of_project>```

  - This starts the scheduler.

### Requirements

SSH keys exchanged with the computing cluster.
Working directory used by ```MEDIA_URL``` and ```HEADNODE_PREFIX_URL``` mounted on the web-server, eg
with ```sshfs```.
