## login to google using allauth package

### install package

    - from --> https://django-allauth.readthedocs.io/en/latest/installation.html
    - set this variable to setting.py
            INSTALLED_APPS = [
                "django.contrib.sites",
                "allauth",
                "allauth.account",
                "allauth.socialaccount",
                "allauth.socialaccount.providers.google",
                ]
            SITE_ID = 2  # that changes according to your site http://127.0.0.1:8000 in admin panel
            LOGIN_REDIRECT_URL = "/"
            # for manual configurations:
            SOCIALACCOUNT_PROVIDERS = {
                "google": {
                    "SCOPE": [
                        "profile",
                        "email",
                    ],
                    "AUTH_PARAMS": {"access_type": "online"},
                }
            }
            AUTHENTICATION_BACKENDS = [
                "django.contrib.auth.backends.ModelBackend",
                "allauth.account.auth_backends.AuthenticationBackend",
            ]

    - set the url.py
        path("accounts/", include("allauth.urls")),

    - migrate

### google configurations in google_api.com

    from --> https://console.cloud.google.com/

    - create_project

![create_proj](https://github.com/PROFabdalla/my_city/blob/main/data/images/create_proj.jpg)
change project_name
click create

    - from sidebar choose "OAuth consent screen"
        choose:
            External - create
        change:
            Application Name
        click save

    - from sidebar choose "Credentials"

![clint_id](https://github.com/PROFabdalla/my_city/blob/main/data/images/Inkedclint_id.jpg)

        choose: application type
            web application

        change: name
        Authorized JavaScript Origins:
            http://127.0.0.1:8000/

        Authorized redirect url:
            http://127.0.0.1:8000/accounts/google/login/callback/
        click create

### admin panel db creation

    sites:
        http://127.0.0.1:8000/

    # add google project api we created in Credentials bar
    Social applications:
        provider:       google
        name:           google_api_project_name
        clint Id:       google clint_id
        secret key :    google clint_secret_key
        sites:          http://127.0.0.1:8000/

### test

    1) http://127.0.0.1:8000/accounts/logout/        --->    SignOut
    2) http://127.0.0.1:8000/accounts/signup/        --->    SignUp   NOT RECOMMENDED
    3) http://127.0.0.1:8000/accounts/login/         --->    login  click google
    4) http://127.0.0.1:8000/accounts/google/login/  --->    login with google


    # Social accounts in db
        now updated with login google account

### to override allauth templates

    got to:
        venv\Lib\site-packages\allauth\templates\account  (this is the default templates)

    to override
        visit --> https://django-allauth.readthedocs.io/en/latest/templates.html
