let routingData = {};

function initRoutingData() {
    $('#tree-container').html('');
    d3.select("svg").remove();
    routingData = {};
    routingData.name = "AACDC1-STG-ASW1";
    routingData.children = [];
}


function renderRouteTable() {
    initRoutingData();

    $.ajax({
        url: "static/d3/data/" + hostname + "/json/routing/show ip route vrf all.json",
        dataType: 'json',
        async: false,
        success: function (data) {
            let rows = data.TABLE_vrf.ROW_vrf;

            for (let i = 0; i < rows.length; i++) {
                if (!rows[i].TABLE_addrf || !rows[i].TABLE_addrf.ROW_addrf || !rows[i].TABLE_addrf.ROW_addrf.TABLE_prefix || !rows[i].TABLE_addrf.ROW_addrf.TABLE_prefix.ROW_prefix)
                    continue;
                let keyElement = $('#inputKey');
                let key = keyElement && keyElement.val() ? keyElement.val().toString() : '';

                let vrf_name = rows[i]['vrf-name-out'];
                let color = '#333';
                switch (vrf_name) {
                    case 'STAGE-BLUE':
                        color = 'blue';
                        break;
                    case 'STAGE-BLUE-GREY':
                        color = '#8888ff';
                        break;
                    case 'STAGE-GREEN':
                        color = '#00aa00';
                        break;
                    case 'STAGE-GREEN-GREY':
                        color = '#66aa66';
                        break;
                    case 'STAGE-GREY':
                        color = 'GREY';
                        break;
                    case 'STAGE-RED':
                        color = '#ff0000';
                        break;
                    default:
                        break;
                }

                let prefixes = rows[i].TABLE_addrf.ROW_addrf.TABLE_prefix.ROW_prefix;
                let children1 = [];
                for (let prefix of prefixes) {
                    if (!prefix.TABLE_path.ROW_path)
                        continue;

                    let children2 = [];

                    let ip_prefix = prefix.ipprefix;
                    let paths = prefix.TABLE_path.ROW_path;
                    if (Array.isArray(paths)) {
                        for (let j = 0; j < paths.length - 1; j = j + 2) {
                            let ipnexthop = paths[j].ipnexthop;
                            let clientname = paths[j + 1].clientname;
                            let ifname = paths[j].ifname ? paths[j].ifname : '';
                            let tag = paths[j + 1].tag;
                            let children2_name = ipnexthop + ' ' + clientname + ' ' + ifname;
                            if (clientname.startsWith("bgp")) {
                                children2_name = ipnexthop + '  BGP-' + tag;
                            }

                            let path = vrf_name + "#" + ip_prefix + "#" + children2_name;

                            if (key && key.length && path.toLowerCase().indexOf(key.toLowerCase()) < 0)
                                continue;

                            children2.push({name: children2_name, color: color});
                        }
                    } else {
                        let ipnexthop = paths.ipnexthop;
                        let clientname = paths.clientname;
                        let ifname = paths.ifname ? paths.ifname : '';
                        let tag = paths.tag;
                        let children2_name = ipnexthop + ' ' + clientname + ' ' + ifname;
                        if (clientname.startsWith("bgp")) {
                            children2_name = ipnexthop + '  BGP-' + tag;
                        }

                        let path = vrf_name + "#" + ip_prefix + "#" + children2_name;

                        if (key && key.length && path.toLowerCase().indexOf(key.toLowerCase()) < 0)
                            continue;

                        children2.push({name: children2_name, color: color});
                    }

                    if (children2.length > 0)
                        children1.push({name: ip_prefix, color: color, children: children2});
                }

                routingData.children.push({name: vrf_name, color: color, children: children1});
            }
            // console.log(routingData);
            renderColorTree(routingData);
        }
    });
}

