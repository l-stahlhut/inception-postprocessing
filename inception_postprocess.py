# -*- coding: utf-8 -*-


"""Script to extract 'Beleglisten' for certain tags from the output of a semantically annotated Inception output.
Format of of the inception output (tsv-file):

#Text=So beautifull 😍
14-1	350-352	So	AdjP[4]	EvÄ\_p[87]|EvB\_l[88]
14-2	353-363	beautifull	AdjP[4]	EvÄ\_p[87]|EvB\_l[88]
14-3	364-366	😍	AdjP[4]	EvÄ\_p[87]|EM\_bez[89]

The text is tokenized and sentences are seperated by empty lines.
Formal tags can be found in the third column and functional tags can be found in the fourth column.
"""
# How to use the script:
# $ python3 export_tags.py --input data/ --output belegliste_AdjP.txt --formal AdjP
# $ python3 export_tags.py --input data/ --output belegliste_AdjP.txt --functional EM_bez
# $ python3 export_tags.py --input data/ --output belegliste_In_EvB_l.txt --tag1 In --tag2 EvB_l
# $ python3 export_tags.py --input data/ --output belegliste_phrase_EvB_l.txt --phrase EvB_l

import os
import re
import argparse

parser = argparse.ArgumentParser(description='Get Beleglisten')
parser.add_argument("-i", "--input", help="Specify folder with the input files")
parser.add_argument("-o", "--output", help="Specify the name of your output file.")
parser.add_argument("-fo", "--formal", help="Specify formal tag (e.g. 'NP').")
parser.add_argument("-fu", "--functional", help="Specify functional tag (e.g. 'EM_bez').")
parser.add_argument("-t1", "--tag1", help="Specify the first tag a word in the sentence was tagged with.")
parser.add_argument("-t2", "--tag2", help="Specify the second tag a word in the sentence was tagged with.")
parser.add_argument("-p", "--phrase", help="Specify the tag a phrase was tagged with.")
args = parser.parse_args()

################################# 1. get data ################################################

def get_lines():
	"""Iterates over files in a folder and returns a nested list. Outer list: one sentence per list item. Inner list:
	one token with its tags per list item.

	   lines_list = [['#Text=😘😘😘🔥🔥❤️😍\n',
	   '4-1\t132-134\t😘\t_\tEM\\_k\\_p[9]|EvÄ\\_p[10]|Iteration[11]|EM\\_bez[12]\t\n',
	   '4-2\t134-136\t😘\t_\tEM\\_k\\_p[9]|EvÄ\\_p[10]|Iteration[11]|EM\\_bez[13]\t\n', ...], [], [], ...]
	   """
	# iterate over files to get a list of file names
	file_names = []

	with os.scandir(args.input) as it:  # todo: give path
		for entry in it:
			if entry.name.endswith(".tsv") and entry.is_file():
				file_names.append(entry.name)

	lines_all_files = []

	for filename in file_names:
		with open(os.path.join('data', filename), 'r') as infile:

			lines = infile.readlines()
			lines.append('\n')  # append newline so that for loop works

			sentences = []
			sentence = []

			for line in lines:
				if line != '\n':
					sentence.append(line)  # sentences within a file are split by a newline
				else:
					sentences.append(sentence)  # list of sentences
					sentence = []  # empty list for next sentence

			sentences = sentences[5:] # exclude metainformation

			for sent in sentences:
				lines_all_files.append(sent)

	return lines_all_files

################################# 2. get dictionary for sentence, phrase, words##################################

def sentence_dictionary():
    """Extract a list of dictionaries from the nested list with the relevant information: a sentence
    and the tags that occur in it (no duplicates).
    list = [
    {
    "text": "Hammer bild 🤩💙",
    "functional_tags": ["NP", "EvB_l"],
    "formal_tags":["NP", "EvÄ_p", "Evb_l", "Evb_e_rand", "EM_bez"]
    }, {}, {}, ...]
    """

    sentences = get_lines()

    l = []  # list of dictionaries

    for sentence in sentences:
        text = sentence[0][6:].rstrip()  # initial sentence to print when tag is present

        # get functional and formal tags lists
        words = sentence[1:]
        formal_tags = []
        functional_tags = []

        for word in words:
            formal_tag = word.rstrip().split('\t')[3]
            functional_tag = word.rstrip().split('\t')[4]
            if formal_tag != '_':
                formal_tags.append(formal_tag)
            if functional_tag != '_':
                functional_tags.append(functional_tag)

        # postprocess formal tags list
        formal_tags = list(set(formal_tags))  # remove duplicates
        formal_tags_clean = []
        for item in formal_tags:
            tag_clean = re.sub(r'[0-9\[\]]', '', item)
            tag_clean = tag_clean.replace('\\', '')
            formal_tags_clean.append(tag_clean)

        # postprocess functional tags list
        functional_tags_split = []
        for item in functional_tags:  # split where there are multiple tags per word
            tags = item.split('|')
            functional_tags_split.append(tags)

        # flatten nested list
        functional_tags_new = []
        for sublist in functional_tags_split:
            for tag in sublist:
                functional_tags_new.append(tag)

        functional_tags = list(set(functional_tags_new))  # remove duplicates
        functional_tags_clean = []
        for item in functional_tags:
            tag_clean = re.sub(r'[0-9\[\]]', '', item)
            tag_clean = tag_clean.replace('\\', '')
            functional_tags_clean.append(tag_clean)

        # compile dictionary
        d = {"text": text, "functional tags": functional_tags_clean, "formal tags": formal_tags_clean}

        l.append(d)

    return l


