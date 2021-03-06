import subprocess
import sys

class zabbix_check(object):
    def __init__(self, source, destination, protocol, port):
        self.source       = source
        self.destination  = destination
        self.protocol     = protocol
        self.port         = port

    def _zabbix_get_tcp(self, source, destination, port):
        tcp_output = subprocess.check_output(["zabbix_get", "-s", source, "-k", "net.tcp.port[" + destination + "," + port + "]"]).strip()
        return tcp_output

    def _zabbix_get_ntp(self, source, destination, port):
        ntp_output = subprocess.check_output(["zabbix_get", "-s", source, "-k", "net.udp.service[ntp," + destination + "," + port + "]"]).strip()
        return ntp_output

    def _zabbix_get_dns(self, source, destination, port):
        dns_output = subprocess.check_output(["zabbix_get", "-s", source, "-k", "net.dns[" + destination + "]"]).strip()
        return dns_output

    def _zabbix_agent_ping(self, source):
        try:
            subprocess.check_output(["zabbix_get", "-s", source, "-k", "agent.ping"]).strip()
            return "agent alive"
        except:
            return source + " is unreachable or don't have zabbix agent installed"

    def zabbix_get(self):

        agent_status = self._zabbix_agent_ping(self.source)
        if agent_status != 'agent alive':
            return agent_status
            sys.exit(1)

        if self.protocol == 'tcp':
            result = self._zabbix_get_tcp(self.source, self.destination, self.port)
        elif self.protocol == 'ntp':
            result = self._zabbix_get_ntp(self.source, self.destination, self.port)
        elif self.protocol == 'dns':
            result = self._zabbix_get_dns(self.source, self.destination, self.port)

	if result == '1':
	    return "Success! Connection established successfully from " + self.source + " to " + self.destination + " on " + self.protocol + " port " + self.port 
	elif result == '0':
	    return "Failed! Cannot connect from " + self.source + " to " + self.destination + " on " + self.protocol + " port " + self.port
	else:
	    return "abcd"
