import json

def rock_group_dict():
    with open('rock_groups.json') as json_file:
        data = json.load(json_file)
    return data

def groups(data):
    groups = []
    for i in range(len(data['rock'])):
        groups.append(data['rock'][i]['name'])
    
    groups_text = ', '.join(groups)

    return groups_text

def description_and_url(data, name):
    for i in range(len(data['rock'])):
        if name in data['rock'][i]['name']:
            return data['rock'][i]['discription'], data['rock'][i]['url']
