# Papermerge Cli

Command line utility which uses REST API to interact with your Papermerge DMS instance

## Install

    $ pip install papermerge-cli


## Usage

Get you REST API authentication token from your instance:

    $ papermerge-cli --host=https://mydms.some-vps.com auth

Or you can provide host as environment variable:

    $ export PAPERMERGE_CLI__HOST=https://mydms.some-vps.com
    $ papermerge-cli auth


Papermerge Cli will prompt you for username and password. Opon successfull
authentication your REST API token will be displayed.