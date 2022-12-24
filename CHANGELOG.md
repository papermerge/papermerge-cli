# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

This project uses [*towncrier*](https://towncrier.readthedocs.io/) and the changes for the upcoming release
can be found in [changelog.d folder](https://github.com/papermerge/papermerge-cli/tree/master/changelog.d/).

<!-- towncrier release notes start -->

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
