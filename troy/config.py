import ConfigParser
import os

CONFIGFILE = os.path.expanduser('~/.troy.ini')

PILOTJOB_TYPES = ('bigjob', 'diane', 'condor')

adaptors = []

config = None

def adaptor_config(adaptor, option):
    
    section = 'troy.adaptors.' + adaptor
    if not config.has_section(section):
        print '[ERROR] adaptor section "%s" not found in config file.' % \
                section
        exit(-1)
    
    value = config.get(section, option)
    
    return value


def read_config():

    print '[INFO] Known Troy adaptor types:', list(PILOTJOB_TYPES)

    global config
    config = ConfigParser.ConfigParser()
    config.read(CONFIGFILE)

    print '[INFO] Looking for adaptors in configuration ...'
    for s in config.sections():
        if s.startswith('troy.adaptors.'):
                
            name = s.split('.', 2)[2]
                
            if name in PILOTJOB_TYPES:
                print "[INFO] %s adaptor entry detected!" % (name)
            else:
                print '[ERROR] Unknown adaptor name:', name
                exit(-1)
                
            if config.getboolean(s, 'enabled'):
                print '[INFO] Status: Enabled'
                adaptors.append(name)
            else:
                print '[INFO] Status: Disabled' 

    print '[INFO] Enabled adaptors found:', list(adaptors)
            
    print '[INFO] General settings:'
    for s in config.defaults():
        print s
        
        
        
if __name__ == '__main__':
    read_config()
    
    c = adaptor_config('bigjob', 'coordination_url')
    print c