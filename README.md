[![pipeline status](https://gitlab.com/kiliant/paper-archive/badges/master/pipeline.svg)](https://gitlab.com/kiliant/paper-archive/commits/master)

# Newspaper Archive
## What it Does
- As a subscriber of the digital version of the [SZ (Sueddeutsche Zeitung)](https://www.sueddeutsche.de/) I was annoyed of the many clicks that were necessary in order to download a PDF file of any issue, so I decided to automate this process.
- This project is built on [Selenium](https://www.seleniumhq.org/), a browser automation project. It enables us to use a headless version of Firefox for browsing e.g. subscriber websites.
- This project looks for available issues of the SZ and then downloads them into a named docker volume. Additionally, it keeps track of all downloaded volumes in a sqlite database. Now you could run this project once a day (or, once a week) to fetch the newest issue(s) for personal archival purposes.

## How to Use
#. Download run.sh: `wget https://raw.githubusercontent.com/kiliant/paper-archive/master/run.sh && chmod +x run.sh`
#. Adapt to you needs (enter username and password)
#. Execute `./run.sh`

## Improvements
This project is not by any means feature-complete.
As of right now, it is working(tm) with Sueddeutsche Zeitung.
But I would like to restructure the code and make it more modular, in order to incorporate more subscription services.
By doing this, this could become a useful project for folks like me that want to create a personal archive of multiple media (subscription services).
Please feel free to help.
You might want to have a look at the issues for a hint regarding any open work.

## License
This project is licensed under the MIT License.

