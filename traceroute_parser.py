import json

with open(file="data/results_list-ipv4_traceroute-(21-1-1_21-1-2).json", mode="r") as file_handle:
    traceroute_results = json.load(file_handle)

file_handle.close()


print(type(traceroute_results))
print(str(len(traceroute_results)))
