"""In this task we will work with OOP, SOLID
principles and serialization.

To solve this task we need:
1. Deserialize JSON files.
2. Merge lists
3. Implement serialization to JSON and XML.
"""

from xml.dom.minidom import parseString
import json
import argparse

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


class Serializer:
    """Base class, that implements serialization Python object"""

    def __init__(self, students_in_room: list):
        self.students_in_room = students_in_room

    def to_format(self):
        raise NotImplementedError

    def to_file(self):
        raise NotImplementedError


class XMLSerializer(Serializer):
    """Class that implements serialization to XML."""

    def __init__(self, students_in_room: list):
        super().__init__(students_in_room)

    def to_format(self):
        """Converts a lists of dicts to XML string.

        :return: XML in string representation
        """

        xml_string = dicttoxml(self.students_in_room,
                               custom_root='students_in_room',
                               # dict_to_xml(item_func) need function,
                               # that generate the element name for
                               # items in a list. Default is 'item'.
                               item_func=lambda source_name: 'field',
                               attr_type=False)

        xml = parseString(xml_string).toprettyxml()
        return xml

    @logger.catch
    def to_file(self):
        """Converts a lists of dicts to XML string.

        :return: None
        """

        with open('students_in_room.xml', 'w') as xml_file:
            xml_file.write(XMLSerializer.to_format(self))

        logger.info('StudentsInRoom was serialized into XML.')


class JSONSerializer(Serializer):
    """Class that implements serialization to XML."""

    def __init__(self, students_in_room: list):
        super().__init__(students_in_room)

    @logger.catch
    def to_format(self):
        """Converts a list of dicts to JSON string.

        :return: JSON in string representation.
        """

        json_string = json.dumps(self.students_in_room, indent=2)
        return json_string

    @logger.catch
    def to_file(self):
        """Fill json file with data.

        :return: None
        """
        json_string = JSONSerializer.to_format(self)
        with open('students_in_room.json', 'w') as json_file:
            json_file.write(json_string)

        logger.info('StudentsInRoom was serialized into JSON.')


@logger.catch
def get_students_from_json(students_json: str):
    """Getting students information from JSON object.

    :param students_json: Path to students JSON
    :return: list
    """

    with open(students_json, 'r') as json_file:
        students_list = json.load(json_file)

    logger.info('Students.json was deserialized to list of dicts.')

    return students_list


def get_rooms_from_json(rooms_json: str):
    """Getting students information from JSON object.

        :param rooms_json: Path to rooms JSON
        :return: list
        """

    with open(rooms_json, 'r') as json_file:
        rooms_list = json.load(json_file)

    logger.info('Rooms.json was deserialized to list of dicts.')

    return rooms_list


@logger.catch
def list_merge(rooms_list: list, students_list: list):
    """Merging two lists.

    :param rooms_list: List of rooms.
    :param students_list: List of students.
    :return: list
    """

    students_in_room = []

    for room in rooms_list:
        students_in_room.append({'id': room['id'],
                                 'room_name': room['name'],
                                 'students': []})

    for student in students_list:
        if student['room'] == students_in_room[student['room']]['id']:
            students_in_room[student['room']]['students'] \
                .append(student['name'])

    logger.info('Students_in_room list of dicts was merged.')

    return students_in_room


def args_parser():
    """Script arguments parser.

    :return: class
    """
    parser = argparse.ArgumentParser(
        description='Parser for script, which implement serialization')
    parser.add_argument('-s', '--students', type=str,
                        help='Path to students.json')
    parser.add_argument('-r', '--rooms', type=str,
                        help='Path to rooms.json')
    parser.add_argument('-f', '--format', choices=['json', 'xml'],
                        help="Serialization format")
    return parser


@logger.catch
def main(room_json: str, student_json: str, serialize_format: str):
    students = get_students_from_json(student_json)
    rooms = get_rooms_from_json(room_json)
    students_in_room = list_merge(rooms, students)
    if serialize_format.lower() == 'xml':
        XMLSerializer(students_in_room).to_file()
    if serialize_format.lower() == 'json':
        JSONSerializer(students_in_room).to_file()


if __name__ == '__main__':
    args_namespace = args_parser().parse_args()
    main(args_namespace.rooms, args_namespace.students,
         args_namespace.format)
