# Custom Djoser Project

Djoser is a Django package that simplifies the process of creating RESTful APIs for Django applications. It provides a set of Django Rest Framework views and endpoints to handle common authentication tasks such as registration, login, logout, password reset, and account activation. Djoser leverages Django's built-in authentication mechanisms and extends them to work with web tokens, offering a seamless integration for developers looking to implement token-based authentication in their projects.

One of the main benefits of using Djoser is its flexibility and extensibility. It allows developers to customize authentication behavior to fit their specific needs without having to write extensive amounts of boilerplate code. Additionally, Djoser's adherence to RESTful principles ensures that APIs built with it are both scalable and easy to consume.

In this project, we have taken the core concepts of Djoser and implemented them natively, tailoring the authentication and user management features specifically for our application's requirements. This approach has allowed us to fine-tune performance, enhance security, and provide a more customized user experience.

## Features

- Token-based authentication system
- Customizable registration and login processes
- Secure password reset mechanism
- Account activation workflow
- Extensible user profiles

## Getting Started

To get started with this project, clone the repository and set up a virtual environment:

```sh
git clone https://github.com/rahulcodepython/Custom-Djoser.git
cd Custom-Djoser
```

Create virtual environment:

```sh
python -m virtualenv venv
```

Activate environment:

for windows

- `sh venv\Scripts\activate`

for linux

- `sh source venv/bin/activate`

Install the required dependencies:

```sh
pip install -r requirements.txt
```

Run the Django migrations to prepare your database:

```sh
python manage.py migrate
```

Finally, start the development server:

```sh
python manage.py runserver
```

## Usage

1. Write an environment file named `.env` file:

```
GITHUB_CLIENT_ID=<Github OAuth2 client id>
GITHUB_CLIENT_SECRET=<Github OAuth2 client secret>
GOOGLE_CLIENT_ID=<Google OAuth2 client id>
GOOGLE_CLIENT_SECRET=<Google OAuth2 client secret>

FRONTEND_URL=http://localhost:3000/
BACKEND_URL=http://localhost:8000
EMAIL_HOST_USER=<Email sending host user email>
EMAIL_HOST_PASSWORD=<Email sending host user password>

GITHUB_REDIRECT_URI=http://localhost:3000/github/callback
GOOGLE_REDIRECT_URI=http://localhost:3000/google/callback
```

## Packages

|   Used Package List   |
| :-------------------: |
|  DjangoRestFramework  |
|       SimpleJWT       |
| Django Mail Templated |

## Contributing

Contributions to this project are welcome. Please refer to the CONTRIBUTING.md file for more details.
