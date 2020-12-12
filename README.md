# froeling-web-connect-logger
Log status information from connect-web.froeling.com.

# Prerequisites
- a froeling PE1 pellet boiler 
- a registered connect-web account at froeling.com
- a virtual server (OSX, LINUX) capable of running this python project once per 15 minutes, half hour or hour.

# Input
- account name and password
- data acquisistion period in minutes (15, 30, 60)

# Process
- get all the available status data from the froeling website
- this project does not need MODBUS hardware (like https://github.com/mhoffacker/PyLamdatronicP3200)

# Output
- a SQLite database file containing the (aggregated) periodic data
