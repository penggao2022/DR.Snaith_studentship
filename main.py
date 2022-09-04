import spacy
import re
nlp = spacy.load("en_core_web_sm")

#name:speaker
name_dic = {}
#get the txt context to a list
def extract_file_to_new_file(filename, encoding='utf-8'):
    sentence_list = []
    with open(filename, encoding=encoding) as file:
        line = file.readline()
        while line:
            if line != '\n':
                sentence_list.append(line)
            line = file.readline()
    file.close()

    with open('clean_data.txt', 'w', encoding='utf-8') as file:
        for i in sentence_list:
            file.write(i)
    return sentence_list


def write_to_new_file(filename, thing_need_to_write):
    with open(filename, encoding='utf-8', mode='w') as file:
        for i in thing_need_to_write:
            file.write(i)
            file.write('\n')

# if find a connection between a name and a speakernum, replace all the speakernum with this name in the list
def replace_all_in_sentence_list(sentence_list, entity_to_speaker_text:str):
    if name_dic.get(entity_to_speaker_text):
        speaker_num = name_dic[entity_to_speaker_text]
        for index, sentence in enumerate(sentence_list):
            match = re.match(speaker_num, sentence)
            if match is not None:
                start, end = match.span()
                new_sentence = sentence.replace(sentence[start: end], entity_to_speaker_text)
                sentence_list[index] = new_sentence
    return sentence_list

# check function
def check_if_value_twice_and_change_to_full(dic_value):
    for index, item in enumerate(name_dic):
        if item in dic_value:
            name_dic[dic_value] = name_dic.pop(item)
            return dic_value
        elif dic_value in item:
            return item
    return dic_value


#parse, convert the text to the target context
def parse(text):
    doc = nlp(text)
    pattern = r'Speaker(\d+)'
    match = re.match(pattern, text)
    for ent in doc.ents:
        # print(ent.text+"---"+ent.label_)
        if ent.label_ == "PERSON":
            # if name_dic.get(ent.text):
            #      start, end = match.span()
            #     # # new_text = text.replace(text[start: end], name_dic[ent.text])
            if not name_dic.get(ent.text):
                # print(ent.text)
                #new_text是本来
                new_text = check_if_value_twice_and_change_to_full(ent.text)
                # print(new_text)
                if new_text == ent.text:
                    start, end = match.span()
                    name_dic[new_text] = text[start: end]
                    replace_all_in_sentence_list(sentence_list=sentence_list, entity_to_speaker_text=ent.text)
                    # new_text = text.replace(text[start: end], ent.text)



sentence_list = extract_file_to_new_file('./transcript.txt')

for index, sentence in enumerate(sentence_list):
    parse(text=sentence_list[index])

print("--------------------------")

for i in sentence_list:
    print(i)

write_to_new_file('./clean_data.txt', sentence_list)












