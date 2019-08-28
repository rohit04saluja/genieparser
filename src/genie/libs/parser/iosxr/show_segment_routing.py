#!/bin/env python
import re

# Genie
from genie.metaparser import MetaParser
from genie.metaparser.util.schemaengine import Schema, Any, Optional

class ShowSegmentRoutingPrefixSidMapSchema(MetaParser):
    ''' Schema for:
          *  show isis segment-routing prefix-sid-map active-policy
          *  show isis segment-routing prefix-sid-map backup-policy
        '''
    schema = {
        Any() : {
            'name' : str,
            Any() : {
                'status' : bool,
                'entries' : int,
                'algorithm' : {
                    'prefix' : str,
                    'sid_index' : int,
                    'range' : int,
                    Optional('flags'): str,
                },
                Optional('isis_id'): int,
                Optional('process_id') : int,
            },
        }
    }


class ShowSegmentRoutingPrefixSidMap(ShowSegmentRoutingPrefixSidMapSchema):
    ''' Parser for:
          *  show isis segment-routing prefix-sid-map active-policy
          *  show isis segment-routing prefix-sid-map backup-policy
        '''

    cli_command = 'show isis segment-routing prefix-sid-map {status}'

    def cli(self, output= None):
        if output is None:
            out = self.device.execute(self.cli_command)
        else:
            out = output
        
        ret_dict = {}

        p1 = re.compile(r'RP\/0\/0\/CPU0:router# show '
            '(?P<name>\w+)\s+segment-routing prefix-sid-map '
            '(?P<status>\w+)-policy$')
        
        p2 = re.compile(r'^SRMS \w+ policy for Process ID (?P<process_id>\d+)$')
        
        p3 = re.compile(r'^IS-IS (?P<isis_id>\d+) \w+ policy$')

        p4 = re.compile(r'(?P<prefix>[\w\.\/]+)\s+(?P<sid_index>\d+)'
            '\s+(?P<range>\d+)(\s+(?P<flags>)[\w\s]+$)?')
        
        p5 = re.compile(r'Number of mapping entries:\s+(?P<entries>\d+)')

        for line in out.splitlines():
            line = line.strip()
        
            # RP/0/0/CPU0:router# show isis \
                        # segment-routing prefix-sid-map active-policy
            m = p1.match(line)
            if m:
                status_bool = True if 'active' in \
                        m.groupdict()['status'].lower()\
                    else False
                name = m.groupdict()['name']
                status = m.groupdict()['status']

                router_dict = ret_dict.setdefault(name, {})
                router_dict['name'] = name
                status_dict = router_dict.setdefault(status, {})
                status_dict['status'] = status_bool

            # SRMS active policy for Process ID 1
            m = p2.match(line)
            if m:
                status_dict.setdefault('process_id', \
                    int(m.groupdict()['process_id']))
            
            # IS-IS 1 active policy
            m = p3.match(line)
            if m:
                status_dict.setdefault('isis_id', int(m.groupdict()['isis_id']))


            # Prefix               SID Index    Range        Flags
            # 1.1.1.100/32         100          20          
            # 1.1.1.150/32         150          10          
            m = p4.match(line)
            if m:
                algo_dict = status_dict.setdefault('algorithm', {})
                algo_dict.setdefault('prefix', m.groupdict()['prefix'])
                algo_dict.setdefault('sid_index', \
                                            int(m.groupdict()['sid_index']))
                algo_dict.setdefault('range', int(m.groupdict()['range']))
                if 'flag' in line.lower():
                    algo_dict.setdefault('flags', m.groupdict()['flags'])

            # Number of mapping entries: 2
            m = p5.match(line)
            if m:
                status_dict['entries'] = int(m.groupdict()['entries'])
        
        return ret_dict


class ShowPceIPV4PeerSchema(MetaParser):
    ''' Schema for:
        * show pce ipv4 peer
    '''
    schema = {
        'database' : {
            Any() : {
                'peer_address' : str,
                'state' : bool,
                'capabilities' : {
                    'stateful' : bool,
                    'segment-routing' : bool,
                    'update' : bool
                }
            },
        }
    }

