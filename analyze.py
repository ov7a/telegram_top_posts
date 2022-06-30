import sys
import json
from collections import defaultdict

with open(sys.argv[1]) as f:
	data = list(map(json.loads, filter(None, f.read().split('\n'))))

top_count = int(sys.argv[2]) if len(sys.argv) > 2 else 5

all_reactions = set()
for item in data:
	all_reactions |= item["reactions"].keys()

def print_top(hint, criteria):
	print(hint)
	for item in sorted(data, key=criteria, reverse=True)[:top_count]:
		count = criteria(item)
		if not count:
			break
		print(f"{count} - {item['url']}")

print_top("views", lambda item: item.get("views", 0))
print()
print_top("forwards", lambda item: item["forwards"])
print()
print_top("replies", lambda item: item["replies"])
print()
print_top("total_reactions", lambda item: sum(item["reactions"].values()))
print()
for reaction in sorted(all_reactions):
	print_top(reaction, lambda item: item["reactions"].get(reaction, 0))
	print()
