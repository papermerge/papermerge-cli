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

### list

Now, with `PAPERMERGE_CLI__HOST` and `PAPERMERGE_CLI__TOKEN` environment variables
set you can use list content of you home folder:

    $ papermerge-cli list

In order to list content of specific folder (including inbox folder):

    $ papermerge-cli list --parent-uuid=UUID-of-the-folder

### me

In order to see current user details (current user UUID, home folder UUID, inbox folder UUID, username etc):

    $ papermerge-cli me

### pref-list

List all preferences:

    $ papermerge-cli pref-list

List specific section of the preferences

    $ papermerge-cli pref-list --section=ocr

Show value of preference `trigger` from section `ocr`:

    $ papermerge-cli pref-list --section=ocr --name=trigger

### pref-update

Update value of the preference `trigger` from section `ocr`:

    $ papermerge-cli pref-update --section=ocr --name=trigger --value=auto


### import

Recursively imports folder from local filesystem. For example, in order
to import recursively all documents from local folder:

    $ papermerge-cli import /path/to/local/folder/

You can also import one single document

    $ papermerge-cli import /path/to/some/document.pdf

### search

Search for node (document or folder) by text or by tags:

    $ papermerge-cli search -q apotheke

Returns all documents (or folders with such title) containing OCRed text 'apotheke'.

You can search by tags only:

    $ papermerge-cli search --tags important

Will search for all documents (and folders) which were tagged with tag 'important'
When multiple tags are provided, by default, will search for nodes with all mentioned tags:

    $ papermerge-cli search --tags important,letters  # returns nodes with both tags important AND letters

In case you want to search for nodes with ANY of the provided tags, use `tags-op` parameter:

    $ papermerge-cli search --tags important,letters --tags-op any

Finally, `tags` and `q` may be combined:

    $ papermerge-cli search --tags important -q apartment
