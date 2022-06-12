with open("result.txt") as f:
    str_in_file = str(f.readlines())
    species_number = str_in_file.count("https")
    raw_list = str_in_file.split(": {'")
    raw_list.remove(raw_list[0])

#get the threats
species_threats_dict = {}
all_threats_set = set()

for i in range(species_number):
    single_threat = raw_list[i].split("]]")

    for j in range(raw_list[i].count(": ")):
        if single_threat[j].find(", '") == 0:
            single_threat[j] = single_threat[j][3:]
        single_threat[j] = single_threat[j][single_threat[j].find(". ")+2:single_threat[j].find("': ")]

    single_threat.remove(single_threat[-1])
    species_threats_dict[i] = single_threat
    all_threats_set = all_threats_set | set(single_threat)

#all_threats_list consists of all kinds of threats
all_threats_list = list(all_threats_set)
frequency = []


#the frequency of each threat
for i in range(len(all_threats_list)):
    frequency.append(0)
    for j in range(species_number):
        if all_threats_list[i] in species_threats_dict[j]:
            frequency[i] += 1


#print the threats with the highest frequency 
for i in range(len(all_threats_list)):
    if frequency[i] == max(frequency):
        print(all_threats_list[i])