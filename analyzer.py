location = input("Give address of jsonlz4 extention file with extention: ")

try:
    import lz4.block as lz4
except ImportError:
    import lz4

stdin = open(location, 'rb')
stdout = open('JSON_FORMAT.json', 'wb')


assert stdin.read(8) == b'mozLz40\0'
stdout.write(lz4.decompress(stdin.read()))
stdin.close()
stdout.close()


import json

with open('JSON_FORMAT.json', encoding='utf-8') as f:
    content = json.load(f)


with open('Analysis.txt', 'w', encoding='utf-8') as f:

    # Write the overview of the content.
    for k, v in content.items():
        # Write the key and the type of the value.
        f.write('\n\n{}:  {}\n'.format(k, type(v)))

        # The value could be of a list type, or just one item.
        if isinstance(v, list):
            for e in v:
                f.write('\t{}\n'.format(e))
        else:
            f.write('\t{}\n'.format(v))

    # Write the content of the tabs in each windows.
    f.write('\n\n=======================================================\n\n')
    windows = content['windows']
    for n, w in enumerate(windows, 1):  # the enumerate is used just for numbering the windows
        f.write('\n\tWindow {}:\n'.format(n))
        tabs = w['tabs']
        for tab in tabs:
            # The tab is a dictionary. Display only 'title' and 'url' from 
            # 'entries' subdictionary.
            e = tab['entries'][0]
            f.write('\t\t{}\n\t\t{}\n\n'.format(e['url'], e['title']))