def token_dictionary():
    """Returns a list of sentences with info on which tags a token was tagged with. .
    Input: Nested list. List of tokens within list of sentences.
    Output: list of dictionaries (sent_list)
    sent_list = [{
        sentence: "token1 token2 token3",
        sent_info: [{token: "token1", tags: ["tag1", "tag2", "tag3", ...]},
                    {token: "token3", tags: ["tag1", "tag2", ...]},
                    {token: "token3", tags: ["tag1", "tag2", ...]}
    ]}
    ]
    """
    list = get_lines()

    sent_list = []

    for l in list:
        sentence = l[0][6:].rstrip()
        sent_info = []

        tokens = l[1:]
        for t in tokens:
            token = t.split('\t')[2]
            tags_form = t.split('\t')[3].replace('\\_','_').replace(r'[0-9\[\]]', '')
            tags_form = re.sub(r'[0-9\[\]]', '', tags_form).split('|')
            tags_funkt = t.split('\t')[4].replace('\\_', '_').replace(r'[0-9\[\]]', '')
            tags_funkt = re.sub(r'[0-9\[\]]', '', tags_funkt).split('|')
            tags = tags_form + tags_funkt
            d = {'token': token, 'tags': tags}
            sent_info.append(d)

        d_sent = {'sentence': sentence, 'sent info': sent_info}

        sent_list.append(d_sent)

    return sent_list


def token_dictionary_raw():
    """Same as token dictionary but with numbers of tags preserved (intermediary step for phrase dictionaries."""

    list = get_lines()

    comments_list = []

    for comment in list:
        sentence = comment[0][6:].rstrip()
        sent_info = []

        tokens = comment[1:]
        for t in tokens:
            token = t.split('\t')[2]
            tags_form = t.split('\t')[3].replace('\\_', '_').split('|')
            tags_funkt = t.split('\t')[4].replace('\\_', '_').split('|')
            tags = tags_form + tags_funkt
            if '_' in tags:
                tags.remove('_')
            d_token = {'token': token, 'tags': tags}
            sent_info.append(d_token)

        d_sent = {'sentence': sentence, 'sent info': sent_info}

        comments_list.append(d_sent)

    return comments_list


def phrase_dictionaries():
    """Returns a list of dictionaries with all tagged 'phrases' per sentence.
       ('Phrases' here means all symbols tagged by a single tag)
       Input: Token dictionary

       :return:
       sent_list = [
           'phrases': {
               'AdjP[6]': 'So beautifull 😍',
               'EvÄ_p[91]': 'So beautifull 😍',
               'EvB_l[92]':'So beautifull',
               'Em_bez[93]':'😍'}, {...}, ...]
       """
    l = []  # one dictionary with phrases per comment

    token_d = token_dictionary_raw()

    for comment in token_d:
        phrases = {}
        for token in comment['sent info']:
            tk = token['token']
            for tag in token['tags']:
                if tag in phrases:
                    phrases[tag].append(tk)
                else:
                    phrases[tag] = [tk]

        #modify key and value (remove numbers from tags, join values)
        d_new = {}
        for k, v in phrases.items():
            k_new = re.sub(r'[0-9\[\]]', '', k)
            d_new[k_new] = ' '.join(v).replace(' .', '.').replace(' ,', ',').replace(' !', '!').replace(' ?', '?')

        l.append(d_new)

    return l

################### 3. fetch info from dictionary according to specified tag ################################

def get_sentences_formal():
    """Return sentences that include a certain formal tag."""

    l = sentence_dictionary()  # list of sentence dictionaries
    sentences_with_tag = []

    for d in l:
        if args.formal in d['formal tags']:
            sentences_with_tag.append(d['text'])

    return sentences_with_tag


def get_sentences_functional():
    """Return sentences that include a certain functional tag."""

    l = sentence_dictionary()  # list of sentence ditionaries
    sentences_with_tag = []

    for d in l:
        if args.functional in d['functional tags']:
            sentences_with_tag.append(d['text'])

    return sentences_with_tag


def get_sentences_multi_tag():
    """Return sentences where at least one word is tagged with both specified tags."""
    sent_list = token_dictionary()
    sentences_with_tags = []

    for d in sent_list:
        sent = d['sentence']
        sent_info = d['sent info']
        for t in sent_info:
            tags = t['tags']
            if args.tag1 in tags and args.tag2 in tags:

                sentences_with_tags.append(sent)

    return sentences_with_tags


def get_phrases():
    """Returns a list of phrases that were tagged with a certain tag."""

    l = phrase_dictionaries()
    phrases_with_tag = []

    for d in l:
        if args.phrase in d.keys():
            phrases_with_tag.append(d[args.phrase])

    return phrases_with_tag

################################# 4. write file ################################################

def outfile():
    if args.formal is not None:
        sentences = get_sentences_formal()
        with open(os.path.join('beleglisten_comments/', args.output), 'w') as f_out:
            for sentence in sentences:
                sentence = sentence + '\n'
                f_out.write(sentence)

    elif args.functional is not None:
        sentences = get_sentences_functional()
        with open(os.path.join('beleglisten_comments/', args.output), 'w') as f_out:
            for sentence in sentences:
                sentence = sentence + '\n'
                f_out.write(sentence)

    elif args.tag1 is not None and args.tag2 is not None:
        sentences = get_sentences_multi_tag()
        with open(os.path.join('beleglisten_comments/', args.output), 'w') as f_out:
            for sentence in sentences:
                sentence = sentence + '\n'
                f_out.write(sentence)

    elif args.phrase is not None:
        phrases = get_phrases()
        with open(os.path.join('beleglisten_phrases/', args.output), 'w') as f_out:
            for phrase in phrases:
                phrase = phrase + '\n'
                f_out.write(phrase)

    else:
        print("Please specify an argument!")


def main():

    outfile()


main()


