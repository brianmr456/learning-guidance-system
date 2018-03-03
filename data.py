def Syllabus():
    syllabus = [
        {
            'mod_order': '1',
            'mod_id' : '1',
            'type' : 'link',
            'instruction' : 'Go through the first 6 chapters of',
            'content' : {
			'txt': 'Coding Projects in Python.',
			'url': 'https://catalog.midcolumbialibraries.org/polaris/search/title.aspx?ctx=1.1033.0.0.6&pos=1'
		}
        },
        {
            'mod_order': '2',
            'mod_id' : '2',
            'type' : 'video',
            'instruction' : 'Watch Python Programming',
            'content' : 'https://www.youtube.com/embed/N4mEzFDjqtA'
        },
        {
            'mod_order': '3',
            'mod_id' : '4',
            'type' : 'assignment',
            'instruction' : 'Complete this challenge',
            'content' : ['Create a new project', 'Create a new text file and enter a list', 'Add code to project to pull data from text file', 'Add code tot he project to list out the data']
        },
        {
            'mod_order': '4',
            'mod_id' : '3',
            'type': 'link',
            'instruction': 'Read',
            'content': {
                'txt': "Hitchhiker's Guide to Python",
                'url': 'https://catalog.midcolumbialibraries.org/polaris/search/title.aspx?ctx=1.1033.0.0.6&pos=1'
            }
        }
    ]
    return syllabus