class ShowPceIPV4Peer(ShowPceIPV4PeerSchema):
    ''' Parser for:
        * show pce ipv4 peer
    '''
    cli_command = 'show pce ipv4 peer'

    def cli(self, output = None):
        if output is None:
            out = self.device.execute(self.cli_command)
        else:
            out = output

        ret_dict = {}

        # Peer address: 192.168.0.1
        p1 = re.compile(r'^Peer address: (?P<address>[\d\.]+)$')

        p2 = re.compile(r'^State: (?P<state>\w+)$')

        p3 = re.compile(r'Capabilities: (?P<stateful>\w+)\,\s+'
            '(?P<segment_routing>[\w\-]+)\,\s+(?P<update>\w+)$')
            

        for line in out.splitlines():
            line = line.strip()

            m = p1.match(line)
            if m:
                address = m.groupdict()['address']
                database_dict = ret_dict.setdefault('database', {})
                address_dict = database_dict.setdefault(address, {})
                address_dict['peer_address'] = address

            m = p2.match(line)
            if m:
                state_bool = True if 'up' in \
                    m.groupdict()['state'].lower() else False
                address_dict['state'] = state_bool

            m = p3.match(line)
            if m:
                capabilities_dict = address_dict.setdefault('capabilities', {})
                
                stateful_bool = True if 'stateful' in \
                    m.groupdict()['stateful'].lower() else False
                segment_bool = True if 'segment-routing' in \
                    m.groupdict()['segment_routing'].lower() else False
                update_bool = True if 'update' in \
                    m.groupdict()['update'].lower() else False
                
                capabilities_dict['stateful'] = stateful_bool
                capabilities_dict['segment-routing'] = segment_bool
                capabilities_dict['update'] = update_bool
        return ret_dict


class ShowPceIPV4PeerDetailSchema(MetaParser):
    ''' Schema for:
        * show pce ipv4 peer detail
    '''
    schema = {
        'database' : {
            Any() : {
                'peer_address' : str,
                'state' : bool,
                'capabilities' : {
                    'stateful' : bool,
                    'segment-routing' : bool,
                    'update' : bool
                },
                'pcep' : {
                    'pcep_uptime': str,
                    'pcep_local_id': int,
                    'pcep_remote_id': int,              
                },
                'ka' : {
                    'sending_intervals': int,
                    'minimum_acceptable_inteval': int,
                },
                'peer_timeout': int,
                'statistics' : {
                    'rx' : {
                        'keepalive_messages' : int,
                        'request_messages' : int,
                        'reply_messages' : int,
                        'error_messages' : int,
                        'open_messages' : int,
                        'report_messages' : int,
                        'update_messages' : int,
                        'initiate_messages' : int,
                    },
                    'tx' : {
                        'keepalive_messages' : int,
                        'request_messages' : int,
                        'reply_messages' : int,
                        'error_messages' : int,
                        'open_messages' : int,
                        'report_messages' : int,
                        'update_messages' : int,
                        'initiate_messages' : int,
                    },
                }
            }
        }
    }

