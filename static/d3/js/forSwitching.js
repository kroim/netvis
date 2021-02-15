let intStatusData = {};

function initIntStatusData() {
    $('#tree-container').html('');
    d3.select("svg").remove();
    intStatusData = {};
    intStatusData.name = "AACDC1-STG-ASW1";
    intStatusData.children = [];
}

function searchKey(key, parentData) {
    if (key && key.length) {
        for (let i = 0; i < parentData.children.length; i++) {
            if (parentData.children[i] && parentData.children[i].length) {
                if (parentData.children[i].name.toLowerCase().indexOf(key.toString().toLowerCase()) > -1) {
                    break;
                }
                searchKey(key, parentData.children[i]);
            } else {
                if (parentData.children[i].name.toLowerCase().indexOf(key.toString().toLowerCase()) < 0)
                    parentData.children.splice(i, 1);
            }
        }
    }
}

function renderIntStatus() {
    initIntStatusData();

    $.ajax({
        url: "static/d3/data/" + hostname + "/json/switching/show interface status.json",
        dataType: 'json',
        async: false,
        success: function (data) {
            let rows = data.TABLE_interface.ROW_interface;
            //console.log(rows.length);

            for (let i = 0; i < rows.length; i++) {
                let keyElement = $('#inputKey');
                let key = keyElement && keyElement.val() ? keyElement.val().toString() : '';


                let path = rows[i].interface + "#" + rows[i].state + "#" + rows[i].vlan + "#Speed:" + rows[i].speed + '#SPF:10Gbase-SR-S' + rows[i].name;
                if (key && key.length) {
                    if (path.toLowerCase().indexOf(key.toLowerCase()) < 0)
                        continue;
                }
                if (rows[i].name) {
                    intStatusData.children.push({
                        'name': rows[i].interface,
                        'children': [{
                            'name': rows[i].state,
                            'children': [{
                                'name': rows[i].vlan,
                                'children': [{
                                    'name': "Speed:" + rows[i].speed,
                                    'children': [{'name': 'SPF:10Gbase-SR-S', 'children': [{'name': rows[i].name}]}]
                                }]
                            }]
                        }]
                    });
                } else {
                    intStatusData.children.push({
                        'name': rows[i].interface,
                        'children': [{
                            'name': rows[i].state,
                            'children': [{
                                'name': rows[i].vlan,
                                'children': [{
                                    'name': "Speed:" + rows[i].speed,
                                    'children': [{'name': 'SPF:10Gbase-SR-S'}]
                                }]
                            }]
                        }]
                    });

                }
            }
            // console.log(intStatusData);
            renderBGPTree(intStatusData);
        }
    });
}

function renderPortChannel() {
    initIntStatusData();

    let multiPairs = [];
    $.ajax({
        url: "static/d3/data/" + hostname + "/json/switching/show port-channel summary.json",
        dataType: 'json',
        async: false,
        success: function (data) {
            // let key = $('#inputKey').val().toString(), path;
            let keyElement = $('#inputKey');
            let key = keyElement && keyElement.val() ? keyElement.val().toString() : '';
            let rows = data.TABLE_channel.ROW_channel;
            //console.log(rows.length);
            for (let i = 0; i < rows.length; i++) {
                let tableRowMembers = rows[i].TABLE_member.ROW_member;
                let color = (rows[i].status === "D") ? "red" : "green";


                if (tableRowMembers.length >= 1) {
                    for (let j = 0; j < tableRowMembers.length; j++) {
                        let multiChild = rows[i]['port-channel'] + ' (' + rows[i].layer + rows[i].status + ') ' + rows[i].prtcl;
                        let multiParent = tableRowMembers[j].port;
                        path = tableRowMembers[0].port + "#" + tableRowMembers[1].port + "#" + multiChild;
                        if (key && key.length) {
                            if (path.toLowerCase().indexOf(key.toLowerCase()) < 0) {
                                break;
                            }
                        }
                        if (j === 0) {
                            intStatusData.children.push({
                                'name': tableRowMembers[j].port,
                                'children': [{
                                    'name': multiChild,
                                    'color': color
                                }]
                            });

                        } else {
                            intStatusData.children.push({
                                'name': multiParent,
                                'color': color,
                                'shareChild': true
                            });

                            multiPairs.push({multiParent, multiChild});
                        }
                    }
                } else {
                    path = tableRowMembers.port + "#" + rows[i]['port-channel'] + ' (' + rows[i].layer + rows[i].status + ') ' + rows[i].prtcl;
                    if (key && key.length) {
                        if (path.toLowerCase().indexOf(key.toLowerCase()) < 0) {
                            continue;
                        }
                    }

                    intStatusData.children.push({
                        'name': tableRowMembers.port,
                        'children': [{
                            'name': rows[i]['port-channel'] + ' (' + rows[i].layer + rows[i].status + ') ' + rows[i].prtcl,
                            'color': color
                        }]
                    });

                }
                //console.log(intStatusData);
            }
            renderMultiParentTree(intStatusData, multiPairs);
            //renderColorTree(intStatusData);
            //console.log(multiPairs);
        }
    });
}

