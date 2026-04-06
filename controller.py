from ryu.app import simple_switch_stp_13
from ryu.lib import stplib
from ryu.lib import dpid as dpid_lib
from ryu.controller.handler import MAIN_DISPATCHER, set_ev_cls


class LinkRecoveryController(simple_switch_stp_13.SimpleSwitch13):
    _CONTEXTS = {'stplib': stplib.Stp}

    def __init__(self, *args, **kwargs):
        super(LinkRecoveryController, self).__init__(*args, **kwargs)
        stp = kwargs['stplib']

        config = {
            dpid_lib.str_to_dpid('0000000000000001'): {'bridge': {'priority': 0x8000}},
            dpid_lib.str_to_dpid('0000000000000002'): {'bridge': {'priority': 0x9000}},
            dpid_lib.str_to_dpid('0000000000000003'): {'bridge': {'priority': 0xa000}},
            dpid_lib.str_to_dpid('0000000000000004'): {'bridge': {'priority': 0xb000}},
        }
        stp.set_config(config)

    @set_ev_cls(stplib.EventTopologyChange, MAIN_DISPATCHER)
    def topology_change_handler(self, ev):
        dp = ev.dp
        dpid_str = "%016x" % dp.id
        self.logger.info("[PROJECT 14] Topology change detected on switch %s", dpid_str)

        if dp.id in self.mac_to_port:
            self.mac_to_port[dp.id].clear()
            self.logger.info("[PROJECT 14] MAC table flushed for switch %s", dpid_str)

    @set_ev_cls(stplib.EventPortStateChange, MAIN_DISPATCHER)
    def port_state_change_handler(self, ev):
        dpid_str = "%016x" % ev.dp.id
        self.logger.info(
            "[PROJECT 14] Switch %s: Port %d state changed to %s",
            dpid_str, ev.port_no, ev.port_state
        )
