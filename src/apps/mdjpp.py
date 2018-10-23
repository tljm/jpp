from jpp.parse import JournalParser

if __name__ == "__main__":

    import argparse

    description = '''MarkDown Journal PreProcessor'''

    parser = argparse.ArgumentParser(description=description,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("-j", action="store", dest="journal_file", required=True, help="Config file filename.")
    
    args = parser.parse_args()


    jp = JournalParser()
    with open(args.journal_file) as jfile:
        jp.proceed(jfile)
        
    jp.finalize()
    