function renderVlan() {
    initIntStatusData();

    $.ajax({
        url: "static/d3/data/" + hostname + "/json/switching/show vlan brief.json",
        dataType: 'json',
        async: false,
        success: function (data) {
            let rows = data.TABLE_vlanbriefxbrief.ROW_vlanbriefxbrief;
            //console.log(rows.length);
            for (let i = 0; i < rows.length; i++) {
                let keyElement = $('#inputKey');
                let key = keyElement && keyElement.val() ? keyElement.val().toString() : '';
                let path = 'Vlan: ' + rows[i]['vlanshowbr-vlanid'] + "#" + 'Name: ' + rows[i]['vlanshowbr-vlanname'] + "#" + rows[i]['vlanshowplist-ifidx'];
                if (key && key.length) {
                    if (path.toLowerCase().indexOf(key.toLowerCase()) < 0)
                        continue;
                }

                intStatusData.children.push({
                    'name': 'Vlan: ' + rows[i]['vlanshowbr-vlanid'],
                    'children': [{
                        'name': 'Name: ' + rows[i]['vlanshowbr-vlanname'],
                        'children': [{
                            'name': rows[i]['vlanshowplist-ifidx']
                        }]
                    }]
                });
                //console.log(intStatusData);
            }
            renderBGPTree(intStatusData);
        }
    });
}

function renderVpc() {
    initIntStatusData();

    let multiPairs = [];
    $.ajax({
        url: "static/d3/data/" + hostname + "/json/switching/show vpc brief.json",
        dataType: 'json',
        async: false,
        success: function (data) {
            let rows = data.TABLE_vpc.ROW_vpc;
            let keyElement = $('#inputKey');
            let key = keyElement && keyElement.val() ? keyElement.val().toString() : '';
            for (let i = 0; i < rows.length; i++) {
                let color = "red";
                let path = "VPC: " + rows[i]['vpc-id'] + "(" + rows[i]['vpc-consistency'] + ")" + "#" + rows[i]['vpc-ifindex'] + "#" + rows[i]['up-vlan-bitset'];
                if (key && key.length && path.toLowerCase().indexOf(key.toLowerCase()) < 0)
                    continue;
                if (rows[i]['vpc-consistency'] === "consistent") color = "green";
                intStatusData.children.push({
                    'name': "VPC: " + rows[i]['vpc-id'] + "(" + rows[i]['vpc-consistency'] + ")",
                    'color': color,
                    'children': [{
                        'name': rows[i]['vpc-ifindex'],
                        'color': color,
                        'children': [{
                            'name': rows[i]['up-vlan-bitset'],
                            'color': color
                        }]
                    }]
                });
            }

            let preData = {
                name: "PEER",
                children: []
            };
            let multiChild = "AACDC1-STG-ASW1";

            preData.children.push({
                'name': "VPC ID: " + data['vpc-domain-id'],
                'children': [
                    intStatusData
                ]
            });

            let multiParent = "Pearlink: " + data.TABLE_peerlink.ROW_peerlink['peerlink-ifindex'];

            preData.children.push({
                'name': multiParent,
                'shareChild': true
            });
            multiPairs.push({multiParent, multiChild});

            // multiParent = "VPC Vlans: " + data.TABLE_peerlink.ROW_peerlink['peer-up-vlan-bitset'];
            // preData.children.push({
            //     'name': multiParent,
            //     'shareChild': true
            // });
            // multiPairs.push({multiParent, multiChild});

            multiParent = data['vpc-peer-status'];
            preData.children.push({
                'name': multiParent,
                'shareChild': true
            });
            multiPairs.push({multiParent, multiChild});

            multiParent = data['vpc-peer-keepalive-status'];
            preData.children.push({
                'name': multiParent,
                'shareChild': true
            });
            multiPairs.push({multiParent, multiChild});

            renderMultiParentTree(preData, multiPairs, false);
        }
    });
}

