from django.contrib.auth.decorators import permission_requiredfrom django.db.models.expressions import resultfrom App.models import Machineryfrom rest_framework.decorators import permission_classes Web-Application-Development

Factory Machinery Status & Repair Tracking 
System

# Documentation
## Requirements


## Deployment

Getting project 
```bash
  git clone https://github.com/jahz2323/WebApplicationDevelopment_GroupF.git
```
Creating virtual env , im using {environment} 
```bash
  python -m venv environment
  environment\Scripts\activate
```

## Setting dependencies, sample Users/Datas and launching project

### With Docker

Install [DockerDesktop](https://docs.docker.com/desktop/), then run
```bash
    docker-compose up -d --build
```

It installs for you everything you need, in order, which you would
had done manually [Without Docker](#without-docker)

1. It installs every dependencies in the file [requirement.txt](requirements.txt).
2. It creates all group roles and assign their permissions.
3. It loads the sample data in the folder [fixtures](App/fixtures).
NB. **_"admin"_** user password is **_"admin"_**, every other sample users has **_"project123"_**

### Without Docker

#### Install dependencies 
```bash
    pip install --no-cache-dir -r requirements.txt
```

#### Create group roles and assign their permissions

```bash
    python manage.py setup_groups
```

#### Run migrations, add samples and run server

```bash
    python manage.py migrate
    
    python manage.py loaddata App/fixtures/collections.json
    python manage.py loaddata App/fixtures/users.json
    python manage.py loaddata App/fixtures/machineries.json
    python manage.py loaddata App/fixtures/machineryfaults.json
    
    python manage.py runserver
```

**_loaddata_** might duplicate not unique samples like warnings if run multiple time (same [With Docker](#with-docker))

#### Open and Navigate to 
http://127.0.0.1:8000

# Create functions with permissions

Because all the groups and permissions are already set, you'll just have to check in the [setup_groups.py](App/management/commands/setup_groups.py) which of the permission you want to be required for the function 

then create the function like this:

if the permission code is "view_machinery"

```python
    @permission_required(App.view_machinery)
    def any_fct(any_args):
        your_fct_content
        return your_result
```
