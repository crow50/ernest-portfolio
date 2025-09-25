# Resume template

*A simple Jekyll + GitHub Pages powered resume template.*

## Credits

This template was originally created by [Joel Glovier](https://github.com/jglovier). The code and styles are licensed under the MIT license. [See project license.](LICENSE)

## Docs

### Running locally

To test locally, run the following in your terminal:

1. Clone repo locally
1. `bundle install`
2. `bundle exec jekyll serve`
3. Open your browser to `localhost:4000`

### Customizing

First you'll want to fork the repo to your own account. Then clone it locally and customize, or use the GitHub web editor to customize.

#### Options/configuration

Most of the basic customization will take place in the `/_config.yml` file. Here is a list of customizations available via `/_config.yml`:

1. `resume_avatar`  
2. `resume_avatar_photo`  
3. `resume_name`  
4. `resume_title`  
5. `resume_contact_email`  
6. `resume_contact_telephone`  
7. `resume_contact_address`

#### Editing content

Most of the content configuration will take place in the `/_layouts/resume.html` file. Simply edit the markup there accordingly

### Publishing to GitHub Pages for free

[GitHub Pages](https://pages.github.com/) will host this for free with your GitHub account. Just make sure you're using a `gh-pages` branch, and the site will automatically be available at `yourusername.github.io/resume-template` (you can rename the repo to resume for your own use if you want it to be available at `yourusername.github.io/resume`). You can also add a CNAME if you want it to be available at a custom domain...

### Configuring with your own domain name

To setup your GH Pages site with a custom domain, [follow the instructions](https://help.github.com/articles/setting-up-a-custom-domain-with-github-pages/) on the GitHub Help site for that topic. We set up a `CNAME` at `_site/CNAME` to point to `domain.name`. Adjust it if you have a different domain.
