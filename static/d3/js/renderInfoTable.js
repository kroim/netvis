renderInfoTable = function (clock1, _hostname = '') {
    d3.select("svg").remove();
    $('#tree-container').html('');
    let feature = loadFeature();
    let hardware = loadHardware();
    let resources = loadResources();

    const chassis_id = hardware.chassis_id ? hardware.chassis_id : '';


    let html = "<div class='container text-center' style='margin-top: 5vw;' id='table'><table class='table table-striped table-bordered'>";
    html += "<thead><tr style='background-color: yellow; font-size: 16px'><th style='text-align: center !important;' colspan='4'>" + hostname + "</th></tr></thead>";
    html += "<tbody>";
    html += "<tr><td>Hardware:</td><td>" + chassis_id + "</td><td>CPU User:</td><td>" + resources.cpu_state_user + "%</td></tr>";
    html += "<tr><td>Version:</td><td>" + hardware.kickstart_ver_str + "</td><td>CPU Kernal:</td><td>" + resources.cpu_state_kernel + "%</td></tr>";
    html += "<tr><td>Manufacturer:</td><td>" + hardware.manufacturer + "</td><td>CPU Idle:</td><td>" + resources.cpu_state_idle + "%</td></tr>";
    html += "<tr><td>Serial:</td><td>" + hardware.proc_board_id + "</td><td></td><td></td></tr>";
    html += "<tr><td>UP Since:</td><td>" + hardware.kern_uptm_days + " day(s), " + hardware.kern_uptm_hrs + " hour(s), " + hardware.kern_uptm_mins + " minute(s), " + hardware.kern_uptm_secs + " second(s)</td><td>Memory Total:</td><td>" + resources.memory_usage_total + "</td></tr>";
    html += "<tr><td>Last Reboot:</td><td>" + hardware.rr_reason + "</td><td>Memory Used:</td><td>" + resources.memory_usage_used + "</td></tr>";
    html += "<tr><td>Clock:</td><td>" + clock1 + "</td><td>Memory Available:</td><td>" + resources.memory_usage_free + "</td></tr>";
    html += "<tr><td>&nbsp;</td><td></td><td></td><td></td></tr>";
    html += "<tr><td>&nbsp;</td><td></td><td></td><td></td></tr>";

    let tempArray1 = [];
    let tempArray3 = [], tempArray4 = [];


    if (hostname === hardware.host_name) {
        for (let i = 0; i < feature.TABLE_cfcFeatureCtrlTable.ROW_cfcFeatureCtrlTable.length; i++) {
            let temp1 = feature.TABLE_cfcFeatureCtrlTable.ROW_cfcFeatureCtrlTable[i];
            if (temp1.cfcFeatureCtrlOpStatus2 === "enabled") {
                tempArray1.push(temp1.cfcFeatureCtrlName2);
            }

        }

        for (let j = 0; j < hardware.TABLE_slot.ROW_slot.TABLE_slot_info.ROW_slot_info.length; j++) {
            let temp2 = hardware.TABLE_slot.ROW_slot.TABLE_slot_info.ROW_slot_info[j];
            if (temp2.status_ok_empty && temp2.status_ok_empty.length) {
                if (temp2.model_num && temp2.model_num.length) {
                    tempArray3.push(temp2.status_ok_empty + " (" + temp2.model_num + ")");
                } else {
                    tempArray3.push(temp2.status_ok_empty);
                }

                if (temp2.type && temp2.type.length) {
                    tempArray4.push(temp2.type);
                }
            }
        }

        for (let k = 0; k < tempArray1.length; k++) {
            html += "<tr><td>" + tempArray1[k] + "</td><td>enabled</td>";

            if (k < tempArray3.length)
                html += "<td>" + tempArray3[k] + "</td>";
            else
                html += "<td></td>";
            if (k < tempArray4.length)
                html += "<td>" + tempArray4[k] + "</td></tr>";
            else
                html += "<td></td></tr>";

        }
    }

    html += "</tbody>";
    html += "</table></div>";
    let oldTable = document.getElementById('table');
    if (oldTable != undefined && oldTable.parentNode != undefined)
        oldTable.parentNode.removeChild(oldTable);
    $('#tree-container').append(html);
    document.querySelector("#full-screen-area").requestFullscreen();

};

loadFeature = function () {
    let result;
    $.ajax({
        url: 'static/d3/data/' + hostname + '/json/system/show feature.json',
        dataType: 'json',
        async: false,
        success: function (data) {
            result = data;
        }
    });
    return result;
};

loadHardware = function () {
    let result;
    $.ajax({
        url: 'static/d3/data/' + hostname + '/json/system/show hardware.json',
        dataType: 'json',
        async: false,
        success: function (data) {
            result = data;
        }
    });
    return result;
};

loadResources = function () {
    let result;
    $.ajax({
        url: 'static/d3/data/' + hostname + '/json/system/show system resources.json',
        dataType: 'json',
        async: false,
        success: function (data) {
            result = data;
        }
    });
    return result;
};