class ShowPceIPV4PeerDetail(ShowPceIPV4PeerDetailSchema):
    ''' Parser for:
        * show pce ipv4 peer detail
    '''

    cli_command = 'show pce ipv4 peer detail'

    def cli(self,output=None):
        if output is None:
            out = self.device.execute(self.cli_command)
        else:
            out = output

        ret_dict = {}

        p1 = re.compile(r'^Peer address: (?P<address>[\d\.]+)$')

        p2 = re.compile(r'^State: (?P<state>\w+)$')

        p3 = re.compile(r'^Capabilities: (?P<stateful>\w+)\,\s+'
                            '(?P<segment_routing>[\w\-]+)\,\s+(?P<update>\w+)$')

        p4 = re.compile(r'^PCEP has been up for: (?P<pcep_up_time>[\w+\:]+)$')

        p5 = re.compile(r'^PCEP session ID: local (?P<local_id>\d+)\, remote '
                                                        '(?P<remote_id>\d+)$')

        p6 = re.compile(r'^Sending KA every (?P<ka_time_intervals>\d+)'
                                                                '\s+seconds$')

        p7 = re.compile(r'^Minimum acceptable KA interval: '
                                    '(?P<minimum_ka_interval>\d+)\s+seconds$')

        p8 = re.compile(r'^Peer timeout after (?P<peer_timeout>\d+)\sseconds$')

        p9 = re.compile(r'^Keepalive messages:\s+rx\s+'
        '(?P<keepalive_messages_rx>\d+)\s+tx\s+(?P<keepalive_messages_tx>\d+)$')

        p10 = re.compile(r'Request messages:\s+rx\s+(?P<request_messages_rx>'
                                    '\d+)\s+tx\s+(?P<request_messages_tx>\d+)$')

        p11 = re.compile(r'^Reply messages:\s+rx\s+(?P<reply_messages_rx>\d+)'
                                        '\s+tx\s+(?P<reply_messages_tx>\d+)$')

        p12 = re.compile(r'^Error messages:\s+rx\s+(?P<error_messages_rx>\d+)'
                                        '\s+tx\s+(?P<error_messages_tx>\d+)$')

        p13 = re.compile(r'^Open messages:\s+rx\s+(?P<open_messages_rx>\d+)\s+'
                                            'tx\s+(?P<open_messages_tx>\d+)$')

        p14 = re.compile(r'^Report messages:\s+rx\s+(?P<report_messages_rx>\d+)'
                                        '\s+tx\s+(?P<report_messages_tx>\d+)$')

        p15 = re.compile(r'^Update messages:\s+rx\s+(?P<update_messages_rx>\d+)'
                                        '\s+tx\s+(?P<update_messages_tx>\d+)$')

        p16 = re.compile(r'^Initiate messages:\s+rx\s+(?P<initiate_messages_rx>'
                                '\d+)\s+tx\s+(?P<initiate_messages_tx>\d+)$')
            
        for line in out.splitlines():
            line = line.strip()

            m = p1.match(line)
            if m:
                address = m.groupdict()['address']
                database_dict = ret_dict.setdefault('database', {})
                address_dict = database_dict.setdefault(address, {})
                address_dict['peer_address'] = address

            m = p2.match(line)
            if m:
                state_bool = True if 'up' in \
                    m.groupdict()['state'].lower() else False
                address_dict['state'] = state_bool

            m = p3.match(line)
            if m:
                capabilities_dict = address_dict.setdefault('capabilities', {})
                
                stateful_bool = True if 'stateful' in \
                    m.groupdict()['stateful'].lower() else False
                segment_bool = True if 'segment-routing' in \
                    m.groupdict()['segment_routing'].lower() else False
                update_bool = True if 'update' in \
                    m.groupdict()['update'].lower() else False
                
                capabilities_dict['stateful'] = stateful_bool
                capabilities_dict['segment-routing'] = segment_bool
                capabilities_dict['update'] = update_bool

            m = p4.match(line)
            if m:
                pcep_dict = address_dict.setdefault('pcep', {})
                pcep_dict['pcep_uptime'] = m.groupdict()['pcep_up_time']
            
            m = p5.match(line)
            if m:
                pcep_dict['pcep_local_id'] = int(m.groupdict()['local_id'])
                pcep_dict['pcep_remote_id'] = int(m.groupdict()['remote_id'])

            m = p6.match(line)
            if m:
                ka_dict = address_dict.setdefault('ka', {})
                ka_dict['sending_intervals'] = \
                                        int(m.groupdict()['ka_time_intervals'])

            m = p7.match(line)
            if m:
                ka_dict['minimum_acceptable_inteval'] = \
                                    int(m.groupdict()['minimum_ka_interval'])

            m = p8.match(line)
            if m:
                peer_timeout = int(m.groupdict()['peer_timeout'])
                address_dict.setdefault('peer_timeout', peer_timeout)
            
            m = p9.match(line)
            if m:
                stats_dict = address_dict.setdefault('statistics', {})
                rx_dict = stats_dict.setdefault('rx', {})
                tx_dict = stats_dict.setdefault('tx', {})

                rx_dict['keepalive_messages'] = \
                                    int(m.groupdict()['keepalive_messages_rx'])
                tx_dict['keepalive_messages'] = \
                                    int(m.groupdict()['keepalive_messages_tx'])
            
            m = p10.match(line)
            if m:
                rx_dict['request_messages'] = \
                                    int(m.groupdict()['request_messages_rx'])
                tx_dict['request_messages'] = \
                                    int(m.groupdict()['request_messages_tx'])

            m = p11.match(line)
            if m:
                rx_dict['reply_messages'] = \
                                        int(m.groupdict()['reply_messages_rx'])
                tx_dict['reply_messages'] = \
                                        int(m.groupdict()['reply_messages_tx'])

            m = p12.match(line)
            if m:
                rx_dict['error_messages'] = \
                                        int(m.groupdict()['error_messages_rx'])
                tx_dict['error_messages'] = \
                                        int(m.groupdict()['error_messages_tx'])

            m = p13.match(line)
            if m:
                rx_dict['open_messages'] = \
                                        int(m.groupdict()['open_messages_rx'])
                tx_dict['open_messages'] = \
                                         int(m.groupdict()['open_messages_tx'])

            m = p14.match(line)
            if m:
                rx_dict['report_messages'] = \
                                     int(m.groupdict()['report_messages_rx'])
                tx_dict['report_messages'] = \
                                     int(m.groupdict()['report_messages_tx'])

            m = p15.match(line)
            if m:
                rx_dict['update_messages'] = \
                                       int(m.groupdict()['update_messages_rx'])
                tx_dict['update_messages'] = \
                                        int(m.groupdict()['update_messages_tx'])

            m = p16.match(line)
            if m:
                rx_dict['initiate_messages'] = \
                                    int(m.groupdict()['initiate_messages_rx'])
                tx_dict['initiate_messages'] = \
                                    int(m.groupdict()['initiate_messages_tx'])
        
        return ret_dict


