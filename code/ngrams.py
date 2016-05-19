# import sys
import os
import nltk
from codecs import open
# from operator import itemgetter
# import numpy as np
# import glob
import dhh_preprocess_tools

nltk.download('punkt')

input_string = ""


def check_env():
    if os.uname()[1] == 'dhh':
        return "/srv/data/newspapers/newspapers/fin/"
    else:
        return "../testdata/fin/"


# local or production?
basepath = check_env()


def get_stopwordlist(input_file):
    output_list = []
    with open(input_file, 'r', encoding="utf-8") as infile:
        for line in infile:
            output_list.append(line.rstrip('\n').strip())
    return output_list


def token_func(input_string):
    tokens = nltk.word_tokenize(input_string.lower())
    refined_tokens = []
    stopwordlist = get_stopwordlist("../data/first_stopwordlist.txt")
    for token in tokens:
        if len(token) > 3:
            if token not in stopwordlist:
                refined_tokens.append(token)
    return refined_tokens


def token_dict(token_list):
    token_counts = {}
    for token in token_list:
        if token in token_counts:
            token_counts[token] = [token_counts[token][0] + 1]
        else:
            token_counts[token] = [1]
    return token_counts


def read_file_to_string(input_file):
    output_string = ""
    with open(input_file, 'r', encoding="utf-8") as infile:
        for line in infile:
            output_string = output_string + line
    return output_string


def token_percentage(token_counts, number_of_tokens):
    length_of_tokenlist = number_of_tokens
    for token in token_counts:
        percentage = round((token_counts[token][0]) / float(length_of_tokenlist), 7)
        token_counts[token].append(percentage)
    return token_counts


def read_files_from_textfile_to_list(file_list_textfile):
    print "reading filelist: " + file_list_textfile + "\n"
    file_list = []
    with open(file_list_textfile, 'r') as infile:
        for line in infile:
            print line
            file_list.append(line.rstrip('\n').strip())
    return file_list


def string_from_list(file_list):
    results_string = ""
    for item in file_list:
        print "\nprocessing item: " + item
        # file3 = item
        results_string += read_file_to_string(item)
    return results_string

# for the first file

# input_file = "test_input.txt"
output_file = "test_output.txt"

print "\nprocessing immigration testdata\n"

training_articles = read_files_from_textfile_to_list("../data/training_data_article_elements.txt")

input_string1 = string_from_list(training_articles)
tokens1 = token_func(input_string1)
lemmatized_tokens1 = dhh_preprocess_tools.hfst_words(tokens1,
                                                     filter=('VERB', 'NOUN', 'ADJ', 'PROPN'))
length_of_tokenlist1 = len(lemmatized_tokens1)
diction1 = token_dict(lemmatized_tokens1)
final_diction1 = token_percentage(diction1, length_of_tokenlist1)
print final_diction1


# the second file preparation

base_articles = read_files_from_textfile_to_list("../data/randomish_sample_3000_articles.txt")

# print type(articles)

input_string3 = string_from_list(base_articles)

# for item in articles:
#     print "\nprocessing item: " + item
#     # file3 = item
#     input_string3 += read_file_to_string(item)

print "\ntokenizing..."
tokens3 = token_func(input_string3)
print "\nadding first tokens to this one..."
tokens3.extend(lemmatized_tokens1)
lemmatized_tokens3 = dhh_preprocess_tools.hfst_words(tokens3,
                                                     filter=('VERB', 'NOUN', 'ADJ', 'PROPN'))
print "\ncounting length: "
length_of_tokenlist3 = len(lemmatized_tokens3)
print ("\n" + str(length_of_tokenlist3) + " tokens")
print "\ncreating dictionary..."
diction3 = token_dict(lemmatized_tokens3)
print "\ncalculating percentages..."
final_diction3 = token_percentage(diction3, length_of_tokenlist3)

###################

# input_file2 = "test_input2.txt"
# # output_file2 = "test_output2.txt"

# input_string2 = read_file_to_string(input_file2)

# tokens2 = token_func(input_string2)
# length_of_tokenlist2 = len(tokens2)
# diction2 = token_dict(tokens2)
# final_diction2 = token_percentage(diction2)
# print final_diction2


def get_differences_dict(training_dict, base_dict):
    differences_dict = {}
    for key in final_diction1:
        if key in final_diction3:
            difference = round(final_diction1[key][1] - final_diction3[key][1], 5)
            count_in_1 = final_diction1[key][0]
            count_in_2 = final_diction3[key][0]
            differences_dict[key] = [difference, count_in_1, count_in_2]
    return differences_dict


def sort_and_shorten_results(differences_dict):
    sorted_list = sorted(differences_dict.items(), key=lambda i: i[1][0], reverse=True)
    shortened_list = sorted_list[:500]
    return shortened_list


differences_dict = get_differences_dict(final_diction1, final_diction3)
# for key in final_diction1:
#     if key in final_diction3:
#         difference = round(final_diction1[key][1] - final_diction3[key][1], 5)
#         count_in_1 = final_diction1[key][0]
#         count_in_2 = final_diction3[key][0]
#         differences_dict[key] = [difference, count_in_1, count_in_2]

# print differences_dict

# if you want to sort with some other item in the list change the secnod position in the lambda

results_list = sort_and_shorten_results(differences_dict)

# sorted_list = sorted(differences_dict.items(), key=lambda i: i[1][0], reverse=True)

# print sorted_list

# shortened_list = sorted_list[:500]


def write_pretty_output(output_file):
    out_f = open(output_file, 'w')
    for item in results_list:
        outputline = unicode(item[0] + "   " +
                             str(item[1][0] * 100) +
                             " %  " +
                             str(item[1][1]) +
                             " items\n")

        out_f.write(outputline.encode('utf8'))
    out_f.close()


def write_machinereadable_output(output_file):
    out_f = open(output_file, 'w')
    for item in results_list:
        outputline = unicode(item[0] + "," +
                             str(item[1][0] * 100) + "\n")

        out_f.write(outputline.encode('utf8'))
    out_f.close()


print "\nwriting top 500 into outputfile\n"
write_pretty_output("really_nice_output_file_500_stopwords_filtered_lemmatized.txt")
write_machinereadable_output("machinereadable_output_file_500_stopwords_filtered_lemmatized.txt")
