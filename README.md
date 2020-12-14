# connect-web-logger
Log information from a registered account at connect-web.froeling.com.

# Prerequisites
- a Fröling PE1 pellet boiler at your home 
- a registered connect-web account at froeling.com which connects to your PE1 pellet boiler
- a computer (connected to the internet) capable of running this Python project periodically

# Input (CLI / configuration)
- account name and password @connect-web.froeling.com
- data acquisition period in minutes (15, 30, 60)

# Process
- get status (configuration) data from the froeling website (read-only)
- write status (configuration) values to a database
- this project does NOT need MODBUS hardware (like https://github.com/mhoffacker/PyLamdatronicP3200)

# Output
- a SQLite database file containing the periodic data
- process status information (stdout, stderr)

# Running the app
- change directory(cd) to where this project resides
- enter command: ***python3 -m logger username password period***
  - username: registered username at connect-web.froeling.com
  - password: registered password for the above user
  - period:   logging period in minutes (15, 30, 60)
  - w.o. arguments: the values are read from the configuration file

# Fairness / Legal
- this app puts some strain on the froeling.com website
- use only for optimizing your Fröling PE1 pellet boiler
- web scraping is legal for "intended usage" and for public data
  - reading your own "private" data is the same as reading public data (IANAL) 
  - Froeling should provide a (local) LAN-API to the PE1 pellet boiler, avoiding the hassle of going thru the internet and the Fröling servers in order to get some local data in the first place 