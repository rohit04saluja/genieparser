expected_output = {
    "nodes": {
        1: {
            "ospf_router_id": "10.19.198.239",
            "area_id": 8,
            "domain_id": 0,
            "asn": 65109,
            "prefix_sid": {
                "prefix": "10.19.198.239",
                "label": 16073,
                "label_type": "regular",
                "domain_id": 0,
                "flags": "N , E",
            },
            "links": {
                0: {
                    "local_address": "10.19.198.26",
                    "remote_address": "10.19.198.25",
                    "local_node": {
                        "ospf_router_id": "10.19.198.239",
                        "area_id": 8,
                        "domain_id": 0,
                        "asn": 65109,
                    },
                    "remote_node": {
                        "ospf_router_id": "10.189.5.252",
                        "area_id": 8,
                        "domain_id": 0,
                        "asn": 65109,
                    },
                    "metric": {"igp": 1000, "te": 1000, "delay": 1000},
                    "bandwidth_total": 125000000,
                    "bandwidth_reservable": 0,
                    "admin_groups": "0x00000000",
                    "adj_sid": {"18": "unprotected", "36": "protected"},
                },
                1: {
                    "local_address": "10.19.198.30",
                    "remote_address": "10.19.198.29",
                    "local_node": {
                        "ospf_router_id": "10.19.198.239",
                        "area_id": 8,
                        "domain_id": 0,
                        "asn": 65109,
                    },
                    "remote_node": {
                        "ospf_router_id": "10.189.5.253",
                        "area_id": 8,
                        "domain_id": 0,
                        "asn": 65109,
                    },
                    "metric": {"igp": 1000, "te": 1000, "delay": 1000},
                    "bandwidth_total": 125000000,
                    "bandwidth_reservable": 0,
                    "admin_groups": "0x00000000",
                    "adj_sid": {"37": "unprotected", "38": "protected"},
                },
            },
        },
        2: {
            "ospf_router_id": "10.189.5.252",
            "area_id": 8,
            "domain_id": 0,
            "asn": 65109,
            "prefix_sid": {
                "prefix": "10.189.5.252",
                "label": 16071,
                "label_type": "regular",
                "domain_id": 0,
                "flags": "N",
            },
            "links": {
                0: {
                    "local_address": "10.19.198.25",
                    "remote_address": "10.19.198.26",
                    "local_node": {
                        "ospf_router_id": "10.189.5.252",
                        "area_id": 8,
                        "domain_id": 0,
                        "asn": 65109,
                    },
                    "remote_node": {
                        "ospf_router_id": "10.19.198.239",
                        "area_id": 8,
                        "domain_id": 0,
                        "asn": 65109,
                    },
                    "metric": {"igp": 1000, "te": 1000, "delay": 1000},
                    "bandwidth_total": 125000000,
                    "bandwidth_reservable": 125000000,
                    "admin_groups": "0x00000000",
                    "adj_sid": {"24": "protected"},
                },
                1: {
                    "local_address": "10.169.14.122",
                    "remote_address": "10.169.14.121",
                    "local_node": {
                        "ospf_router_id": "10.189.5.252",
                        "area_id": 8,
                        "domain_id": 0,
                        "asn": 65109,
                    },
                    "remote_node": {
                        "ospf_router_id": "10.169.14.240",
                        "area_id": 8,
                        "domain_id": 0,
                        "asn": 65109,
                    },
                    "metric": {"igp": 100, "te": 100, "delay": 100},
                    "bandwidth_total": 125000000,
                    "bandwidth_reservable": 125000000,
                    "admin_groups": "0x00000000",
                    "adj_sid": {"16": "protected"},
                },
                2: {
                    "local_address": "10.189.5.93",
                    "remote_address": "10.189.5.94",
                    "local_node": {
                        "ospf_router_id": "10.189.5.252",
                        "area_id": 8,
                        "domain_id": 0,
                        "asn": 65109,
                    },
                    "remote_node": {
                        "ospf_router_id": "10.189.5.253",
                        "area_id": 8,
                        "domain_id": 0,
                        "asn": 65109,
                    },
                    "metric": {"igp": 5, "te": 5, "delay": 5},
                    "bandwidth_total": 125000000,
                    "bandwidth_reservable": 125000000,
                    "admin_groups": "0x00000000",
                    "adj_sid": {"19": "protected"},
                },
            },
        },
    }
}