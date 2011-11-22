'''
Created on Mar 17, 2011

@author: mattf

purpose:  to allow basic json serialization/loading in case the python interpreter
doesn't have the standard distribution json module at its disposal (this is the case
for python version 2.5 and earlier).

notes:  uses 'eval' to convert string to json object -- possible security risk in the
case of loading untrusted strings.
'''

def toJSON(jsObj):
    if type(jsObj) == dict:
        jsonText = objectToJSON(jsObj)
    elif type(jsObj) == list:
        jsonText = arrayToJSON(jsObj)
    elif type(jsObj) == str:
        jsonText = stringToJSON(jsObj)
    elif type(jsObj) == tuple:
        jsonText = arrayToJSON(list(jsObj))
    else:
        jsonText = str(jsObj)
    return jsonText


dumps = toJSON # alias for compatibility with standard library json module


def load(file): # alias for reading from a file
    return eval(file.read())


def test():
    print toJSON(range(1,9))
    print toJSON({3 : 4})
    print toJSON('what"quotation mark')
    x = toJSON({'test1' : 'hello', 'the second test' : 75})
    print x
    print toJSON([])
    print toJSON({})
    print toJSON("")
    print toJSON(0)
    print toJSON(0.03)
    print toJSON((3,4)) # no tuples in json!
#    print json.loads(x)


def objectToJSON(o):
    elems = [stringToJSON(str(k)) + ":" + toJSON(o[k]) for k in o.keys()]
    if len(elems) == 0:
        middle = ''
    else:
        middle = ','.join(elems)
        #middle = reduce(lambda x,y: x + ", " + y, elems)
    return '{' + middle + '}'


def arrayToJSON(a):
    elems = [toJSON(e) for e in a]
    if len(elems) == 0:
        middle = ''
    else:
        middle = ','.join(elems)
        #middle = reduce(lambda x,y: x + ", " + y, elems)
    return '[' + middle + ']'


def stringToJSON(s):
    escaped = escapeString(s)
    return '"' + escaped + '"'


def escapeString(s):
    s = s.replace('\\', '\\\\')
    s = s.replace('"', '\\"')
    return s

if __name__ == "__main__":
    test()
