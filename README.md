# Amaranth

**This is not an officially supported Google product.**

**Please note that development on this project has ceased. See
[Project Status](#project-status) for more information.**

Amaranth is a nutritional data inference project to help users become more aware
of what's in their food.

Amaranth is comprised of two sub-projects:

- The Amaranth Machine Learning Model (Amaranth ML)
- The Amaranth Chrome Extension (Amaranth CE)

Amaranth ML does the predicting, for example, identifying whether or not a dish
is high-calorie. Amaranth CE is in charge of finding dish names on webpages to
give to Amaranth ML, and then displaying the result to the user.

## Installation

Most major project functions have an associated Makefile recipe.
To set up the project for development, run the `setup` recipe in the root of the
project directory as follows:

```bash
make setup
```

This will install all dependencies for Amaranth ML (using your local `pip`
version), and install all the dependencies for Amaranth CE into the
`amaranth-chrome-ext/` directory using `npm`.

The other possible recipes you can run for this project are listed below.

```bash
make run-interactive   # Run the Amaranth ML model in an interactive mode
make run-train         # Train the Amaranth ML model
make test-python       # Run Python unit tests
make lint-python       # Lint Python source code
make test-js           # Run Javascript unit tests
make lint-js           # Lint Javascript source code
```

## Usage

Amaranth CE is not packaged as an official Chrome Extension, and is not released
on the Chrome Web Store. If you'd like to install Amaranth CE on your own Chrome
web browser, please use the following steps.

1. Clone this project to your local machine using `git clone ...`
2. In your Chrome browser navigate to `chrome://extensions` in the URL bar
3. Toggle "Developer Mode" ON.
    - The toggle is located in the top right-hand corner of the screen, but 
    machine requirements could move the button around.
4. Select "Load Unpacked" from the menu.
5. In the file browser, navigate to the this project's install directory, and
select the `amaranth-chrome-ext/` directory.
6. Done! Navigate to any restaurant page on grubhub.com to see the model infer
dish data.

## Project Structure

- `amaranth-chrome-ext/` - Amaranth CE source code
- `amaranth/` - Amaranth ML source code
- `data/` - Directory to store datasets for training Amaranth ML. More info
can be found in `data/where-is-the-data.md`
- `docs/` Miscellaneous documentation files

## Project Status

This project was a part of Tom Lauerman's Google internship in the summer of
2020. Since the conclusion of the internship, this Github repository is now
inactive.