class ShowPceIPV4PeerprefixSchema(MetaParser):
    ''' Schema for:
        * show pce ipv4 prefix
    '''
    schema = {
        'prefix' :{
            Any() : {
                'node' : int,
                'te_router_id': str,
                'host_name': str,
                Any() : {
                    'system_id' : str,
                    'level' : int,
                },
                'advertised_prefixes': str,
            }
        }
    }

class ShowPceIPV4PeerPrefix(ShowPceIPV4PeerprefixSchema):
    ''' Parser for:
        * show pce ipv4 prefix
    '''

    cli_command = 'show pcs ipv4 prefix'
    
    def cli(self, output = None):
        if output is None:
            out = self.device.execute(self.cli_command)
        else:
            out = output

        ret_dict = {}

        p1 = re.compile(r'Node (?P<node_number>\d+)')

        p2 = re.compile(r'^TE router ID: (?P<router_id>[\d\.]+)$')

        p3 = re.compile(r'^Host name: (?P<host_name>\w+)$')

        p4 = re.compile(r'^ISIS system ID: (?P<system_id>[\w\.]+)'
                                        '\s+level-(?P<system_id_level>\d+)$')

        p5 = re.compile(r'^(?P<adv_prefixes>[\w\.]+)$')

        for line in out.splitlines():
            line = line.strip()

            m = p1.match(line)
            if m:
                node = int(m.groupdict()['node_number'])
                prefix_dict = ret_dict.setdefault('prefix', {})
                node_dict = prefix_dict.setdefault(node, {})

                node_dict['node'] = node

            m = p2.match(line)
            if m:
                node_dict['te_router_id'] = m.groupdict()['router_id']
            
            m = p3.match(line)
            if m:
                node_dict['host_name'] = m.groupdict()['host_name']
            
            m = p4.match(line)
            if m:
                sys_id = m.groupdict()['system_id']
                sys_dict = node_dict.setdefault(sys_id, {})

                sys_dict['system_id'] = sys_id
                sys_dict['level'] = int(m.groupdict()['system_id_level'])

            m = p5.match(line)
            if m:
                node_dict['advertised_prefixes'] = m.groupdict()['adv_prefixes']

        return ret_dict

class ShowPceIpv4TopologySummarySchema(MetaParser):
    ''' Schema for:
        * show pce ipv4 topology summary
    '''
    schema = {
        'summary' : {
            'topology_nodes' : int,
            'prefixes' : {
                'prefixes' : int,
                'prefix_sids' : int,
            },
            'links' : {
                'links' : int,
                'adjancency_sids': int,
            }
        }
    }

