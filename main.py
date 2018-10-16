import argparse
import os
import csv
import json
import datetime
import numpy as np

#-------------------------------------------------------------------------------------------------------------------
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--print', help="Prints out resulting password", action='store_true')
parser.add_argument('-l', '--log', help="Prints out elements of the log file", action='store_true')
parser.add_argument('url', help="Enter the url to get the password for")
args = parser.parse_args()

#-------------------------------------------------------------------------------------------------------------------
def url_strip(root):
    """
    Goal: strip the url parameter to the alphabetic characters of the website name only.
    Package(s): csv (reader()).

    url_strip() is a 3 steps process:
        1- splitting anything before and including 'www.' ;
        2- splitting anything after and including the domain (e.g. '.com') ;
        3- removing all non-alphabetic characters.

    :param root: the url to strip to the website name.

    :return: the url striped.
    """
    if root.find('//www.') != -1:
        pref = 'www.'
    else:
        pref = '//'
    if pref in root:
        root = root.split(pref)[1]

    with open('MatthieuMAYER/passwords/domain_list.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] in root:
                root = root.split(row[0])[0]

    for s in root:
        if not s.isalpha():
            root = root.replace(s, '')

    return root.lower()

#-------------------------------------------------------------------------------------------------------------------
def save_log(seed):
    """
    Goal: save the stripped url name in the json log file (create or update usage time).
    Package(s): json (load(), dumps(), datetime (datetime,now()).

    save_log() is a 2 steps process:
        1- load the json log file as a local dictionary and update the current log in this dictionary ;
        2- save the updated log dictionary as the json log file.

    :param seed: the stripped url name to save or update in the json log file.

    :return: none.
    """
    log_file = 'MatthieuMayer/passwords/log.json'
    with open(log_file, 'r') as file:
        dict_log = json.load(file)
        dict_log[seed] = str(datetime.datetime.now())

    with open(log_file, 'w') as file:
        file.write(json.dumps(dict_log))

#-------------------------------------------------------------------------------------------------------------------        
def display_log():
    """
    Goal: print all key/value pairs stored in the json log file.
    Package(s): json (load()).

    print_log() is a 1 step process:
        1- load the json log file in a local dictionary and print every key/value pairs.

    :return: none.
    """
    log_file = 'MatthieuMayer/passwords/log.json'
    with open(log_file, 'r') as file:
        dict_log = json.load(file)
        for k, v in dict_log.items():
            print(k, ':', v)

#-------------------------------------------------------------------------------------------------------------------      
def num_to_alpha(x):
    """
    Goal: convert any number looping on a 26 digits base in its alphabetic analog (e.g. 1 = 'a', 13 = 'm', 28 = 'b').
    Package(s): none.

    num_to_alpha() is a 3 steps process:
        1- create lists of numbers from 1 to 26 and letters from 'a' to 'z' ;
        2- zip the lists in a list of tuples ;
        3- convert the list of tuples in a dictionary.

    :param x: the number to convert to alphabetic character.
    :return: the alphabetic character corresponding to x.
    """
    if x > 26:
        x = x % 26
    ls_numb = [i for i in range(1, 27)]
    ls_alpha = [chr(i) for i in range(ord('a'), ord('z') + 1)]

    ls_conv = list(zip(ls_numb, ls_alpha))

    dict_conv = dict(ls_conv)

    return dict_conv[x]

#-------------------------------------------------------------------------------------------------------------------
def alpha_to_num(s):
    """
    Goal: convert any alphabetic character in its numerical analog (e.g. 'a' = 1, 'm' = 13).
    Package(s): none.

    alpha_to_num() is a 3 steps process:
        1- create lists of letters from 'a' to 'z' and numbers from 1 to 26 ;
        2- zip the lists in a list of tuples ;
        3- convert the list of tuples in a dictionary.

    :param s: the alphabetic character to convert to a number.
    :return: the number corresponding to s.

    """
    ls_alpha = [chr(i) for i in range(ord('a'), ord('z') + 1)]
    ls_numb = [i for i in range(1, 27)]

    ls_conv = list(zip(ls_alpha, ls_numb))

    dict_conv = dict(ls_conv)

    return dict_conv[s]

#-------------------------------------------------------------------------------------------------------------------
def create_password(seed):
    """
    Goal: create a password specific to the seed passed as a parameter.
    Package(s): numpy.random (seed(), randint()).

    create_password() is 3 steps process:
        1- convert each letter of the website name to numbers and add them to create the random generator seed ;
        2- generate one upper case letter, one 5 digits number and one lower case letter
        3- concatenate these 3 parts with '-' characters to create the password

    :param seed: the seed to create the password from (in our case the website name).
    :return: the created password specific to the given seed.
    """
    ls_num = [alpha_to_num(s) for s in seed]
    sum = 0
    for num in ls_num:
        sum += num
    np.random.seed(sum)

    ul_part = num_to_alpha(np.random.randint(1, 27)).upper()
    num_part = np.random.randint(10000, 100000)
    ll_part = num_to_alpha(np.random.randint(1, 27))

    password = ul_part + '-' + str(num_part) + '-' + ll_part

    return password             

####################################################################################################################

def main():
    root = args.url
    seed = url_strip(root)
    save_log(seed)
    password = create_password(seed)
    os.system("echo '%s' | pbcopy" % password)
    
    if args.print:
    print('\n', password, '\n')

    if args.log:
        cfc.display_log()
        print('\n')

main()
