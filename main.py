import sys

from lxml import html, etree
from collections import Counter


# From the original task matching any 3 of 5 attributes(excluding id) guarantees match of elements
SIMILARITY_PERCENT = 3/5


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) != 3:
        raise Exception('You should enter three arguments: path to original html, path to changed html, id of element')

    with open(args[0], 'r') as original_html:
        root = html.parse(original_html).getroot()
        try:
            element = root.get_element_by_id(args[2])
        except KeyError as e:
            print('ERROR: There is no such id in the original html')
            exit(1)

        # Collect attributes of the found element.
        attrs = {k: v for k, v in element.items()}

    with open(args[1], 'r') as altered_html:
        root = etree.parse(altered_html).getroot()
        tree = root.getroottree()

        def _build_xpath(attribute):
            return etree.XPath(
                f"descendant-or-self::*[@{attribute} and contains(concat(' ', normalize-space(@{attribute}), ' '), concat(' ', $attr, ' '))]"
            )

        matches = {}
        for attr_name, attr_value in attrs.items():
            # Try to match element by every attribute we've gathered from original element
            matches[attr_name] = [tree.getpath(i) for i in _build_xpath(attr_name)(root, attr=attr_value)]

        # If id has been matched ignore other attributes
        if len(matches.get('id')) > 0:
            print('The id of an element has matched. Other attributes were ignored.')
            print('XPATH:', matches.get('id')[0])
        else:
            # Ignore id in similarity % calculations
            del(matches['id'])
            matches_list = [i for item in matches.values() for i in item]
            for item, cnt in Counter(matches_list).items():
                similarity = cnt/len(matches.keys())
                if similarity >= SIMILARITY_PERCENT:
                    matched_attrs_names = [k for k, v in matches.items() if item in v]
                    print(f'Similarity percent is {similarity}. {cnt} attributes out of {len(matches.keys())} matched.')
                    print(f'Matched attributes are: {", ".join(matched_attrs_names)}')
                    print('XPATH:', item)
