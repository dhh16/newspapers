from codecs import open


def get_stopwordlist(input_file):
    output_list = []
    with open(input_file, 'r', encoding="utf-8") as infile:
        for line in infile:
            output_list.append(line)
    return output_list

print get_stopwordlist("../data/first_stopwordlist.txt")
