# mothulity - web interface

Web Interface and database/job scheduler for [mothulity](https://github.com/dizak/mothulity).

The main principle is to:
1. Present HTML front-end to the user which gather submission data.
2. Run a separate sched.py script which takes care of reading what was gathered in the database
and submit it to [SLURM](https://slurm.schedmd.com/) and watch the submitted process.

### Installation

1. Create virtual env with:  ``` conda env create --file /path/to/mothulity.yaml ```

2. Create directory_for_django_project.

3. Add ```mothulity.apps.MothulityConfig``` to directory_for_django_project/django_project/settings.py.

4. Add ```from django.conf.urls import include``` to directory_for_django_project/django_project/urls.py.

5. Add ```url(r"^mothulity/", include("mothulity.urls"))``` to directory_for_django_project/django_project/urls.py.

6. ```git clone https://github.com/dizak/mothulity_django``` to directory_for_django_project/django_project.

7. Run ```python manage.py makemigrations && python manage.py migrate```.

8. Run ```tests python manage.py test mothulity```.

9. Run python manage.py runserver.

### Requirements

SSH keys exchanged with the computing cluster.
