window.addTable = function addTable() {
    var url = "add_table?";
    url += "tab_name=";
    url += document.getElementById("inputNewTableName").value;
    url += "&col_settings=";
    var colsJSON = {};
    var col_name, col_type;
    for (let i = 0; i < 5; i++) {
        col_name = document.getElementById(`inputNewTableColName${i}`).value;
        col_type = document.getElementById(`inputNewTableColType${i}`).value;
        if (col_name != "" && col_name != null) {
            colsJSON[col_name] = col_type;
        }
    }
    url += encodeURIComponent(JSON.stringify(colsJSON));

    var xhr = new XMLHttpRequest();
    xhr.open("GET", url, true);
    xhr.setRequestHeader("Content-Type", "text/html");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) { 
            prepareTabAdd();
        }
    };
    xhr.send();
}

window.addColumn = function addColumn () {
    var url = "add_column?";
    url += "tab_name=";
    url += document.getElementById("inputAddColTableName").value;
    url += "&col_settings=";
    var colsJSON = {};
    var col_name, col_type;
    col_name = document.getElementById("inputAddColColName").value;
    col_type = document.getElementById("inputAddColColType").value;
    if (col_name != "" && col_name != null) {
        colsJSON[col_name] = col_type;
    }
    url += encodeURIComponent(JSON.stringify(colsJSON));

    var xhr = new XMLHttpRequest();
    xhr.open("GET", url, true);
    xhr.setRequestHeader("Content-Type", "text/html");
    xhr.send();
}

window.removeColumn = function removeColumn(tabName) {
    var colName = document.getElementById(`removeColumn_${tabName}`).value;
    var url = `remove_column?tab_name=${tabName}&col_name=${colName}`;

    var xhr = new XMLHttpRequest();
    xhr.open("GET", url, true);
    xhr.setRequestHeader("Content-Type", "text/html");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) { 
            prepareTabRemove();
        }
    };
    xhr.send();
}

window.removeTable = function removeTable(tabName) {
    var url = `remove_table?tab_name=${tabName}`;

    var xhr = new XMLHttpRequest();
    xhr.open("GET", url, true);
    xhr.setRequestHeader("Content-Type", "text/html");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) { 
            prepareTabRemove();
        }
    };
    xhr.send();
}