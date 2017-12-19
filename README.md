# mothulity - web interface

Web Interface and database/job scheduler for [mothulity](https://github.com/dizak/mothulity).

The main principle is to:
1. Present HTML front-end to the user which gathers submission data.
2. Run a separate sched.py script which takes care of reading what was gathered in the database, submits it to [SLURM](https://slurm.schedmd.com/) and watches the submitted process.

### Installation

1. Create virtual env with:  ``` conda env create --file /path/to/mothulity.yaml ```

2. Type ```django-admin startproject <name_of_project>```.

3. Add ```mothulity.apps.MothulityConfig``` to <name_of_project>/<name_of_project>/settings.py.

4. Add  ```MEDIA_URL = os.path.join(BASE_DIR, "mothulity/upload/")``` and ```HEADNODE_PREFIX_URL = "/path/to/files/on/computing_cluster"```.

  - MEDIA_URL is where uploaded files are stored on the web-server.

  - HEADNODE_PREFIX_URL is where files are copied to the computing cluster.

  **EACH URL MUST HAVE TRAILING SLASH!**

5. Add ```from django.conf.urls import include``` to <name_of_project>/<name_of_project>/urls.py.

6. Add ```url(r"^mothulity/", include("mothulity.urls"))``` to <name_of_project>/<name_of_project>/urls.py.

7. ```git clone https://github.com/dizak/mothulity_django``` to <name_of_project> and rename it to ```mothulity```

9. Replace ```sys.path.append("/home/dizak/Software/django_site/")``` with ```sys.path.append("/home/dizak/Software/<name_of_project>/")```

10. Replace ```os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_site.settings")```
with ```os.environ.setdefault("DJANGO_SETTINGS_MODULE", "<name_of_project>.settings")```

8. Run ```python manage.py makemigrations && python manage.py migrate```.

9. Run ```tests python manage.py test mothulity```.

10. Run ```python manage.py runserver```.

### Requirements

SSH keys exchanged with the computing cluster.