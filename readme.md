neuroner project
=======================

This project is based on [Wagtail CMS](https://github.com/wagtail/wagtail).

**Document contents**

- [Installation](#installation)
- [Next steps](#next-steps)
- [Other notes](#other-notes)

# Installation


- [Docker](#setup-with-docker)
- [Miniconda](#setup-with-virtualenv)
- [Heroku](#deploy-to-heroku)


#### Installation
Once you've installed the necessary dependencies run the following commands:

```bash
git clone https://github.com/wagtail/bakerydemo.git
cd bakerydemo
vagrant up
vagrant ssh
# then, within the SSH session:
./manage.py runserver 0.0.0.0:8000
```

The demo site will now be accessible at [http://localhost:8000/](http://localhost:8000/) and the Wagtail admin
interface at [http://localhost:8000/admin/](http://localhost:8000/admin/).

Log into the admin with the credentials ``admin / changeme``.

Use `Ctrl+c` to stop the local server.

Setup with Docker
-----------------

#### Dependencies
* [Docker](https://docs.docker.com/engine/installation/)
* [Docker Compose](https://docs.docker.com/compose/install/)

### Installation
Run the following commands:

```bash
git clone https://github.com/wagtail/bakerydemo.git
cd bakerydemo
docker-compose up --build -d
docker-compose run app /venv/bin/python manage.py load_initial_data
docker-compose up
```

The demo site will now be accessible at [http://localhost:8000/](http://localhost:8000/) and the Wagtail admin
interface at [http://localhost:8000/admin/](http://localhost:8000/admin/).

Log into the admin with the credentials ``admin / changeme``.

**Important:** This `docker-compose.yml` is configured for local testing only, and is _not_ intended for production use.

### Debugging
To tail the logs from the Docker containers in realtime, run:

```bash
docker-compose logs -f
```

Setup with Miniconda
---------------------
You can run the Wagtail demo locally without setting up Docker and simply use Miniconda env.

#### Dependencies
* Python 3.6 or 3.8
* [Miniconda](https://virtualenv.pypa.io/en/stable/installation/)

### Installation

With [miniconda](https://virtualenvwrapper.readthedocs.io/en/latest/)
installed, run:

    conda create --name ...
    python --version

Confirm that this is showing a compatible version of Python 3.x. If not, and you have multiple versions of Python installed on your system, you may need to specify the appropriate version when creating the virtualenv:

    deactivate
    rmvirtualenv wagtailbakerydemo
    mkvirtualenv wagtailbakerydemo --python=python3.6
    python --version

Now we're ready to set up the bakery demo project itself:

    cd ~/dev [or your preferred dev directory]
    git clone https://github.com/wagtail/bakerydemo.git
    cd bakerydemo
    pip install -r requirements/base.txt

Next, we'll set up our local environment variables. We use [django-dotenv](https://github.com/jpadilla/django-dotenv)
to help with this. It reads environment variables located in a file name `.env` in the top level directory of the project. The only variable we need to start is `DJANGO_SETTINGS_MODULE`:

    $ cp bakerydemo/settings/local.py.example bakerydemo/settings/local.py
    $ echo "DJANGO_SETTINGS_MODULE=bakerydemo.settings.local" > .env

To set up your database and load initial data, run the following commands:

    ./manage.py migrate
    ./manage.py load_initial_data
    ./manage.py runserver

Log into the admin with the credentials ``admin / changeme``.

# Next steps


### Preparing this archive for distribution

If you change content or images in this repo and need to prepare a new fixture file for export, do the following on a branch:

`./manage.py dumpdata --natural-foreign --indent 2 -e auth.permission -e contenttypes -e wagtailcore.GroupCollectionPermission -e wagtailimages.filter -e wagtailcore.pagerevision -e wagtailimages.rendition  -e sessions > bakerydemo/base/fixtures/bakerydemo.json`

Please optimize any included images to 1200px wide with JPEG compression at 60%. Note that `media/images` is ignored in the repo by `.gitignore` but `media/original_images` is not. Wagtail's local image "renditions" are excluded in the fixture recipe above.

Make a pull request to https://github.com/wagtail/bakerydemo

# Other notes

### Note on demo search

Because we can't (easily) use ElasticSearch for this demo, we use wagtail's native DB search.
However, native DB search can't search specific fields in our models on a generalized `Page` query.
So for demo purposes ONLY, we hard-code the model names we want to search into `search.views`, which is
not ideal. In production, use ElasticSearch and a simplified search query, per
[http://docs.wagtail.io/en/v1.13.1/topics/search/searching.html](http://docs.wagtail.io/en/v1.13.1/topics/search/searching.html).

### Sending email from the contact form

The following setting in `base.py` and `production.py` ensures that live email is not sent by the demo contact form.

`EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'`

In production on your own site, you'll need to change this to:

`EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'`

and configure [SMTP settings](https://docs.djangoproject.com/en/1.10/topics/email/#smtp-backend) appropriate for your email provider.

### Ownership of demo content

All content in the demo is public domain. Textual content in this project is either sourced from Wikipedia or is lorem ipsum. All images are from either Wikimedia Commons or other copyright-free sources.


### How to make wagtail to resize images on uploading (to save space on server)

- login to server
- activate env(miniconda) on server
- `pip install django-imagekit`
- `sudo nano /home/habrauser/miniconda3/envs/env38_fawbesturn/lib/python3.8/site-packages/wagtail/project_template/project_name/settings/base.py`
  here we need to add 'imagekit' to INSTALLED_APPS
  
- `sudo nano /home/sammy/miniconda3/envs/env38_django/lib/python3.8/site-packages/wagtail/images/models.py `
  add 
     from imagekit.models import ImageSpecField, ProcessedImageField
     from imagekit.processors import ResizeToFill, Adjust, ResizeToFit
     
  modify AbstractImage:
  
    `file = ProcessedImageField(
        verbose_name=_('file'), 
        upload_to=get_upload_to, 
        width_field='width', 
        height_field='height',
        ``
        processors = [
                     ResizeToFit(1600, 500,
                                 # upscale=False
                                 ),
                 ],
        format='JPEG',
        options={'quality': 60},
    )`
    
- `python manage.py makemigrations`
- `python manage.py migrate`
  
  
  
  
  
### Use wagtail_hooks to customize admin menu items:

You can use Wagtail's Hooks functionality, particularly the construct_main_menu hook:

Create a wagtail_hooks.py file in your corresponding application, with something like the following (from the Wagtail Docs):

`from wagtail.core import hooks`

@hooks.register('construct_main_menu')
def hide_explorer_menu_item_from_frank(request, menu_items):
  if request.user.username == 'frank':
    `menu_items[:] = [item for item in menu_items if item.name != 'explorer']

  