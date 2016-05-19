# import sys
import os
import nltk
from codecs import open
import glob
#nltk.download('punkt')
import xml.etree.ElementTree as ET

input_string = ""


def check_env():
    if os.uname()[1] == 'dhh':
        return "/srv/data/newspapers/newspapers/fin/"
    else:
        return "../testdata/fin/"


# local or production?
basepath = check_env()


def token_func(input_string):
    tokens = nltk.word_tokenize(input_string.lower())
    refined_tokens = []
    for token in tokens:
        if len(token) > 3:
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
    file_list = []
    with open(file_list_textfile, 'r') as infile:
        for line in infile:
            file_list.append(line.rstrip('\n').strip())
    return file_list
  


def string_from_list(file_list):
    results_string = ""
    print file_list
    print "\nprocessing item: " + file_list
    results_string += read_file_to_string(file_list)
    return results_string


###########################
# checking for the probability 
############################


def article_prob():
    out_f5 = open("Final", 'w')
    input_article_list = read_files_from_textfile_to_list("../data/randomish_sample_3000_articles.txt")
    # i =0
    for in_list in input_article_list:
        input_string_article = ""
        input_string_article = string_from_list(in_list)  # read file to string
        article_token = token_func(input_string_article)
        out_f = open("output_file_article", 'w')
        out_f1 = open("output_file_article_final", 'w')
        for item in article_token:
            out_f.write(item.encode('utf8') + "\n")
            out_f.close()
        in_string = read_file_to_string("../data/machinereadable_output_file_500_stopwords_filtered_lemmatized_relative.txt")
        in_token = token_func(in_string)
        le = len(article_token)
        lab = in_token[1].split(",")
        sumi = 0.0
        for item in article_token:
            for i in range(0, len(in_token) - 1):
                l = in_token[i].split(",")[0]
                if item == l:
                    out_f_l = unicode(item + "\t" + in_token[i].split(",")[1])
                    out_f1.write(out_f_l.encode("utf") + "\n")
                    sumi = sumi + float(in_token[i].split(",")[1])
            print "The final sum(values)/amount of is \n"
        if le > 0:
            lll = sumi / le
        else:
            lll = 0
        out_ff = unicode(in_list + "\t" + "," + str(lll))
        out_f5.write(out_ff.encode("utf") + "\n")
    write_Final_readable()


def write_Final_readable():
    out_final_readable = open("Final_hyperlink.txt", "w")
    f = open("Final", "r")
    answer = {}
    sorted_list2 = {}
    for line in f:
        k, v = line.strip().split(",")
        answer[k.strip()] = v.strip()
    f.close()
    sorted_list = sorted(answer.items(), key=lambda i: i[1], reverse=True)
    for j in range(0, len(sorted_list)):
        start = sorted_list[j][0].find("extracted")
        end_sup = sorted_list[j][0].find("supplement")
        end_sec = sorted_list[j][0].find("section")
        if end_sup > 0:
            xmml_path = sorted_list[j][0][:start] + "alto" + sorted_list[j][0][start + 9:end_sup] + "001.xml"
        elif end_sec > 0:
            xmml_path = sorted_list[j][0][:start] + "alto" + sorted_list[j][0][start + 9:end_sec] + "001.xml"
        else:
            end = sorted_list[j][0].find("article")
            xmml_path = sorted_list[j][0][:start]+"alto"+sorted_list[j][0][start+9:end]+"001.xml"
        e = ET.parse(xmml_path).getroot()
        out_xff = unicode("Serial Number = " + str(j) +"\n" + e[0][16].text + "\n" + str(sorted_list[j][1]) + "\n" + sorted_list[j][0] + "\n"+ "********************************" + "\n")
        out_final_readable.write(out_xff.encode("utf") +"\n")


def write_final_readable_textfilelinks():
    out_final_readable = open("Final_textfiles.txt","w")
    f = open("Final","r")
    answer ={}
    sorted_list2 ={}
    for line in f:
        k,v = line.strip().split(",")
        answer[k.strip()] = v.strip()
    f.close()
    sorted_list = sorted(answer.items(), key=lambda i: i[1], reverse=True)
    shortened_list = sorted_list[:50]
    for j in range(0,len(shortened_list)):
        # start = sorted_list[j][0].find("extracted")
        # end_sup = sorted_list[j][0].find("supplement")
        # end_sec = sorted_list[j][0].find("section")
        # if end_sup>0:
        #     xmml_path = sorted_list[j][0][:start]+"alto"+sorted_list[j][0][start+9:end_sup]+"001.xml"
        # elif end_sec>0:
        #     xmml_path = sorted_list[j][0][:start]+"alto"+sorted_list[j][0][start+9:end_sec]+"001.xml"
        #     else:
        #     end = sorted_list[j][0].find("article")
        #         xmml_path = sorted_list[j][0][:start]+"alto"+sorted_list[j][0][start+9:end]+"001.xml"
        # e = ET.parse(xmml_path).getroot()
        out_xff = unicode("Serial Number = " + str(j) +"\n" + str(sorted_list[j][1]) + "\n"+ "86.50.168.175/" + (sorted_list[j][0])[4:] + "\n"+ "********************************" + "\n")
        out_final_readable.write(out_xff.encode("utf") +"\n")
