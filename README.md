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

Papermerge Cli will prompt you for username and password. On successfull
authentication your REST API token will be displayed - now you can use
this token for all subsequent authentications.

Use token for authentication by exporting token as PAPERMERGE_CLI__TOKEN environment
variable:

    $ export PAPERMERGE_CLI__TOKEN=mytoken

Now, with `PAPERMERGE_CLI__HOST` and `PAPERMERGE_CLI__TOKEN` environment variables
set you can use list content of you home folder:

    $ papermerge-cli list

In order to list content of specific folder (including inbox folder):

    $ papermerge-cli list --parent-uuid=UUID-of-the-folder

In order to see current user details (current user UUID, home folder UUID, inbox folder UUID, username etc):

    $ papermerge-cli me


List all preferences:

    $ papermerge-cli pref-list

List specific section of the preferences

    $ preferences-cli pref-list --section=ocr

Show value of preference `trigger` from section `ocr`:

    $ preferences-cli pref-list --section=ocr --name=trigger

Update value of the preference `trigger` from section `ocr`:

    $ preferences-cli pref-update --section=ocr --name=trigger --value=auto
