import io

filepos = 0

def main():
    # open a test file for reading
    with io.open('test.pwn') as file:
                filepos = 0
                line = file.readline()

                while (line != ""):
                        if (is_open_doc_comment(line)):                              
                                parse_comment(file)
                                
                        line = file.readline()

def parse_comment(file):
        line = file.readline()

        while (line != ""):
                if (is_close_doc_comment(line)):
                        break
                elif (is_doc_summary(line)):
                        print get_doc_summary(file)

                line = file.readline()

def is_doc_summary(text):
        stripped = text.lstrip()

        if (stripped.startswith('Function:')):
                print 'doc-converter: Found YSI comment summary'

                return True
        else:
                return False

def get_doc_summary(file):
        line = file.readline()
        summary = ''

        while (line != ""):
                if (is_end_doc_section(line)):
                        break
                else:
                        summary += line

                line = file.readline()
                
        return summary

def is_end_doc_section(text):
        return is_close_doc_comment(text)
                        
def is_open_doc_comment(text):
        stripped = text.lstrip()
        
        if (stripped.startswith('/*----------------------------------------------------------------------------*\\')):
                print 'doc-converter: Found YSI comment opening'
                
                return True
        else:
                return False

def is_close_doc_comment(text):
        stripped = text.lstrip()
        
        if (stripped.startswith('/*----------------------------------------------------------------------------*\\')):
                print 'doc-converter: Found YSI comment closing'
                
                return True
        else:
                return False
        
        
def make_intermediate(text):
    # convert text to an intermediate form
    pass
    
def convert_function(intermediate):
    # Convert an intermediate to a string representation
    # which can be dumped to a file
    pass

class YsiParser( object ):
    # Parse a YSI function header to
    # a FunctionDescriptor
    pass
    
# Generate PawnDocs using a FunctionDescriptor
# object
class PawnDocGenerator( object ):   
    def get_as_string():
        pawndoc = ''
    
class FunctionDescriptor( object ):
    # Describe a function
    summary = ''
    returns = ''
    params  = []
    notes   = ''
    
if __name__ == "__main__":
    main()