function renderBgpPeers() {
    initRoutingData();

    $.ajax({
        url: "static/d3/data/" + hostname + "/json/routing/show bgp all neighbors vrf all.json",
        dataType: 'json',
        async: false,
        success: function (data) {
            let rows = data.TABLE_neighbor.ROW_neighbor;
            //console.log(rows.length);

            let trees = [];

            for (let i = 0; i < rows.length; i++) {
                let keyElement = $('#inputKey');
                let key = keyElement && keyElement.val() ? keyElement.val().toString() : '';

                let children1_name = '64823';
                let children2_name = rows[i]['description'].split('|')[1];
                children2_name = children2_name.split('-')[1] + '-' + children2_name.split('-')[2];
                while (children2_name.indexOf(' ') > -1) {
                    children2_name = children2_name.replace(' ', '');
                }
                let children3_name = rows[i]['neighbor'];
                let children4_name = rows[i]['remoteas'];
                let children5_name = rows[i]['state'];
                let children6_name = rows[i]['elapsedtime'];
                let children7_name = rows[i]['fd'];

                let path = children1_name + '#' + children2_name + '#' + children3_name + '#' + children4_name + '#' + children5_name + '#' + children6_name;
                if (key && key.length && path.toLowerCase().indexOf(key.toLowerCase()) < 0)
                    continue;

                trees.push({
                    c1: children1_name,
                    c2: children2_name,
                    c3: children3_name,
                    c4: children4_name,
                    c5: children5_name,
                    c6: children6_name,
                    c7: children7_name
                });
            }
            // console.log(trees);

            for (let tree of trees) {
                let color = '#333';
                switch (tree.c2) {
                    case 'STAGE-BLUE':
                        color = 'blue';
                        break;
                    case 'STAGE-BLUE-GREY':
                        color = '#8888ff';
                        break;
                    case 'STAGE-GREEN':
                        color = '#00aa00';
                        break;
                    case 'STAGE-GREEN-GREY':
                        color = '#66aa66';
                        break;
                    case 'STAGE-GREY':
                        color = 'GREY';
                        break;
                    case 'STAGE-RED':
                        color = '#ff0000';
                        break;
                    default:
                        break;
                }
                // console.log(color);

                if (routingData.children.length) {
                    let repeat_c1_index = -1;
                    for (let i = 0; i < routingData.children.length; i++) {
                        if (routingData.children[i].name === tree.c1) {
                            repeat_c1_index = i;
                            break;
                        }
                    }
                    if (repeat_c1_index > -1) {
                        let repeat_c2_index = -1;
                        for (let j = 0; j < routingData.children[repeat_c1_index].children.length; j++) {
                            if (routingData.children[repeat_c1_index].children[j].name === tree.c2) {
                                repeat_c2_index = j;
                                break;
                            }
                        }
                        // console.log(tree.c2);
                        // console.log(repeat_c2_index);

                        if (repeat_c2_index > -1) {
                            routingData.children[repeat_c1_index].children[repeat_c2_index].children.push({
                                name: tree.c3,
                                color: color,
                                popup: true,
                                children: [{
                                    name: tree.c4,
                                    color: color,
                                    children: [{
                                        name: tree.c5,
                                        color: color,
                                        children: [{
                                            name: tree.c6,
                                            color: color,
                                            children: [{
                                                name: tree.c7,
                                                color: color
                                            }]
                                        }]
                                    }]
                                }]
                            })
                        } else {
                            routingData.children[repeat_c1_index].children.push({
                                name: tree.c2,
                                color: color,
                                children: [{
                                    name: tree.c3,
                                    color: color,
                                    popup: true,
                                    children: [{
                                        name: tree.c4,
                                        color: color,
                                        children: [{
                                            name: tree.c5,
                                            color: color,
                                            children: [{
                                                name: tree.c6,
                                                color: color,
                                                children: [{
                                                    name: tree.c7,
                                                    color: color
                                                }]
                                            }]
                                        }]
                                    }]
                                }]
                            })
                        }
                    } else {
                        routingData.children[repeat_c1_index].children.push(
                            {
                                name: tree.c1,
                                children: [{
                                    name: tree.c2,
                                    color: color,
                                    children: [{
                                        name: tree.c3,
                                        color: color,
                                        popup: true,
                                        children: [{
                                            name: tree.c4,
                                            color: color,
                                            children: [{
                                                name: tree.c5,
                                                color: color,
                                                children: [{
                                                    name: tree.c6,
                                                    color: color,
                                                    children: [{
                                                        name: tree.c7,
                                                        color: color
                                                    }]
                                                }]
                                            }]
                                        }]
                                    }]
                                }]
                            }
                        )
                    }
                } else {
                    routingData.children.push(
                        {
                            name: tree.c1,
                            children: [{
                                name: tree.c2,
                                color: color,
                                children: [{
                                    name: tree.c3,
                                    color: color,
                                    popup: true,
                                    children: [{
                                        name: tree.c4,
                                        color: color,
                                        children: [{
                                            name: tree.c5,
                                            color: color,
                                            children: [{
                                                name: tree.c6,
                                                color: color,
                                                children: [{
                                                    name: tree.c7,
                                                    color: color
                                                }]
                                            }]
                                        }]
                                    }]
                                }]
                            }]
                        }
                    )
                }
            }
            // console.log(routingData);
            renderColorTree(routingData);
        }
    });
}
