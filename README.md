# Full Stack FastAPI and Deta

THis branche focus on the implementation of the CRUD operations on `users`

The inventory of all branches is available on the master branche, more specifically in its README file

## Features

## Setting up

Set all the settings of your backend in a file copied from .settings.sample

    cp .settings.sample .settings.test
        PROJECT_KEY=123
        ...

    cp .settings.sample .settings.dev
        PROJECT_KEY=123
        EMAILS_ENABLED=True
        ...

Set your PYTHONPATH and which settings file to use in your .env file

    cp .env.sample .env
        PYTHONPATH=`pwd`/backend
        SETTINGS_FILE=.settings.dev


## Testing

    SETTINGS_FILE=.settings.test pytest -x --pdb tests

## Linting

    bash lint.sh backend tests

## Technical mindset

- focus on getting fastAPI deployed on a Micro and a BaseBD
- bare environment
    - keeping the deps to the minimum:
        - fastapi
        - passlib (for password encryption)
        - pydantic[email] (for email validation)
        - jinja2 (for emails formatting)
    - keeping tests and linters to the minimum

## Tree architecture

- provide the scafeholding in `core`
    -> keep as DRY as possible
- isolate the user features in one package `users`
    -> will facilitate the implementation of multi micros
- expose the `schemas` outside of the package
    -> will act as the contract between micros