

if __name__ == "__main__":

    import argparse

    description = '''MarkDown Journal PreProcessor'''

    parser = argparse.ArgumentParser(description=description,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("-j", action="store", dest="journal_file", required=True, help="Config file filename.")

