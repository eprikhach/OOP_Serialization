# OOP_Serialization

<p> In this task we will work with OOP, SOLID
principles and serialization.</p>

<p> To solve this task we need:
1. Create base classes for entity.
2. Implement deserialization. 
3. Create new python objects with existed data.
4. Implement Serialization to JSON and XML.</p>


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
- Script must contain input parameters

# How to run a script

- Install python3, if missing
  https://www.python.org/downloads/.

- Install dependencies using requirements.txt . 
  Its can be done with a command in the terminal,
  namely "pip3 install -r requirements.txt"

- To run the script
  you need to copy the path to the .py file,
  path to room.json, students.json, choose on of
  two serialization format and 
  write the following 
  construction: "python3 path-to-file
  path-to-rooms.json path-to-students.json xml/json", 
  where path-to-file is your path.
