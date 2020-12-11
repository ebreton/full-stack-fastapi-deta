# Full Stack FastAPI and Deta

THis branche focus on the implementation of the CRUD operations on `users`

The inventory of all branches is available on the master branche, more specifically in its README file

## Features

## Testing

    export PYTHONPATH=~/git-repos/full-stack-fastapi-deta/backend
    pytest -x --pdb tests

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
        - flake8
        - pytest

## Tree architecture

- isolate the user features in one package `users`
    -> will facilitate the implementation of multi micros
- expose the `schemas` outside of the package
    -> will act as the contract between micros
- provide the scafeholding in `core`
    -> keep as DRY as possible