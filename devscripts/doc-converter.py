import io
import glob
import sys

filepos = 0

def main():
    # open a test file for reading
    # 'test.pwn'
    # 'C:/Development/Pawn/YSI/pawno/include/YSI/y_users.inc'
    
    #files = glob.glob('C:\Development\Pawn\YSI\pawno\include\YSI\*.inc')
    files = ['test.pwn', 'y_users.inc']
    
    print 'doc-converter: Found ' + str(len(files)) + ' in YSI include directory.'
    
    for f in files:
        print 'doc-converter: Converting ' + f
        
        convert_file(f)
        
def convert_file(filename):
    output_text = ''
    
    with io.open(filename, 'r') as file:
        line = file.readline()

        while (line != ""):
                if (is_open_doc_comment(line)):
                    func = parse_comment(file)

                    # add PawnDoc'd version to buffer
                    output_text += get_pawn_xml(func)
                else:
                    # add normal line to buffer
                    output_text += line
                    
                line = file.readline()

    with io.open(filename + '.txt', 'w') as file:
        file.write(output_text)

def file_range_replace(file, start, end, text):
    file.seek(0)

    contents = file.read()
    contents = contents.replace(contents[start:end], text)

    print 'file:'
    print contents

    file.seek(end)
    
    #file.write(contents)
    #file.flush()
    
    #file.seek(start + sys.getsizeof(text), io.SEEK_SET)
    
def get_pawn_xml(function):
    pawn_xml = '/**\n'

    if 'summary' in function:
        pawn_xml += ' * <summary>\n' + xml_prettify_data(function['summary'].strip()) + '\n * </summary>\n'

    if 'params' in function:
        for param in function['params']:
            for name, desc in param.items():
                pawn_xml += ' * <param name="'+ name +'">\n' + xml_prettify_data(desc.strip()) + '\n * </param>\n'

    if 'return' in function:
        pawn_xml += ' * <returns>\n' + xml_prettify_data(function['return'].strip()) + '\n * </returns>\n'
        
    if 'note' in function:
        pawn_xml += ' * <remarks>\n' + xml_prettify_data(function['note'].strip()) + '\n * </remarks>\n'
        
    pawn_xml += ' */\n'

    return pawn_xml

def xml_prettify_data(inner, level=1):
    # Takes the inner content of XML and formats it nicely.
    # Level 1 Indent:
    #   ' *  {%inner}'
    #   ' *    {%inner}'

    pretty = ''
    lines  = inner.split('\n')
    
    for line in lines:
        pretty += ' *' + (' ' * level * 2) + line + '\n'

    return pretty.rstrip()

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
                    # unknown doc header/content, consume
                    line = file.readline()
                    
                    # print 'doc-converter: ' + line
                    # print 'doc-converter: Unknown document header found in comment context'
                    # print 'doc-converter: the line has been skipped'
                    
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

