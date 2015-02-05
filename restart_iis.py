import win32serviceutil
import time

def service_info(action, machine, service):
    if action == 'stop': 
        win32serviceutil.StopService(service, machine)
        print '%s stopped successfully' % service
    elif action == 'stop_with_deps':
        win32serviceutil.StopServiceWithDeps(service, machine)
        print '%s stopped successfully with deps' % service
    elif action == 'start':
        win32serviceutil.StartService(service, machine)
        print '%s started successfully' % service
    elif action == 'restart': 
        win32serviceutil.RestartService(service, machine)
        print '%s restarted successfully' % service
    elif action == 'status':
        if win32serviceutil.QueryServiceStatus(service, machine)[1] == 4:
            print "%s is running normally" % service 
        else:
            print "%s is *not* running" % service 

def service_action(action, service):
    service_info(action, 'ip-0AC4EF00', service)

if __name__ == '__main__':
    machine = 'ip-0AC4EF00'
    service = 'Print Spooler'
    service_info('stop', machine, service)
    print "Sleeping for 5 seconds..." 
    time.sleep(5)
    service_info('start', machine, service)