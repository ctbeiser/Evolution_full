import re
import sys
import json

decoder = json.JSONDecoder()
count = 0
buffer = ""

READ_SIZE = 1
MULTILINE_JSON = r"[\[{]"
MULTILINE_JSON_RE = re.compile(MULTILINE_JSON)

for line in sys.stdin:

    buffer += line.rstrip()
    tried = 0

    while tried < len(buffer):

        try:
            decoded, end = decoder.raw_decode(buffer)
            buffer = buffer[end:].lstrip()
            count += 1
            print(json.dumps(decoded))

        except ValueError as e:
            if not MULTILINE_JSON_RE.match(buffer):
                exit(0)
            tried = len(buffer)

print(json.dumps({"count": count}))
