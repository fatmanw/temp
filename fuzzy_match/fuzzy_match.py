#!/usr/bin/env python

import re


demo_list = ['django_migrations.py',
    'django_admin_log.py',
    'main_generator.py',
    'migrations.py',
    'api_user.doc',
    'user_group.doc',
    'accounts.txt',
    ]
    

def fuzzy_finder(user_input, collection):
    suggestion = []
    pattern = '.*?'.join(user_input)
    regex = re.compile(pattern)
    for item in collection:
    	match = regex.search(item)
        if match:
            suggestion.append((len(match.group()), match.start(),item))	
    return [x for _,_,x in sorted(suggestion)]

def main():
    user_input = raw_input()
    print fuzzy_finder(user_input, demo_list)


if __name__ == '__main__':
    main()
   