class ShowPceIpv4TopologySummary(ShowPceIpv4TopologySummarySchema):
    ''' parser for:
        * show pce ipv4 topology summary
    '''

    cli_command = 'show pce ipv4 topology summary'

    def cli(self, output = None):
        if output is None:
            out = self.device.execute(self.cli_command)
        else:
            out = output

        p1 = re.compile(r'^Topology nodes:\s+(?P<topology_nodes>\d+)$')

        p2 = re.compile(r'^Prefixes:\s+(?P<prefixes>\d+)$')

        p3 = re.compile(r'^Prefix SIDs:\s+(?P<prefix_sids>\d+)$')
        
        p4 = re.compile(r'^Links:\s+(?P<links>\d+)$')

        p5 = re.compile(r'^Adjacency SIDs:\s+(?P<adj_sids>\d+)$')

        ret_dict = {}

        for line in out.splitlines():
            line = line.strip()

            m = p1.match(line)
            if m:
                topology_dict = ret_dict.setdefault('summary', {})
                topology_dict['topology_nodes'] = \
                                            int(m.groupdict()['topology_nodes'])

            m = p2.match(line)
            if m:
                prefix_dict = topology_dict.setdefault('prefixes', {})
                prefix_dict['prefixes'] = int(m.groupdict()['prefixes'])

            m = p3.match(line)
            if m:
                prefix_dict['prefix_sids'] = int(m.groupdict()['prefix_sids'])

            m = p4.match(line)
            if m:
                links_dict = topology_dict.setdefault('links', {})
                links_dict['links'] = int(m.groupdict()['links'])

            m = p5.match(line)
            if m:
                links_dict['adjancency_sids'] = int(m.groupdict()['adj_sids'])
        
        return ret_dict

class ShowPceLspSchema(MetaParser):
    ''' Schema for:
            show pce lsp
    '''
    schema = {
        'pcc' : {
            Any() : {
                'pcc' : str,
                'tunnel_name' : str,
                'lsps' : {
                    Any() : {
                        'lsp_number' : int,
                        'source': str,
                        'destination': str,
                        'tunnel_id' : int,
                        'lsp_id' : int,
                        'state' : {
                            'admin' : bool,
                            'operation' : bool,
                        },
                        'setup_type' : str,
                        'binding_sid' : int
                    },
                }
            },
        }

    }
class ShowPceLsp(ShowPceLspSchema):
    ''' Parser for:
            show pce lsp
    '''

    cli_command = 'show pce lsp'

    def cli(self, output = None):
        if output is None:
            out = self.device.execute(self.cli_command)
        else:
            out = output
        
        p1 = re.compile(r'^PCC (?P<pcc_id>[\d\.]+):$')

        p2 = re.compile(r'^Tunnel Name: (?P<tunnel_name>\w+)$')

        p3 = re.compile(r'^LSP\[(?P<lsp_number>\d+)\]:$')

        p4 = re.compile(r'^source (?P<lsp_source>[\d\.]+), destination '
                '(?P<lsp_destination>[\d\.]+), tunnel ID (?P<tunnel_id>\d+), '
                'LSP ID (?P<lsp_id>\d+)$')

        p5 = re.compile(r'State: Admin (?P<admin_state>\w+), Operation '
                                                    '(?P<operation_state>\w+)$')

        p6 = re.compile(r'^Setup type: (?P<setup_type>[\w\s]+)$')

        p7 = re.compile(r'^Binding SID: (?P<binding_sid>\d+)$')

        ret_dict = {}

        for line in out.splitlines():
            line = line.strip()

            m = p1.match(line)
            if m:
                pcc_id = m.groupdict()['pcc_id']
                pccs_dict = ret_dict.setdefault('pcc', {})

                pcc_dict = pccs_dict.setdefault(pcc_id, {})
                pcc_dict['pcc'] = pcc_id

            m = p2.match(line)
            if m:
                pcc_dict['tunnel_name'] = m.groupdict()['tunnel_name']

            m = p3.match(line)
            if m:
                lsp_numb = int(m.groupdict()['lsp_number'])

                lsps_dict = pcc_dict.setdefault('lsps', {})
                lsp_dict = lsps_dict.setdefault(lsp_numb, {})

                lsp_dict['lsp_number'] = lsp_numb

            m = p4.match(line)
            if m:
                lsp_dict['source'] = m.groupdict()['lsp_source']
                lsp_dict['destination'] = m.groupdict()['lsp_destination']
                lsp_dict['tunnel_id'] = int(m.groupdict()['tunnel_id'])
                lsp_dict['lsp_id'] = int(m.groupdict()['lsp_id'])

            m = p5.match(line)
            if m:
                admin_bool = True if 'up' in \
                                m.groupdict()['admin_state'].lower() else False
                operation_bool = True if 'up' in \
                            m.groupdict()['operation_state'].lower() else False
                state_dict = lsp_dict.setdefault('state', {})

                state_dict['admin'] = admin_bool
                state_dict['operation'] = operation_bool

            m = p6.match(line)
            if m:
                lsp_dict['setup_type'] = m.groupdict()['setup_type']

            m = p7.match(line)
            if m:
                lsp_dict['binding_sid'] = int(m.groupdict()['binding_sid'])

        return ret_dict

