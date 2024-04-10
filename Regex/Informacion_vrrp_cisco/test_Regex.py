import textfsm
from pprint import pprint
import sys

filename = sys.argv[1]
template_name = sys.argv[2]

def test_Regex(filename, template):
    with open("/Users/georgesolorzano/Google Drive/PythonCode/Assessment/ntc-templates/templates/"+template_name) as f:
        template = textfsm.TextFSM(f)
        with open(filename) as data:
            text = data.read()
            parse = template.ParseTextToDicts(text)
            pprint(parse)

test_Regex(filename, template_name)

