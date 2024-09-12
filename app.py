#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module Name: app.py

Description:
    Flask app for Ernest Baker's professional resume website

Author:
    Ernest Baker (baker5792@gmail.com)

Created:
    2024-08-28

Last Modified:
    2024-08-28

Version:
    0.2.0

License:
    GPL 3.0

Usage:
    python app.py [options]
"""

import logging
import argparse
from flask import Flask, render_template

# Setting up logging
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='src/static', template_folder='src/templates')

projects = [
    {
        "title": "Ernest Baker - Professional Resume",
        "description": "This project encompasses my professional portfolio, resume and other experiences.",
        "link": "https://github.com/crow50/ernest-portfolio",
        "image": "images/Resized_American_Bulldog_Crow_Avatar.png"
    },
    {
        "title": "LibraryAssembler",
        "description": "Application dedicated to sorting, renaming and delivering your eBooks, Magazines, Comics and Audiobooks",
        "link": "https://github.com/crow50/libraryassembler",
        "image": "images/DALLE_LibraryAssembler.webp"
    }
]

def setup_logging(level: int = logging.INFO) -> None:
    """Set up logging with a specified log level."""
    logging.basicConfig(level=level, format=LOG_FORMAT)
    logger.setLevel(level)
    logger.debug("Logging is set up.")

def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Start the Flask application.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("-o", "--output", type=str, help="Output file path")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host to run the Flask app on")
    parser.add_argument("--port", type=int, default=5000, help="Port to run the Flask app on")

    args = parser.parse_args()

    if args.verbose:
        setup_logging(logging.DEBUG)
        logger.debug("Verbose mode activated.")

    return args

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html', projects=projects)

@app.route('/military-service')
def military_service():
    return render_template('military_service.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

def main() -> None:
    """
    Main entry point of the script.
    """
    logger.info("Script started.")
    args = parse_arguments()

    # Run the Flask app
    match args:
        case argparse.Namespace(verbose=True):
            app.run(debug=True)
        case _:
            app.run()

    logger.info("Script finished.")

if __name__ == '__main__':
    main()