class ShowPceLspDetailSchema(MetaParser):
    ''' Schema for:
       * show pce lsp detail
    '''
    schema = {
        'pcc' : {
            Any() : {
                'pcc' : str,
                'tunnel_name' : str,
                'lsps' : {
                    Any() : {
                        'lsp_number' : int,
                        'source': str,
                        'destination': str,
                        'tunnel_id' : int,
                        'lsp_id' : int,
                        'state' : {
                            'admin' : bool,
                            'operation' : bool,
                        },
                        'setup_type' : str,
                        'binding_sid' : int,
                        'pcep_information' : {
                            'plsp_id' : int,
                            'plsp_flags' : str,
                        },
                        'paths' : {
                            Any() : {
                                Optional('path') : str,
                                Optional('metric_type') : str,
                                Optional('accumulated_metric') : int,
                                Optional('none'): str,
                                Optional('sids'): {
                                    Any() : {
                                        'sid_number' : int,
                                        'sid_label' : int,
                                        'sid_local_address': str,
                                        'sid_remote_address': str,
                                    },
                                },
                            },
                        },
                    },
                    'event_history' : {
                        Any() : {
                            'time' : str,
                            Any() : {
                                'event' : str,
                                'symbolic_name' : str,
                                Optional('lsp-id'): int,
                                Optional('plsp-id'): int,
                                Optional('source') : str,
                                Optional('destination') : str,
                                Optional('flags') : {
                                    'd' : int,
                                    'r' : int,
                                    'a' : int,
                                    'o' : int,
                                    'sig_bw' : int,
                                    'act_bw' : int,
                                },
                                Optional('peer') : str,
                            },
                        },
                    }
                }
            },
        }
    }

