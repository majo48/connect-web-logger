# froeling-web-connect-logger
Log status information from connect-web.froeling.com.

# Prerequisites
- a froeling PE1 pellet boiler at your home 
- a registered connect-web account at froeling.com which connects to your PE1 pellet boiler
- a computer (connected to the internet) capable of running this python project periodically

# Input (configuration)
- account name and password @connect-web.froeling.com
- data acquisistion period in minutes (15, 30, 60)

# Process
- get all the available status data from the froeling website, write status values to a database
- this project does not need MODBUS hardware (like https://github.com/mhoffacker/PyLamdatronicP3200)

# Output
- a SQLite database file containing the periodic data
- process status information
