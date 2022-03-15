# pyaster
This project is intended to provide similar functionality in Python as [roaster](https://github.com/i-Cell-Mobilsoft-Open-Source/roaster) provides in Java to write automated unit and integration tests ... or something like so.

# what has been done yet (a.k.a. feature list)
1. config provider which eats yaml files from a folder and provides values stored in it 
2. random util to generate ids and uuids and tokens

# what has been planned (a.k.a. todo list)
1. documentation
2. requirements.txt
3. Zephyr Scale (in [roaster](https://github.com/i-Cell-Mobilsoft-Open-Source/roaster) it is 
known as TM4J)

# what is out of the current scope
These functionality provided by Python in more straightforward way than it is in Java
so it won't be implemented in this lean library since it doesn't intended to reinvent the wheel
(neither the wheel cog)
1. `RestAssured` which has a more straightforward replacement in Python via `requests`
2. `Redis` which in Python already implemented in `redis` library
3. Similar functionality than `Oracle DB` is `cx_Oracle` in Python 
4. `Selenide` and `Hybernate` and `MongoDB` have reliable and well tested Python libraries as well 