class ShowPceLspDetail(ShowPceLspDetailSchema):
    ''' Parser for:
       * show pce lsp detail
    '''

    cli_command = 'show pce lsp detail'

    def cli(self, output = None):
        if output is None:
            out = self.device.execute(self.cli_command)
        else:
            out=output
        
        p1 = re.compile(r'^PCC (?P<pcc_id>[\d\.]+):$')

        p2 = re.compile(r'^Tunnel Name: (?P<tunnel_name>\w+)$')

        p3 = re.compile(r'^LSP\[(?P<lsp_number>\d+)\]:$')

        p4 = re.compile(r'^source (?P<lsp_source>[\d\.]+), destination '
                            '(?P<lsp_destination>[\d\.]+), tunnel ID '
                            '(?P<tunnel_id>\d+), LSP ID (?P<lsp_id>\d+)$')

        p5 = re.compile(r'State: Admin (?P<admin_state>\w+), Operation '
                                                    '(?P<operation_state>\w+)$')

        p6 = re.compile(r'^Setup type: (?P<setup_type>[\w\s]+)$')

        p7 = re.compile(r'^Binding SID: (?P<binding_sid>\d+)$')

        p8 = re.compile(r'^plsp-id (?P<plsp_id>\d+), flags:'
                                                ' (?P<plsp_flags>[\w\s\:]+)$')

        #   Reported path: 
        p9 = re.compile(r'^(?P<specified_path>\w+) path:$')

        p10 = re.compile(r'^Metric type: (?P<metric_type>\w+), '
                            'Accumulated Metric (?P<accumulated_metric>\d+)$')

        # SID[0]: Adj, Label 24000, Address: local 10.10.10.1 remote 10.10.10.2
        p11 = re.compile(r'^SID\[(?P<sid_number>\d+)\]: Adj, Label '
                            '(?P<sid_label>\d+), Address: local '
                            '(?P<sid_local_address>[\d\.]+) remote '
                            '(?P<sid_remote_address>[\d\.]+)$')
        p11_1 = re.compile(r'None')
        # June 13 2016 13:28:29     Report
        p12 = re.compile(r'^(?P<event_time>\w+ \d+ \d+ [\d\:]+)\s+ '
                                                        '(?P<event_type>\w+)$')
        # Symbolic-name: rtrA_t1, LSP-ID: 2,
        p13 = re.compile(r'^Symbolic-name: (?P<symbolic_name>\w+), '
                                '(?P<id_name>[\w\-]+): (?P<symbolic_id>\d+),$')
        # Source: 192.168.0.1 Destination: 192.168.0.4,
        p14 = re.compile(r'^Source: (?P<event_source>[\d\.]+) Destination: '
                                                '(?P<dest_source>[\d\.]+),$')

        # D:1, R:0, A:1 O:1, Sig.BW: 0, Act.BW: 0
        p15 = re.compile(r'^D:(?P<d_event>\d+), R:(?P<r_event>\d+), '
                            'A:(?P<a_event>\d+) O:(?P<o_event>\d+), Sig\.BW: '
                            '(?P<event_sig>\d+), Act.BW: (?P<event_act>\d+)$')

        p16 = re.compile(r'Peer: (?P<event_peer>[\d\.]+)')

        ret_dict = {}

        for line in out.splitlines():
            line = line.strip()

            m = p1.match(line)
            if m:
                pcc_id = m.groupdict()['pcc_id']
                pccs_dict = ret_dict.setdefault('pcc', {})

                pcc_dict = pccs_dict.setdefault(pcc_id, {})
                pcc_dict['pcc'] = pcc_id

            m = p2.match(line)
            if m:
                pcc_dict['tunnel_name'] = m.groupdict()['tunnel_name']

            m = p3.match(line)
            if m:
                lsp_numb = int(m.groupdict()['lsp_number'])

                lsps_dict = pcc_dict.setdefault('lsps', {})
                lsp_dict = lsps_dict.setdefault(lsp_numb, {})

                lsp_dict['lsp_number'] = lsp_numb

            m = p4.match(line)
            if m:
                lsp_dict['source'] = m.groupdict()['lsp_source']
                lsp_dict['destination'] = m.groupdict()['lsp_destination']
                lsp_dict['tunnel_id'] = int(m.groupdict()['tunnel_id'])
                lsp_dict['lsp_id'] = int(m.groupdict()['lsp_id'])

            m = p5.match(line)
            if m:
                admin_bool = True if 'up' in \
                                m.groupdict()['admin_state'].lower() else False
                operation_bool = True if 'up' in \
                            m.groupdict()['operation_state'].lower() else False
                state_dict = lsp_dict.setdefault('state', {})

                state_dict['admin'] = admin_bool
                state_dict['operation'] = operation_bool

            m = p6.match(line)
            if m:
                lsp_dict['setup_type'] = m.groupdict()['setup_type'].lower()

            m = p7.match(line)
            if m:
                lsp_dict['binding_sid'] = int(m.groupdict()['binding_sid'])

            m = p8.match(line)
            if m:
                pcep_info_dict = lsp_dict.setdefault('pcep_information', {})
                pcep_info_dict['plsp_id'] = int(m.groupdict()['plsp_id'])
                pcep_info_dict['plsp_flags'] = \
                                            m.groupdict()['plsp_flags'].lower()

            m = p9.match(line)
            if m:
                path = m.groupdict()['specified_path'].lower()
                path_dict = lsp_dict.setdefault('paths', {}).setdefault(path,{})

                path_dict['path'] = path
            
            m = p10.match(line)
            if m:
                path_dict['metric_type'] = m.groupdict()['metric_type'].lower()
                path_dict['accumulated_metric'] = \
                                        int(m.groupdict()['accumulated_metric'])

            m = p11.match(line)
            if m:
                sid_number = int(m.groupdict()['sid_number'])
                sid_dict = path_dict.setdefault('sids', {}).\
                                                    setdefault(sid_number, {})

                sid_dict['sid_number'] = sid_number
                sid_dict['sid_label'] = int(m.groupdict()['sid_label'])
                sid_dict['sid_local_address']=m.groupdict()['sid_local_address']
                sid_dict['sid_remote_address'] = \
                                            m.groupdict()['sid_remote_address']

            m = p11_1.match(line)
            if m:
                path_dict['none'] = 'none'

            m = p12.match(line)
            if m:
                event_time = m.groupdict()['event_time'].lower()
                event_type = m.groupdict()['event_type'].lower()

                time_dict = lsps_dict.setdefault('event_history', {}).\
                                                    setdefault(event_time, {})
                time_dict['time'] = event_time

                event_dict = time_dict.setdefault(event_type, {})
                event_dict['event'] = event_type
            
            m = p13.match(line)
            if m:
                id_name = m.groupdict()['id_name'].lower()
                event_dict['symbolic_name'] = m.groupdict()['symbolic_name']
                event_dict[id_name] = int(m.groupdict()['symbolic_id'])

            m = p14.match(line)
            if m:
                event_dict['source'] = m.groupdict()['event_source']
                event_dict['destination'] = m.groupdict()['dest_source']

            m = p15.match(line)
            if m:
                flag_dict = event_dict.setdefault('flags', {})
                flag_dict['d'] = int(m.groupdict()['d_event'])
                flag_dict['r'] = int(m.groupdict()['r_event'])
                flag_dict['a'] = int(m.groupdict()['a_event'])
                flag_dict['o'] = int(m.groupdict()['o_event'])
                flag_dict['sig_bw'] = int(m.groupdict()['event_sig'])
                flag_dict['act_bw'] = int(m.groupdict()['event_act'])

            m = p16.match(line)
            if m:
                if 'peer' in line.lower():
                    event_dict['peer'] = m.groupdict()['event_peer']

        return ret_dict

    
