renderInitialTable = function (clock1, clock2) {
    d3.select("svg").remove();
    $('#tree-container').html('');
    var html = "<div class='container text-center' style='margin-top: 5vw;' id='table'><table class='table table-striped table-bordered'>";
    html += "<thead><tr style='background-color: yellow;'><th style='text-align: center !important;'>updated on: " + clock1 + "</th><th style='text-align: center !important;'>updated on: " + clock2 + "</th></tr></thead>";
    html += "<tbody>";
    html += "<tr><td>show system resources</td><td>show ip route vrf all</td></tr>";
    html += "<tr><td>show hardware</td><td>show ip int vrf all</td></tr>";
    html += "<tr><td>show feature</td><td>show bgp all vrf all</td></tr>";
    html += "<tr><td></td><td>show bgp l2vpn evpn vrf all</td></tr>";
    html += "<tr><td>show interface status</td><td>show ip ospf database detail vrf all</td></tr>";
    html += "<tr><td>show port-channel summary</td><td></td></tr>";
    html += "<tr><td>show vlan brief</td><td></td></tr>";
    html += "<tr><td>show vpc brief</td><td></td></tr>";
    html += "<tr><td>show fex detail</td><td></td></tr>";
    html += "<tr><td>show cdp neighbors detail</td><td></td></tr>";
    html += "<tr><td>show ip arp vrf all</td><td></td></tr>";
    html += "<tr><td>show mac address-table</td><td></td></tr>";
    html += "<tr><td>show spanning-tree detail</td><td></td></tr>";
    html += "</tbody>";
    html += "</table></div>";
    let oldTable = document.getElementById('table');
    if (oldTable != undefined && oldTable.parentNode != undefined)
        oldTable.parentNode.removeChild(oldTable);
    $('#tree-container').append(html);
    document.querySelector("#full-screen-area").requestFullscreen();

};