#!/usr/bin/env python
from django.core.management import execute_manager
import os
import sys
#current_directory = os.path.dirname(sys.argv[0])
current_directory ='c:\\Develop\\MoneyDJTV\\MoneyDJTV'
print 'current_directory:'
print current_directory
parent_directory = os.path.dirname(current_directory)
module_name = os.path.basename(current_directory)
sys.path.append(parent_directory)
sys.path.append(current_directory)
os.environ['DJANGO_SETTINGS_MODULE'] = '%s.settings' % 'MoneyDJTV'
print 'os.environ:'
print os.environ['DJANGO_SETTINGS_MODULE'] 
try:
    import settings # Assumed to be in the same directory.
except ImportError:
    import sys
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
    sys.stderr.write("Unexpected error: %r" % sys.exc_info()[0])
    sys.exit(1)

print 'After import settings'
if __name__ == "__main__":
    execute_manager(settings)
