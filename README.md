# Full Stack FastAPI and Deta

THis branche focus on the implementation of the CRUD operations on `users`

The inventory of all branches is available on the master branche, more specifically in its README file

## Features

## Gettring the right versions

Deta use python runtime 3.7.9. It will avoid bad surprises to adapt your environment

    brew install pyenv (check details on official doc)
    CFLAGS="-I$(brew --prefix openssl)/include -I$(brew --prefix readline)/include -I$(xcrun --show-sdk-path)/usr/include" \
        LDFLAGS="-L$(brew --prefix openssl)/lib -L$(brew --prefix readline)/lib -L$(xcrun --show-sdk-path)/usr/lib"\
        pyenv install 3.7.9
    pyenv local 3.7.9
    python -m pip install poetry
    python -m poetry install

## Setting up

Always start with jumping into the right pool

    python -m poetry shell
    curl -fsSL https://get.deta.dev/cli.sh | sh


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

## Running

    deta new backend
    cd backend && deta update --env ../.settings.dev

## Linting

    bash lint.sh backend tests

## Adding dependencies

    poetry add you_dependency
    poetry export -f requirements.txt --without-hashes --output backend/requirements.txt
    deta deploy backend/

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