# Changelog

## 0.8.0 - 2024-02-22

## Added

- `--skip-ocr` flag. Works only with Papermerge REST API >= 3.1

## 0.7.1 - 2024-02-20

### Fixed

- papermerge-cli import option --delete without any function [Issue#592](https://github.com/ciur/papermerge/issues/592)


## 0.7.0 - 2023-12-22

- pydantic dependency upgraded from 1.x to v2.5
- `import` command fixed to work with REST API version 3.0 (Papermerge DMS 3.0)
- `server-version` command added (returns version of server REST API)

## 0.3.3 - 2022-12-24


### Added

- Show tabelar output using rich styles [Issue#noissue](https://github.com/papermerge/papermerge-cli/issues/noissue)


## 0.3.2 - 2022-12-24


### Added

- Various minor fixes/additions (e.g. rich formatting was added) [Issue#20](https://github.com/papermerge/papermerge-cli/issues/20)


## 0.3.1 - 2022-12-20


### Added

- add `--version` flag which will show papermerge-cli version [Issue#13](https://github.com/papermerge/papermerge-cli/issues/13)


### Fixed

- Fixes exception when host name contains trailing slash [Issue#15](https://github.com/papermerge/papermerge-cli/issues/15)
- auth command should not ask for password confirmation [Issue#17](https://github.com/papermerge/papermerge-cli/issues/17)


## 0.3.0 - 2022-12-19


### Added

- Relax python requirement from strict 3.10.x to >= 3.8 and < 3.11 [#11](https://github.com/papermerge/papermerge-cli/issues/11)
