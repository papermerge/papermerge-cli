[![Tests](https://github.com/papermerge/papermerge-cli/actions/workflows/tests.yml/badge.svg)](https://github.com/papermerge/papermerge-cli/actions/workflows/tests.yml)

# Papermerge Cli

Command line utility which uses REST API to interact with your Papermerge DMS
instance. You can use `papermerge-cli`, for example, to recursively import local folder to
your Papermerge DMS instance.

## Requirements

In order to use `papermerge-cli` you need to have python installed.
You need [python](https://www.python.org/) version >= 3.10.

## Install

    $ pip install papermerge-cli

[pip](https://pypi.org/project/pip/) is package installer for python - it usually comes with python
interpreter. In order to install `pip` on Ubuntu use following command:

    $ sudo apt install python3-pip


## REST API/CLI Version Compatibility

REST API column - is version of Papermerge REST API server. This value
you can get from:

    $ papermerge-cli server-version

CLI column - is version of papermege-cli command line utility. This value
you can get from:

    $ papermerge-cli --version


| REST API | CLI  |
|----------|------|
| =3.0     | =0.7 |
| =2.1     | = 0.3.3|

## Usage

Get you REST API authentication token from your instance:

    $ papermerge-cli --host=https://mydms.some-vps.com auth

Or you can provide host as environment variable:

    $ export PAPERMERGE_CLI__HOST=https://mydms.some-vps.com
    $ papermerge-cli auth

Papermerge Cli will prompt you for username and password. On successfull
authentication your REST API token will be displayed - now you can use
this token for all subsequent authentications.

Use token for authentication by exporting token as `PAPERMERGE_CLI__TOKEN`
environment variable:

    $ export PAPERMERGE_CLI__TOKEN=mytoken

### list

Now, with `PAPERMERGE_CLI__HOST` and `PAPERMERGE_CLI__TOKEN` environment
variables set you can use list content of you home folder:

    $ papermerge-cli list

In order to list content of specific folder (including inbox folder):

    $ papermerge-cli list --parent-uuid=UUID-of-the-folder

### me

In order to see current user details (current user UUID, home folder UUID, inbox
folder UUID, username etc):

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

If you want the local copy the uploaded documents **to be deleted** after
successful import - add `--delete` flag:

    $ papermerge-cli import --delete /path/to/folder/

PLEASE BE CAREFUL WITH `--delete` FLAG AS IT WILL IRREVERSIBLE DELETE THE LOCAL
COPY OF THE UPLOADED DOCUMENT!

### search

Search for node (document or folder) by text or by tags:

    $ papermerge-cli search -q apotheke

Returns all documents (or folders with such title) containing OCRed
text 'apotheke'.

You can search by tags only:

    $ papermerge-cli search --tags important

Will search for all documents (and folders) which were tagged with
tag 'important' When multiple tags are provided, by default, will search for
nodes with all mentioned tags:

    $ papermerge-cli search --tags important,letters  # returns nodes with both tags important AND letters

In case you want to search for nodes with ANY of the provided tags, use
`tags-op` parameter:

    $ papermerge-cli search --tags important,letters --tags-op any

Finally, `tags` and `q` may be combined:

    $ papermerge-cli search --tags important -q apartment

### download

Downloads a folder or a document:

    $ papermerge-cli download --uuid <document or folder uuid>

In case uuid is the ID of specific folder - a zip file will be downloaded; zip
file will contain all nodes insides specified folder.

You can use `--uuid` multiple times:

    $ papermerge-cli download --uuid <uuid of doc1> --uuid <uuid of doc2> --uuid <uuid of folder 1>

If you want to download content to specific file on your file-system, use `-f`
option:

    $ papermerge-cli download --uuid <doc-uuid> -f /path/to/file-system/document.pdf

or in case of uuid is a folder:

    $ papermerge-cli download --uuid <folder-uuid>  -f /path/to/file-system/folder.zip

You can also specify the format/type of the downloaded archive (e.g. in case node is either a folder):

     $ papermerge-cli download --uuid <folder-uuid>  -f /path/to/file-system/folder.targz -t targz
