"""In this task we will work with OOP, SOLID
principles and serialization.

To solve this task we need:
1. Create base classes for entity.
2. Implement deserialization.
3. Create new python objects with existed data.
4. Implement serialization to JSON and XML.
"""

import json
import re
from xml.dom.minidom import parseString
import sys

from dicttoxml import dicttoxml
# Logging third-party tools is mainly used here for debugging. I
# thought about catching critical situations of different levels,
# but this would greatly inflate the program.
from loguru import logger

# Removing basic logging handler, which is used for debugging.
# Users don't need to know what's going on in the program.
logger.remove(0)

logger.add('logs.log', level='INFO',
           format="{time} {level} {message}",
           rotation='1 MB', compression='zip')


class Student:
    """Base class for students."""

    instances = []

    def __init__(self, student_id: int, student_name: str, room: int):
        self.student_id = student_id
        self.name = student_name
        self.room = room
        self.__class__.instances.append(self)


class Room:
    """Base class for rooms."""

    instances = []

    def __init__(self, room_id: int, room_name: str):
        self.room_id = room_id
        self.room_name = room_name
        self.__class__.instances.append(self)


class StudentsInRoom:
    """Base class for students, that livings in a room"""

    instances = []

    def __init__(self, room_number: int, students_name: list):
        self.room_number = room_number
        self.students_name = students_name
        self.__class__.instances.append(self)


class Deserialize:
    """Base class for implementing data deserialization."""

    @logger.catch
    def from_file(self):
        raise NotImplementedError


class StudentsDeserializeFromJSON(Deserialize):
    """Class, that implements deserialization to Python objects."""

    def __init__(self, path_to_file):
        self.path_to_file = path_to_file

    @logger.catch
    def from_file(self):
        """Deserialization json structure into Student instances.

        :return: None
        """

        with open(self.path_to_file, 'r') as json_file:
            students_list = json.load(json_file)
            for student in students_list:

                Student(student_id=student['id'],
                        student_name=student['name'],
                        room=student['room'])

        logger.info('Json file with students info was deserialized, '
                    'Student has a {} instances'.
                    format(len(Student.instances)))


class RoomsDeserializeFromJSON(Deserialize):
    """Class, that implements deserialization into Python objects."""

    def __init__(self, path_to_file):
        self.path_to_file = path_to_file

    @logger.catch
    def from_file(self):
        """Deserialization json structure to Rooms instances.

        :return: None
        """

        with open(self.path_to_file, 'r') as json_file:
            rooms_list = json.load(json_file)
            for room in rooms_list:
                Room(room_id=room['id'], room_name=room['name'])

        logger.info('Json file with room info was deserialized, '
                    'Room has a {} instances now.'.
                    format(len(Room.instances)))


class DataDumping:
    """Base class for data dumping."""

    def dump_data(self):
        raise NotImplementedError


class StudentsInRoomDumping(DataDumping):
    """Dumping a new structure data to StudentsInRoom."""

    @staticmethod
    @logger.catch
    def dump_data():
        """Converts fields from different class instances into new
        Python objects.

        :return: None
        """

        for room in Room.instances:
            students_in_room = []
            for student in Student.instances:
                if int(re.search(r'\d+', room.room_name).group(0)) \
                        == student.room:
                    # re is used here to check room number,
                    # id may not be always = room number
                    students_in_room.append(student.name)
            StudentsInRoom(room_number=room.room_name,
                           students_name=students_in_room)
        logger.info("StudentsInRoom was dumped and now contains {} "
                    "instances".format(len(StudentsInRoom.instances)))


class Serialize:
    """Base class, that implements serialization Python object"""

    @staticmethod
    def to_format():
        raise NotImplementedError


class SerializeToXML(Serialize):
    """Class that implements serialization to XML."""

    @staticmethod
    @logger.catch
    def to_format():
        """Converts a python object to XML.

        :return: None
        """
        students_in_room = []
        for room_info in StudentsInRoom.instances:
            students_in_room.append(room_info.__dict__)
        xml_string = dicttoxml(students_in_room,
                               custom_root='students_in_room',
                               # dict_to_xml(item_func) need function,
                               # that generate the element name for
                               # items in a list. Default is 'item'.
                               item_func=lambda source_name: 'field',
                               attr_type=False)

        xml = parseString(xml_string).toprettyxml()

        with open('students_in_room.xml', 'w') as xml_file:
            xml_file.write(xml)

        logger.info('StudentsInRoom was serialized into XML.')


class SerializeToJSON(Serialize):
    """Class that implements serialization to XML."""

    @staticmethod
    @logger.catch
    def to_format():
        """Converts a python object to JSON.

        :return: None
        """

        students_in_room = []
        for room_info in StudentsInRoom.instances:
            students_in_room.append(room_info.__dict__)

        with open('students_in_room.json', 'w') as json_file:
            json.dump(students_in_room, json_file, indent=2)

        logger.info('StudentsInRoom was serialized into JSON.')


@logger.catch
def main(room_json, student_json, serialize_format):
    if str(serialize_format).lower() == 'json':
        RoomsDeserializeFromJSON(str(room_json)).from_file()
        StudentsDeserializeFromJSON(str(student_json)).from_file()
        StudentsInRoomDumping().dump_data()
        SerializeToJSON().to_format()
    elif str(serialize_format).lower() == 'xml':
        RoomsDeserializeFromJSON(str(room_json)).from_file()
        StudentsDeserializeFromJSON(str(student_json)).from_file()
        StudentsInRoomDumping().dump_data()
        SerializeToXML().to_format()
    else:
        print('Incorrect serialization format')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])
