/**
 * Variables for storing BGP/COLOR json data
 */
ajaxindicatorstart("Loading...   Please Wait...");

let bgpData = {}, bgpDataOriginal = {}, bgpDataLoaded = false;
let colorData = {}, colorDataOriginal = {}, colorDataLoaded = false;
let hostname = "AACDC1-STG-ASW1";
let clock1, clock2;
let mappingData = [];
const MODE_NONE = 0, MODE_BGP = 1, MODE_ROUTING_INTBRIEF = 2, MODE_ROUTING_ROUTETABLE = 22;
const MODE_SWITCH_INTSTATUS = 30, MODE_SWITCH_PORTCHANNEL = 31, MODE_SWITCH_VLAN = 32, MODE_SWITCH_VPC = 33,
    MODE_SWITCH_FEX = 34, MODE_SWITCH_CDP = 35, MODE_SWITCH_ARP = 36, MODE_SWITCH_MAC = 37, MODE_SWITCH_STP = 38;
let modeSetting = MODE_NONE;

/**
 * init generated data value
 */
function initBgpData() {
    bgpData.name = hostname;
    bgpData.children = [];

}

function initColor() {
    colorData.name = hostname;
    colorData.children = [];
}

/**
 * generate new json data to display from existing json file
 * and save the data in an object variable, bgpData
 * @param data
 */
let host = [];

function generateNewData(data, key) {
    initBgpData();
    host = data.TABLE_vrf.ROW_vrf.TABLE_afi.ROW_afi[0].TABLE_safi.ROW_safi.TABLE_rd.ROW_rd.TABLE_prefix.ROW_prefix;
    //console.log("host="+host);

    for (let i = 0; i < host.length; i++) {
        let ipprefix = host[i].ipprefix;
        let paths = host[i].TABLE_path.ROW_path;

        for (let j = 0; j < paths.length; j++) {
            let isNone = false;
            if (paths[j].best === "none") {
                isNone = true;
            } else {
                isNone = false;
            }
            if (!isNone) {
                if (paths[j] && paths[j].aspath) {
                    let asPaths = paths[j].aspath.split(" ");

                    let childNode = {}, curNode = childNode;
                    //console.log('curNode='+curNode);
                    for (let k = 0; k < asPaths.length; k++) {

                        curNode.name = asPaths[k];
                        curNode.children = [];
                        curNode.children.push({});
                        curNode = curNode.children[0];
                    }
                    // for the last child , ipprefix
                    curNode.name = ipprefix;

                    // if searchmode: check if it matches

                    if (key && key.length > 0) {
                        if (ipprefix.toLowerCase().indexOf(key, 0) >= 0 || paths[j].aspath.toLowerCase().indexOf(key, 0) >= 0) {
                            //console.log("key="+key+"-"+ipprefix);
                            addChildNode(bgpData, childNode);
                        } else {
                        }
                    } else {
                        addChildNode(bgpData, childNode);
                    }
                    break;
                }

            }


        }

    }
    return bgpData;

}


/**
 * generate new json data to display color existing json file
 * @param data
 * @param key
 */
let vrf = [];
let intf = [];

function generateIntBriefData(data, key) {
    $('#tree-container').html('');
    d3.select("svg").remove();

    initColor();
    vrf = data.TABLE_vrf;
    intf = data.TABLE_intf;
    let count = vrf.length > intf.length ? vrf.length : intf.length;
    for (let i = 0; i < count; i++) {
        let child = {};
        child.children = [];
        let temp0 = vrf[i].ROW_vrf['vrf-name-out'];
        let temp1 = intf[i].ROW_intf['prefix'] + "/" + intf[i].ROW_intf['masklen'];
        let temp2 = intf[i].ROW_intf['intf-name'];
        let temp3 = intf[i].ROW_intf['proto-state'];
        let temp4 = intf[i].ROW_intf['link-state'];
        let temp5 = intf[i].ROW_intf['admin-state'];

        if (key && key.length) {
            if (
                (temp0.toLowerCase().indexOf(key) < 0) &&
                (temp1.toLowerCase().indexOf(key) < 0) &&
                (temp2.toLowerCase().indexOf(key) < 0) &&
                (temp3.toLowerCase().indexOf(key) < 0) &&
                (temp4.toLowerCase().indexOf(key) < 0) &&
                (temp5.toLowerCase().indexOf(key) < 0)) {
                continue;
            }
        }

        child.name = temp0;
        child.color = temp0;
        child.children.push({
            name: temp1,
            color: temp0,
            children: [{
                name: temp2,
                color: temp0,
                children: [{name: temp3, children: [{name: temp4, children: [{name: temp5}]}]}]
            }]
        });
        addChildNode(colorData, child);
    }
    //console.log(colorData);
    return colorData;

}

//console.log(colorData);
/**
 * render Tree of Dendrogram
 * @param data
 */
function renderTree(data) {
    switch (modeSetting) {
        case MODE_BGP:
            renderBGPTree(data);
            break;
        case MODE_ROUTING_INTBRIEF:
            renderColorTree(data);
            break;
        case MODE_NONE:
            renderInitialTable(clock1, clock2);
        default:
            break;
    }
}

function keyDown(event) {
    if (event.key == 'Enter')
        update();
}


function onHome(_hostname = '') {
    hostname = _hostname;
    renderInitialTable(clock1, clock2);
}


