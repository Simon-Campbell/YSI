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
        description = {}

        while (line != ""):
                if (is_close_doc_comment(line)):
                    break
                elif (is_doc_summary(line)):
                       description['summary'], line = get_doc_summary(file)
                elif (is_doc_params(line)):
                        description['params'], line = get_doc_params(file)
                else:
                    line = file.readline()

        print description

def is_doc_summary(text):
        if is_doc_header('Function', text):
            print 'doc-converter: Found YSI comment summary'

            return True
        else:
            return False

def is_doc_params(text):
    if is_doc_header('Params', text):
        print 'doc-converter: Found YSI parameter list'
        
        return True
    else:
        return False

def is_doc_header(header, text):
    stripped = text.lstrip()

    if (stripped.startswith(header + ':')):
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
                
        return summary, line

def get_doc_params(file):
        line = file.readline()
        params = []
        last_param = {}
        is_continued = False
        
        while (line != ""):
            if (is_end_doc_section(line)):
                break
            else:
                # param <= name - documentation
                param = line.split('-', 1)

                if len(param) < 2:
                    print 'continue'
                else:
                    print 'got param'
                    last_param = { param[0].strip(): param[1].strip() }
                    params.append()

            line = file.readline()

        return params, line


def is_end_doc_section(text):
        return is_close_doc_comment(text) or is_doc_params(text) or is_doc_summary(text)
                        
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

