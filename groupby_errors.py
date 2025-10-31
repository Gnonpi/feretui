from pprint import pprint
from collections import Counter
from pathlib import Path

LOG_TYPING = Path() / "basedpyright.log"

error_lines = []
with open(LOG_TYPING) as f:
    for line in f:
        if "error: " in line:
            error_msg = line.split("error: ")[1:]
            error_msg = " -- ".join(error_msg)
            error_lines.append(error_msg)
results = Counter(error_lines)
pprint(results.most_common(5))

