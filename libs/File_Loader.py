import glob
import imp
import os

def get_objects(folder):
    uri = os.path.normpath(os.path.join(os.path.dirname(__file__), folder))
    fileslist = glob.glob(uri+"/*.py")   
    modules = []
    for f in fileslist:      
        index = f.rfind('_')
        index2 = f.rfind('/')
        if f[index2+1] == '_':          
            modulename = f[index2+2:index]
            my_module = imp.load_source(modulename,f)
            modules.append(my_module)
    return modules