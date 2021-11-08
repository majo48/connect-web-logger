# Dependencies
Copyright (c) 2020 M. Jonasse (martin.jonasse@mail.ch)

This application is built and tested with the following dependencies (subdependencies not displayed):

- ***python*** (3.9): programming language
- ***pip*** (21.2.4): package installer for Python
- ***setuptools*** (57.4.0): library for packaging Python projects
- ***selenium*** (4.0.0): framework for software testing
- ***phantomjs*** (1.4.1): discontinued headless browser used for automating web page interaction
- ***schedule*** (1.1.0): lightweight scheduler (like cron)
- ***matplotlib*** (3.4.3): Python standard plotter

- See: pyCharm -> Preferences -> Project: connect-web-logger -> Python Interpreter
- The above dependencies are located in a new virtual environment, stored in the project repository folder ***connect-web-logger/venv*** (excluded in .gitignore)

- ***Chrome*** (95.0.4638.69): Browser for MacOS
  - staging area (download): https://chromedriver.chromium.org/downloads
  - OSX: chromedriver (download, unzip, terminal: mv <path>/chromedriver /usr/local/bin/chromedriver)
  - Windows: chromedriver.exe (download, unzip, move to: C:\WebDriver\bin\chromedriver.exe)

- Alternative (works too, change code in session.py):
- ***FireFox*** (84.0.1, 64-bit): Browser for MacOS 
  - geckodriver ($ brew install geckodriver)

Developed with:

- ***pycharm*** (Professional 2021.2): Jetbrains Python IDE 
  - where pyCharm > File > Settings > Version Control > Commit
    - unset the checkbox "Use non-modal commit interface"
    - this wil enable your favorite Git > Local Changes window
