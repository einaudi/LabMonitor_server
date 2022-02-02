import { create, render, expand } from './json-view.js';

window.getDBTree = function getDBTree(callback) {
  callback = callback || function() {};
  var xhr = new XMLHttpRequest();
  xhr.open("GET", "get_db_tree", true);
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.onreadystatechange = function () {
      if (xhr.readyState === 4 && xhr.status === 200) {    
        callback(JSON.parse(xhr.responseText));  
      }
  };
  xhr.send();
}

window.setDBTree = function setDBTree(){
  getDBTree(function(data) {
    const tree = create(data);
    render(tree, document.querySelector('.dbTree'));
    expand(tree);
  })
}

window.openTab = function openTab(evt, tabName) {
    // Declare all variables
    var i, tabcontent, tablinks;
  
    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
  
    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // Tab specifics
    if (tabName == 'DB tree') {
      document.getElementById('DB tree').innerHTML = "<p class=\"dbTree\"></p>";
      setDBTree();      
    }
  
    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}

// Tabs preparation
window.prepareAddTable = function prepareAddTable() {
  var addTableHTML = `
  <label>New table name:</label>
  <input id="inputNewTableName" type="text"><br><br>
  <table>
    <tr>
      <th>Column name</th>
      <th>Column type</th>
    </tr>
  `;
  for (let i = 0; i < 5; i++) {
    addTableHTML += `
    <tr>
      <th>
        <input id="inputNewTableColName${i}" type="text" value="">
      </th>
      <th>
        <select id="inputNewTableColType${i}" name="coltypes">
          <option value="real">real</option>
          <option value="varchar(255)">string</option>
        </select>
      </th>
    </tr>
    `;
  }
  
  addTableHTML += `
  </table><br>
  <button id="buttonNewTable" onclick="addTable()">Add table</button>
  `;

  document.getElementById('Add table').innerHTML = addTableHTML;
}

window.prepareRemove = function prepareRemove() {
  getDBTree(function(data) {
    var removeHTML = ``;

    for (var tab_name in data) {
      removeHTML += `
      <h2>Table ${tab_name}
      <button onclick="removeTable('${tab_name}')">Remove table</button>
      </h2>
      <p>
      Remove column <select id="removeColumn_${tab_name}" name="colnames">
      `;
      for (var col_name in data[tab_name]) {
        removeHTML += `
        <option value=${col_name}>${col_name}</option>
        `;
      }
      removeHTML += `
      </select>
      <button onclick="removeColumn('${tab_name}')">Remove column</button>
      </p>
      `;
    }

    document.getElementById('Remove').innerHTML = removeHTML;
  });
}

window.prepareTabs = function prepareTabs(evt) {
  // Prepare Add table tab
  prepareAddTable();
  // Prepare Remove tab
  prepareRemove();

  // Prepare and show db tree
  openTab(evt, 'DB tree');
}
