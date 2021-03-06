# taskPY1

<p> In this task we will work with OOP, SOLID
principles and serialization.</p>

<p> To solve this task we need:
1. Deserialize JSON files.
2. Merge lists
3. Implement serialization to JSON and XML.
4. Write JSON and XML structures to files. </p>


# Q & A

*<p> Why we use loguru instead of
the built-in logging module? </p>*

- No Handler, no Formatter, no Filter:
  one function to rule them all
- Easier file logging with rotation / retention / compression
- Modern string formatting using braces style
- Exceptions catching within threads or main
- Pretty logging with colors
- Fully descriptive exceptions
- Better datetime handling
- Entirely compatible with standard logging
- 10x faster than built-in logging

*<p> Why we use dicttoxml instead of
the built-in xml.dom.minidom module? </p>*

- It's more simple to use

# Functional requirements

- Concatenate two json files and serialize to
  one of the two formats
- SOLID principles
- OOP
- Script must contains input parameters

# How to run a script

- Install python3, if missing
  https://www.python.org/downloads/.

- Install dependencies using requirements.txt . 
  Its can be done with a command in the terminal,
  namely "pip3 install -r requirements.txt"

- To run the script
  you need to copy the path to the .py file,
  path to room.json, students.json, choose one of
  two serialization format and 
  write the following 
  construction: "python3 path-to-file
  path-to-rooms.json path-to-students.json xml/json"
  into terminal/command line.
