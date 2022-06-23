import csv
import re
with open("phonebook_raw.csv", encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
first_line = contacts_list.pop(0)
for contact in contacts_list:
    item1 = re.findall('[А-Я]+[а-я]*', contact[0])
    lastname = item1[0]
    item2 = re.findall('[А-Я]+[а-я]*', contact[1])
    if len(item2) > 0:
        firstname = item2[0]
    elif len(item1) > 1:
        firstname = item1[1]
    else:
        firstname = ''
    item3 = re.findall('[А-Я]+[а-я]*', contact[2])
    if len(item3) > 0:
        surname = item3[0]
    elif len(item2) > 1:
        surname = item2[1]
    elif len(item1) > 2:
        surname = item1[2]
    else:
        surname = ''
    contact[0] = lastname + ' ' + firstname
    contact[1] = firstname
    contact[2] = surname
uniq_list = []
repeat_list = []
for item in contacts_list:
    if item[0] not in uniq_list:
        uniq_list.append(item[0])
    else:
        repeat_list.append(item[0])
merge_list = []
for rep in repeat_list:
    data_list = []
    for contact in contacts_list:
        if contact[0] == rep:
            data_list.append(contact)
        else:
            pass
    merge = ['' for i in range(7)]
    for data in data_list:
        for i, note in enumerate(data):
            if merge[i] != note:
                merge[i] += note
    merge_list.append(merge)
uniq_contacts_list = contacts_list[:]
for merge in merge_list:
    for contact in contacts_list:
        if contact[0] == merge[0]:
            uniq_contacts_list.remove(contact)
uniq_contacts_list += merge_list
for contact in uniq_contacts_list:
    contact[0] = contact[0].split(' ')[0]
phone_pattern1 = '(\+ ?7)\s?\(?\d{3}\)? ?\d{3}-?\d{2}-?\d{2}'
phone_pattern2 = '8\s?\(?\d{3}\)?-? ?\d{3}-?\d{2}-?\d{2}'
added_phone_pattern = 'доб\.\s?\d{4}'
for contact in uniq_contacts_list:
    phone_not_formatted = re.search(phone_pattern1, contact[5])
    if phone_not_formatted:
        phone = re.sub('\s?\(?', '', phone_not_formatted.group())
        phone = re.sub('\)?', '', phone[:])
        phone = re.sub('\-?', '', phone[:])
        phone = phone[0:2] + '(' + phone[2:5] + ')' + phone[5:8] + '-' + phone[8:10] + '-' + phone[10:12]
        added = re.search(added_phone_pattern, contact[5])
        if added:
            added_formatted = re.sub('\s*','', added.group())
            phone = phone + ' ' + added_formatted
    else:
        phone_not_formatted = re.search(phone_pattern2, contact[5])
        if phone_not_formatted:
            phone = re.sub('\s?\(?', '', phone_not_formatted.group())
            phone = re.sub('\)?', '', phone[:])
            phone = re.sub('\-?', '', phone[:])
            phone = '+7(' + phone[1:4] + ')' + phone[4:7] + '-' + phone[7:9] + '-' + phone[9:11]
            added = re.search(added_phone_pattern, contact[5])
            if added:
                added_formatted = re.sub('\s*', '', added.group())
                phone = phone + ' ' + added_formatted
        else:
            phone = ''
    contact[5] = phone
uniq_contacts_list.insert(0, first_line)
with open("phonebook.csv", "w", encoding='utf-8') as f:
  datawriter = csv.writer(f, delimiter=',')
  datawriter.writerows(uniq_contacts_list)
