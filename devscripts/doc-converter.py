import io

filepos = 0

def main():
    # open a test file for reading
    with io.open('test.pwn') as file:
                filepos = 0
                line = file.readline()

                while (line != ""):
                        if (is_open_doc_comment(line)):
                                print 'YSI Doc:'
                                print parse_comment(file)
                                
                        line = file.readline()

def parse_comment(file):
        line = file.readline()
        description = {}

        while (line != ""):
                if is_close_doc_comment(line):
                    line = file.readline()
                    break
                elif is_doc_summary(line):
                       description['summary'], line = get_doc_summary(file)
                elif is_doc_params(line):
                        description['params'], line = get_doc_params(file)
                elif is_note_doc_header(line):
                        description['note'], line = get_doc_note(file)
                elif is_return_doc_header(line):
                        description['return'], line = get_doc_return(file)
                else:
                    # unknown doc header/content consume
                    line = file.readline()
                    
                    print 'doc-converter: ' + line
                    print 'doc-converter: Unknown document header found in comment context'
                    print 'doc-converter: the line has been skipped'
                    
        return description
    
def is_doc_summary(text):
        if is_doc_header('Function', text):
            # print 'doc-converter: Found YSI comment summary'

            return True
        else:
            return False

def is_doc_params(text):
    if is_doc_header('Params', text):
        # print 'doc-converter: Found YSI parameter list'
        
        return True
    else:
        return False

def is_doc_header(header, text):
    stripped = text.lstrip()

    if (stripped.startswith(header + ':')):
        return True
    else:
        return False

def get_doc_params(file):
        line = file.readline()
        params = []
        last_param = {}
        
        while (line != ""):
            if (is_end_doc_section(line)):
                break
            else:
                # Param:
                #   (Name) - (Documentation)
                #   ([A-za-z_][A-Za-z0-9_]+) - (.*)
                param = line.split('-', 1)

                if len(param) < 2:
                    # fppend to the last parameters
                    # documentation
                    last_param[last_param.keys()[0]] += param[0].lstrip()
                else:
                    # Found a new parameter so set last param to
                    # equal it and append it to the parameter list
                    last_param = { param[0].strip(): param[1].lstrip() }
                    params.append(last_param)

            line = file.readline()

        return params, line

def get_doc_summary(file):
    return get_doc_text(file)

def get_doc_note(file):
    return get_doc_text(file)

def get_doc_return(file):
    return get_doc_text(file)

# general method to get chunk of text given that
# header has just been seen. method breaks when
# doc section ends
def get_doc_text(file):
    line = file.readline()
    text = ''

    while (line != ""):
        if is_end_doc_section(line):
            break
        else:
            # get rid of preceding tabs, keep right
            # whitespace (e.g. new lines)
            text += line.lstrip()
        line = file.readline()
    return text, line
    

def is_end_doc_section(text):
        return is_close_doc_comment(text) or \
               is_doc_params(text) or \
               is_doc_summary(text) or \
               is_return_doc_header(text) or \
               is_note_doc_header(text)

def is_return_doc_header(text):
    if is_doc_header('Return', text):
        # print 'doc-converter: Found YSI return documentation'
        
        return True
    else:
        return False

def is_note_doc_header(text):
    if is_doc_header('Notes', text):
        # print 'doc-converter: Found YSI note'
        
        return True
    else:
        return False
    
def is_open_doc_comment(text):
        stripped = text.lstrip()
        
        if (stripped.startswith('/*----------------------------------------------------------------------------*\\')):
                # print 'doc-converter: Found YSI comment opening'
                
                return True
        else:
                return False

def is_close_doc_comment(text):
        stripped = text.lstrip()
        
        if (stripped.startswith('\\*----------------------------------------------------------------------------*/')):
                # print 'doc-converter: Found YSI comment closing'
                
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

