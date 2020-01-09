import webbrowser
import json
import sys


def saver():

    location = "/home/kush/.mozilla/firefox/56s5hya4.default/sessionstore-backups/recovery.jsonlz4"
    try:
        import lz4.block as lz4
    except ImportError:
        import lz4

    stdin = open(location, 'rb')
    # name of file here
    stdout = open(
        '/home/kush/.mozilla/firefox/56s5hya4.default/sessionstore-backups/decrypted_state.json', 'wb')

    assert stdin.read(8) == b'mozLz40\0'
    stdout.write(lz4.decompress(stdin.read()))
    stdin.close()
    stdout.close()


def opener():
    with open('/home/kush/.mozilla/firefox/56s5hya4.default/sessionstore-backups/decrypted_state.json', encoding='utf-8') as f:
        content = json.load(f)

    # The loaded content is a dictionary. List the keys first (console).
    for k in content:
        print(k)

    # Now list the content bound to the keys. As the console may not be capable
    # to display all characters, write it to the file.
    with open('/home/kush/.mozilla/firefox/56s5hya4.default/sessionstore-backups/thorugh_analysis.txt', 'w', encoding='utf-8') as f:

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
        window_url = []
        counter = -1
        # the enumerate is used just for numbering the windows
        for n, w in enumerate(windows, 1):
            f.write('\n\tWindow {}:\n'.format(n))
            tabs = w['tabs']
            window_url.append(list())
            counter += 1
            for tab in tabs:
                # The tab is a dictionary. Display only 'title' and 'url' from
                # 'entries' subdictionary.
                e = tab['entries'][0]
                f.write('\t\t{}\n\t\t{}\n\n'.format(e['url'], e['title']))
                window_url[counter].append(e['url'])

    for window in window_url:
        counter = 0
        for tab in window:
            if counter == 0:
                webbrowser.open(tab, new=1, autoraise=True)
                counter += 1
            else:
                webbrowser.open(tab, new=2, autoraise=True)


if __name__ == "__main__":
    if sys.argv[1] == 'save':
        saver()
    elif sys.argv[1] == 'open':
        opener()
    else:
        print('Abee saale')
        print(sys.argv)
