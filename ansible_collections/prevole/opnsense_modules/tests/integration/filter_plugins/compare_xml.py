from lxml import etree as et


class FilterModule(object):
    def filters(self):
        return {'compare_xml': compare_xml}


def compare_xml(current_path, expected_path):
    current = et.parse(current_path)
    expected = et.parse(expected_path)

    return xml_compare(current.getroot(), expected.getroot())


def xml_compare(current, expected):
    if len(current) == len(expected):
        for element in current:
            possible_elements = expected.findall(element.tag)

            if len(possible_elements) == 0:
                raise ex(f'{element.tag} not found in \\{0}', element, expected)

            elif len(possible_elements) == 1:
                if len(element) > 0:
                    xml_compare(element, possible_elements[0])

                elif len(possible_elements[0]) > 0:
                    raise ex('Expected element contains other elements: {1}', element, possible_elements[0])

                elif element.text != possible_elements[0].text:
                    raise ex('{0} is not the same as {1}', element, possible_elements[0])

            else:
                found = False

                for possible_element in possible_elements:
                    try:
                        xml_compare(element, possible_element)
                        found = True
                    except Exception:
                        continue

                if not found:
                    raise ex('{0} not exactly found in {1}', element, possible_elements)

    else:
        raise ex('{0} has not the same length as {1}', current, expected)

    return True


def ex(msg, current, expected):
    path = xml_path(current)
    current_str = xml_str(current)
    expected_str = xml_str(expected)

    return Exception(f'{path}: {msg.format(current_str, expected_str)}')


def xml_str(item):
    if type(item) is list:
        msg = ''

        for i in item:
            msg = f'{msg} / {et.tostring(i)}'

        return msg

    else:
        return et.tostring(item)


def xml_path(element, path=''):
    if element.getparent() is not None:
        return xml_path(element.getparent(), f'/{element.tag}{path}')
    else:
        return f'/{element.tag}{path}'
