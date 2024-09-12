# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

### Changed
- Began working on [military_service.html](../src/templates/military_service.html), added references in base template nav bar and app.py
- Corrected typo in [portfolio.html](../src/templates/portfolio.html)
- Improved [css](../src/static/css/main.css) and included entries for project-items
- Renamed projects.html to [portfolio.html](../src/templates/portfolio.html) and added more projects

### Added
- Generated [Library Assembler Image](../src/static/images/DALLE_LibraryAssembler.webp)
- Created project data structure and looping function. Resolves #15

### Fixed
- Validated and corrected links in navigation bar. Resolves #16

## [2.2.0-alpha] 2024-08-29

### Added
- Created new templates: [about.html](../src/templates/about.html), [contact.html](../src/templates/contact.html), and [projects.html](../src/templates/projects.html)

### Fixed
- Restored previous static files to [github-pages](../github-pages/) to maintain static pages until containerized application is complete.

### Changed
- Versioned [app.py](../app.py) to 0.2.0, I intend to have it catch up with this changelog in the future
- Reversioned [changelog](CHANGELOG.md) in preparation of application versioning.
- Relocated pieces of the original [index.html](../src/templates/index.html) to the various templates: [about.html](../src/templates/about.html), [contact.html](../src/templates/contact.html), and [projects.html](../src/templates/projects.html)
- Updated [deploy.yml](../.github/workflows/deploy.yml) to include new location for static github pages 
- Updated [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) link to version 1.1.0 from 1.0.0


## [2.1.0-alpha] - 2024-08-28

### Added
- Created [base.html](../src/templates/base.html) for dynamic website as a Flask project

### Changed
- Refactored [index.html](../src/templates/index.html) for Flask syntax and referencing new [base template](../src/templates/base.html)
- Fixed nooptions in [app.py](../app.py)
- Refactored [app.py](../app.py) to include logging and arguments


## [2.0.0-alpha] - 2024-08-28

### Changed
- Promplty removed the enhancement/dynamic-website branch from the [deploy.yml](../.github/workflows/deploy.yml) since it wouldn't pass checks due to not being able to deploy to Github Pages because of environment protection rules
- Added enhancement/dynamic-website branch to [deploy.yml](../.github/workflows/deploy.yml) for testing of changes
- Moved previous site files to [src/](../src/)
- Renamed clevelandwater to [cleveland-water](../cleveland-water/)
- Renamed dlc to [duquense-light-company](../duquesne-light-company/)
- Updated [deploy.yml](../.github/workflows/deploy.yml) to reflect job path for Github Actions
- Updated [Issue and Pull Request Templates](../.github/) to be a bit more relevant
- Swapped verbage in the [CHANGELOG](CHANGELOG.md) from deleted to removed as is proper, also tracking these ongoing changes
- Updated [index.html](../src/templates/index.html) to reference the new locations for [icon](../src/static/images/favicon.ico) and [css](../src/static/css/main.css)
- Split site file between [static](../src/static/) and [templates](../src/templates/) for Flask convention
- Renamed static asset folders except for [image](../src/static/images/), styles becomes [css](../src/static/css/) and scripts becomes [js](../src/static/js/)

### Added
- Created [src/](../src/) folder to hold project files going forward
- Created [requirements.txt](../requirements.txt)
- Created [app.py](../app.py) for Flask application
- Created [static](../src/static/) and [templates](../src/templates/) folders for Flask convention


## [1.1.0] - 2024-08-27

### Fixed
- Corrected links in [CHANGELOG](CHANGELOG.md)

### Added
- This [CHANGELOG](CHANGELOG.md) including the [docs/](../docs/) folder
- [Issue and PR Templates](../.github/)
- Initial [.gitignore](../.gitignore)

### Removed
- Removed unnecessary package.json
- Removed static.yml.bak from previous github actions


## [1.0.0] - 2024-08-01

### Previously Existed
- [Workflows](../.github/workflows/)
- [Cleveland Water](../clevelandwater/)
- [DLC](../dlc/)
- [Images](../images/)
- [Scripts](../scripts/)
- [Styles](../styles/)
- [Index.html](../index.html)
- [LICENSE](../LICENSE)
- [README](../README.md)