class ShowSegment_RoutingLocal_BlockInconsistenciesSchema(MetaParser):
    ''' Schema for:
        * show segment-routing local-block inconsistencies
    '''

    schema = {
        'dates' : {
            Any() : {
                'date' : str,
                'inconsistencies' : {
                    Any() : {
                        'inconsistency' : str,
                        'range' : {
                            'start': int,
                            'end' : int,
                        },
                    },
                }
            },
        }
    }

class ShowSegment_RoutingLocal_BlockInconsistencies(ShowSegment_RoutingLocal_BlockInconsistenciesSchema):
    ''' Parser for: 
        * show segment-routing local-block inconsistencies
    '''

    cli_command = 'show segment-routing local-block inconsistencies'

    def cli(self, output = None):
        if output is None:
            out = self.device.execute(self.cli_command)
        else:
            out = output
        # Tue Aug 15 13:53:30.555 EDT
        p1 = re.compile(r'^(?P<inconsistency_date>[\w\s]+[\d\:\.]+\s\w+)$')
        
        # SRLB inconsistencies range: Start/End: 30000/30009
        p2 = re.compile(r'(?P<inconsistency_type>\w+) inconsistencies range: '
                                    'Start\/End: (?P<start>\d+)\/(?P<end>\d+)')
        
        ret_dict = {}

        for line in out.splitlines():
            line = line.strip()

            m = p1.match(line)
            if m:
                date = m.groupdict()['inconsistency_date'].lower()

                dates_dict = ret_dict.setdefault('dates', {})
                date_dict = dates_dict.setdefault(date, {})

                date_dict['date'] = date
            
            m = p2.match(line)
            if m:
                inconsistency = m.groupdict()['inconsistency_type'].lower()

                inconsistency_dict=date_dict.setdefault('inconsistencies', {}).\
                                    setdefault(inconsistency, {})

                inconsistency_dict['inconsistency'] = inconsistency
                range_dict = inconsistency_dict.setdefault('range', {})

                range_dict['start'] = int(m.groupdict()['start'])
                range_dict['end'] = int(m.groupdict()['end'])
        
        return ret_dict