function renderFex() {
    initIntStatusData();

    let multiPairs = [];
    $.ajax({
        url: "static/d3/data/" + hostname + "/json/switching/show fex detail.json",
        dataType: 'json',
        async: false,
        success: function (data) {
            let rows = data.TABLE_fex_info.ROW_fex_info;
            for (let i = 0; i < rows.length; i++) {
                let color = "green";
                let keyElement = $('#inputKey');
                let key = keyElement && keyElement.val() ? keyElement.val().toString() : '';
                let childNode = {
                    name: rows[i].fex_state + "/" + rows[i].model + "/" + rows[i].serial,
                    children: []
                };

                let fexPorts = rows[i].TABLE_fex_port.ROW_fex_port;
                let filteredChild = {
                    name: rows[i].fex_state + "/" + rows[i].model + "/" + rows[i].serial,
                    children: []
                };
                for (let k = 0; k < fexPorts.length; k++) {
                    if (fexPorts[k].fex_port_oper_state === "Down") color = "red";
                    else color = "green";
                    let name = fexPorts[k].fex_port + " " + fexPorts[k].fex_port_oper_state;
                    if (key && key.length && name.toLowerCase().indexOf(key.toLowerCase()) > -1) {
                        filteredChild.children.push({
                            name: fexPorts[k].fex_port + " " + fexPorts[k].fex_port_oper_state,
                            color: color
                        });
                        // console.log(name);
                    }
                    childNode.children.push({
                        name: fexPorts[k].fex_port + " " + fexPorts[k].fex_port_oper_state,
                        color: color
                    });

                }

                let fbrStates = rows[i].TABLE_fbr_state.ROW_fbr_state;
                let multiChild = fbrStates[0].fbr_index;
                let path = fbrStates[0].fbr_index + "#" + fbrStates[1].fbr_index + "#" + fbrStates[2].fbr_index + "#" + childNode.name;
                if (key && key.length) {
                    if (path.toLowerCase().indexOf(key.toLowerCase()) < 0) {
                        childNode = filteredChild;
                        if (childNode.children.length === 0)
                            continue;
                    } else {
                        // console.log(path);
                    }
                }

                for (let j = 1; j < fbrStates.length; j++) {
                    let multiParent = fbrStates[j].fbr_index;

                    if (j === 1) {
                        intStatusData.children.push({
                            'name': multiParent,
                            'children': [{
                                'name': multiChild,
                                'children': [
                                    childNode
                                ]
                            }]
                        });

                    } else {
                        intStatusData.children.push({
                            'name': multiParent,
                            'shareChild': true
                        });

                        multiPairs.push({multiParent, multiChild});
                    }
                }
            }
            // console.log(intStatusData);
            renderMultiParentTree(intStatusData, multiPairs, false);
        }
    });
}

function renderCdp() {
    initIntStatusData();
    $.ajax({
        url: "static/d3/data/" + hostname + "/json/switching/show cdp neighbors detail.json",
        dataType: 'json',
        async: false,
        success: function (data) {
            let rows = data.TABLE_cdp_neighbor_detail_info.ROW_cdp_neighbor_detail_info;
            for (let i = 0; i < rows.length; i++) {
                let childNode = {
                    name: rows[i].port_id,
                    children: []
                };
                childNode.children.push({
                    name: rows[i].sysname
                });
                childNode.children.push({
                    name: rows[i].platform_id
                });
                childNode.children.push({
                    name: rows[i].v4addr
                });
                if (rows[i].v4mgmtaddr) {
                    childNode.children.push({
                        name: rows[i].v4mgmtaddr
                    });
                }

                intStatusData.children.push({
                    name: rows[i].intf_id,
                    children: [
                        childNode
                    ]
                });
            }
            // console.log(intStatusData);
            renderBGPTree(intStatusData);
        }
    });

    ajaxindicatorstop();
}

function renderArp() {
    initIntStatusData();
    $.ajax({
        url: "static/d3/data/" + hostname + "/json/switching/show ip arp vrf all.json",
        dataType: 'json',
        async: false,
        success: function (data) {
            let rows = data.TABLE_vrf.ROW_vrf.TABLE_adj.ROW_adj;
            for (let i = 0; i < rows.length; i++) {
                let keyElement = $('#inputKey');
                let key = keyElement && keyElement.val() ? keyElement.val().toString() : '';
                let path = rows[i].mac + "#" + rows[i]['ip-addr-out'] + "#" + rows[i]['intf-out'];

                let childNode = {
                    name: rows[i].mac,
                    children: [{
                        name: rows[i]['ip-addr-out'],
                        children: [{
                            name: rows[i]['intf-out']
                        }]
                    }]
                };
                if (key && key.length) {
                    if (path.toLowerCase().indexOf(key.toLowerCase()) > -1) {
                        addChildNode(intStatusData, childNode);
                    }
                } else {
                    addChildNode(intStatusData, childNode);
                }
            }

            // console.log(intStatusData);
            renderBGPTree(intStatusData);
        }
    });
}

function renderMac() {
    initIntStatusData();
    $.ajax({
        url: "static/d3/data/" + hostname + "/json/switching/show mac address-table.json",
        dataType: 'json',
        async: false,
        success: function (data) {
            let rows = data.TABLE_mac_address.ROW_mac_address;
            for (let i = 0; i < rows.length; i++) {
                let keyElement = $('#inputKey');
                let key = keyElement && keyElement.val() ? keyElement.val().toString() : '';
                let path = "Vlan: " + rows[i].disp_vlan + "#" + rows[i].disp_mac_addr + "#" + rows[i].disp_port;
                let childNode = {
                    name: "Vlan: " + rows[i].disp_vlan,
                    children: [{
                        name: rows[i].disp_mac_addr,
                        children: [{
                            name: rows[i].disp_port
                        }]
                    }]
                };
                if (key && key.length) {
                    if (path.toLowerCase().indexOf(key.toLowerCase()) > -1) {
                        addChildNode(intStatusData, childNode);
                    }
                } else {
                    addChildNode(intStatusData, childNode);
                }
            }

            // console.log(intStatusData);
            renderBGPTree(intStatusData);
        }
    });
}

function renderStp() {
    initIntStatusData();
}
