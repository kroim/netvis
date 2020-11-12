renderTextFile = function (url) {
    d3.select("svg").remove();
    $('#tree-container').html('');

    var temp = url.split('/');
    var temp2 = temp[temp.length - 1].split('.');
    var title = temp2[0];
    var html = "<div class='container-fluid  text-center' id='table' style='margin-top: 10px'>";
    // html +=         "<h4 class='text-primary'>"+title+"</h4>";
    html += "<iframe src='" + url + "' style='width: 100%; height: 92vh; border:none'>";
    html += "</iframe>";
    html += "</div>";

    var oldTable = document.getElementById('table');
    if (oldTable != undefined && oldTable.parentNode != undefined)
        oldTable.parentNode.removeChild(oldTable);
    $('#tree-container').append(html);
    document.querySelector("#full-screen-area").requestFullscreen();

};