function onInfo(_hostname = '') {
    hostname = _hostname;
    renderInfoTable(clock1, hostname);
}

function onConfig(_hostname = '') {
    hostname = _hostname;
    renderTextFile('static/d3/data/' + _hostname + '/json/system/config.txt');
}

function onLog(_hostname = '') {
    hostname = _hostname;
    renderTextFile('static/d3/data/' + _hostname + '/json/system/log.txt');
}


// search & remove other items
function update() {
    let keyElement = document.getElementById('inputKey')
    let key = keyElement ? keyElement.value.toLowerCase() : '';
    //alert('key = ' + key);
    ajaxindicatorstart("Loading...   Please Wait...");
    d3.select("svg").remove();
    setTimeout(function () {
        let extractData;
        switch (modeSetting) {
            case MODE_BGP:
                extractData = generateNewData(bgpDataOriginal, key);
                break;
            case MODE_ROUTING_INTBRIEF:
                extractData = generateIntBriefData(colorDataOriginal, key);
                break;
            case MODE_ROUTING_ROUTETABLE:
                renderRouteTable();
                break;
            case MODE_SWITCH_INTSTATUS:
                renderIntStatus();
                break;
            case MODE_SWITCH_PORTCHANNEL:
                renderPortChannel();
                break;
            case MODE_SWITCH_VLAN:
                renderVlan();
                break;
            case MODE_SWITCH_VPC:
                renderVpc();
                break;
            case MODE_SWITCH_FEX:
                renderFex();
                break;
            case MODE_SWITCH_CDP:
                renderCdp();
                break;
            case MODE_SWITCH_ARP:
                renderArp();
                break;
            case MODE_SWITCH_MAC:
                renderMac();
                break;
            case MODE_SWITCH_STP:
                renderStp();
                break;
            default:
                break;
        }
        if (extractData) {
            renderTree(extractData);
        }
        ajaxindicatorstop();
    }, 500);
    document.querySelector("#full-screen-area").requestFullscreen();
}

function onIntBrief(_hostname = '') {
    hostname = _hostname;
    modeSetting = MODE_ROUTING_INTBRIEF;
    update();
}


function onRouteTable(_hostname = '') {
    hostname = _hostname;
    modeSetting = MODE_ROUTING_ROUTETABLE;
    update();
}

function onIntStatus(_hostname = '') {
    hostname = _hostname;
    modeSetting = MODE_SWITCH_INTSTATUS;
    update();
}

function onPortChannel(_hostname = '') {
    hostname = _hostname;
    modeSetting = MODE_SWITCH_PORTCHANNEL;
    update();
}

function onVlan(_hostname = '') {
    hostname = _hostname;
    modeSetting = MODE_SWITCH_VLAN;
    update();
}

function onVpc(_hostname = '') {
    hostname = _hostname;
    modeSetting = MODE_SWITCH_VPC;
    update();
}

function onFex(_hostname = '') {
    hostname = _hostname;
    modeSetting = MODE_SWITCH_FEX;
    update();
}

function onCdp(_hostname = '') {
    hostname = _hostname;
    modeSetting = MODE_SWITCH_CDP;
    update();
}

function onArp(_hostname = '') {
    hostname = _hostname;
    modeSetting = MODE_SWITCH_ARP;
    update();
}

function onMac(_hostname = '') {
    hostname = _hostname;
    modeSetting = MODE_SWITCH_MAC;
    update();
}

function onStp(_hostname = '') {
    hostname = _hostname;
    modeSetting = MODE_SWITCH_STP;
    update();
}

function keyDown(event) {
    if (event.key == 'Enter')
        update();
}


$(document).ready(function () {
    // set SSH button setting
    for (let mapping of mapping_ssh) {
        let ssh_selector = `tr#${mapping.text} td.row-ssh>a`;
        $(ssh_selector).attr('title', mapping.text);
        $(ssh_selector).attr('href', mapping.url);
    }
    /*

    // show dendrogram for Bgp
        $('#btnBgp').click(function () {
            document.getElementById('inputKey').value = "";
            modeSetting = MODE_BGP;
            update();
        });

    // show dendrogram for Color
        $('#btnIntBrief').click(function () {
            document.getElementById('inputKey').value = "";
            modeSetting = MODE_ROUTING_INTBRIEF;
            update();
        });


        $('#btnSave').click(function () {
            //saveImage();
        });
    */

//Loading Colors
    $.ajax({
        url: 'static/d3/data/' + hostname + '/json/routing/show ip int vrf all.json',
        dataType: 'json',
        async: false,
        success: function (data) {
            //console.log(data);
            if (!colorDataLoaded) {
                colorDataOriginal = data;
                colorDataLoaded = true;
            }

            //generateColorData to display
            generateIntBriefData(data);
        }
    });

    $.ajax({
        url: 'static/d3/data/' + hostname + '/json/system/clock1.json',
        dataType: 'json',
        async: false,
        success: function (data) {
            clock1 = data.simple_time;
        }
    });

    $.ajax({
        url: 'static/d3/data/' + hostname + '/json/system/clock2.json',
        dataType: 'json',
        async: false,
        success: function (data) {
            clock2 = data.simple_time;
        }
    });

    // renderTree(bgpData);

    $('[data-toggle="tooltip"]').tooltip();


    $('#btnSearch').click(function () {
        update();
    })
});
ajaxindicatorstop();

