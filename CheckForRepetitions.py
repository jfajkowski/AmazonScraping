import os

acquired_set = set()
amazon_list = []
with open(os.path.dirname(os.path.abspath(__file__)) + "/database/msd_acquired.txt") as f_in:
    for msd_id in f_in:
        acquired_set.add(msd_id.rstrip())

with open(os.path.dirname(os.path.abspath(__file__)) + "/database/unique_tracks.txt") as f_in:
    for line in f_in:
        if line.split("<SEP>")[0] not in acquired_set:
            amazon_list.append(line.rstrip())

with open(os.path.dirname(os.path.abspath(__file__)) + "/database/amazon_tracks.txt", mode='w') as f_out:
    for line in amazon_list:
        f_out.write("%s\n" % line)
print "DONE"