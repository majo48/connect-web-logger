# Dependencies
Copyright (c) 2020 M. Jonasse (martin.jonasse@mail.ch)

This application is built and tested with the following dependencies:

- ***python*** (3.9): programming language
- ***pip*** (20.3.3): package installer for Python
- ***setuptools*** (51.0.0): library for packaging Python projects
- ***selenium*** (3.141.0): framework for software testing
  - urllib (1.26.2): library for selenium
- ***phantomjs*** (1.3.0): discontinued headless browser used for automating web page interaction
- ***schedule*** (0.6.0): lightweight scheduler (like cron)
- ***matplotlib*** (3.3.3): Python standard plotter
  - Pillow (8.0.1): library for matplotlib
  - cycler (0.10.0): library for matplotlib
  - kiwisolver (1.3.1): library for matplotlib
  - numpy (1.19.4): library for matplotlib
  - pyparsing (2.4.7): library for matplotlib
  - python-dateutil (2.8.1): library for matplotlib
  - six (1.15.0): library for matplotlib

Developed with:

- ***pycharm*** (Professional 2020.3): Jetbrains Python IDE 
- dependencies are located in a new virtual environment, stored in the project repository folder ***connect-web-logger/venv*** (excluded in .gitignore)
- exceptions for MacOS: 
  - also install geckodriver ($ brew install geckodriver)
