from jpp.options import default_options
from jpp.parse import JournalParser

if __name__ == "__main__":

    import argparse

    description = '''MarkDown Journal PreProcessor'''

    parser = argparse.ArgumentParser(description=description,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("-j", action="store", dest="journal_file", required=True, help="Config file filename.")
    
    for option in (o for o in dir(default_options) if o.startswith('jpp_')):
        name = option[4:]
        parser.add_argument("--%s" % name,
                            action="store",
                            dest=name,
                            required=False,
                            default=getattr(default_options,option),
                            type=type(getattr(default_options,option)))
    
    args = parser.parse_args()


    jp = JournalParser()
    with open(args.journal_file) as jfile:
        jp.proceed(jfile)
        
    jp.finalize() # explicit call
    
