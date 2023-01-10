const MAX_ROWS = 200;

// Initialize data variables
let trumpfData = [];
let amadaData = [];
let punchData = [];
let formingData = [1];
let machine, filtering, dataLoading;

let currentTrumpfData = [];
let currentAmadaData = [];
let currentPunchData = [];
let currentFormingData = [];

/**
 * When visiting at first, get data from server
 *
 */

axios.get("/trumpf/data").then((response) => {
  trumpfData = response.data;
  currentTrumpfData = response.data;

  $("#explorer-buttons").append(
    $(`<a class="nav-link explorer-buttons mx-1 my-1" href="#" style="width:2rem">
      Trumpf Laser
    </a>`)
  );
  addExplorerListeners();
  if (amadaData.length > 0 && punchData.length > 0 && formingData.length > 0) {
    $("#loading").addClass("hidden");
  }
});

axios.get("/amada/data").then((response) => {
  amadaData = response.data;
  currentAmadaData = response.data;
  $("#explorer-buttons").append(
    $(`<a class="nav-link explorer-buttons mx-1 my-1" href="#" style="width:2rem">
      Amada Laser
    </a>`)
  );
  addExplorerListeners();
  if (trumpfData.length > 0 && punchData.length > 0 && formingData.length > 0) {
    $("#loading").addClass("hidden");
  }
});

axios.get("/punch/data").then((response) => {
  punchData = response.data;
  currentPunchData = response.data;
  $("#explorer-buttons").append(
    $(`<a class="nav-link explorer-buttons mx-1 my-1" href="#" style="width:2rem">
      Punch
    </a>`)
  );
  addExplorerListeners();
  if (amadaData.length > 0 && trumpfData.length > 0 && formingData.length > 0) {
    $("#loading").addClass("hidden");
  }
});

// axios.get("/forming/data").then((response) => {
//     formingData = response.data;
//     currentFormingData = response.data;
// });

/**
 * Event listeners for data explorer buttons
 */
function addExplorerListeners() {
  $(".explorer-buttons").on("click", (click) => {
    selectExplorer(click);
  });
}

/**
 * Button event that chooses data explorer
 */

function selectExplorer(click) {
  machine = click.target.innerText;

  dataLoading = true;

  $(".explorer-buttons").removeClass("explorer-buttons-active");
  $(click.target).addClass("explorer-buttons-active");

  $("div.trumpf").addClass("hidden");
  $("div.amada").addClass("hidden");
  $("div.punch").addClass("hidden");
  $("div.forming").addClass("hidden");

  $("table.trumpf").addClass("hidden");
  $("table.amada").addClass("hidden");
  $("table.punch").addClass("hidden");
  $("table.forming").addClass("hidden");

  $("tbody.results").empty();
  
  $("#trumpf-nest-filter").val("");
  $("#trumpf-nested_with-filter").val("");
  $("#trumpf-gauge-filter").val("");
  $("#trumpf-material-filter").val("");
  $("#trumpf-size_x-filter").val("");
  $("#trumpf-size_y-filter").val("");

  $("#amada-nest-filter").val("");
  $("#amada-nested_with-filter").val("");
  $("#amada-gauge-filter").val("");
  $("#amada-material-filter").val("");
  $("#amada-size_x-filter").val("");
  $("#amada-size_y-filter").val("");

  $("#punch-nest-filter").val("");
  $("#punch-nested_with-filter").val("");
  $("#punch-gauge-filter").val("");
  $("#punch-material-filter").val("");
  $("#punch-size_x-filter").val("");
  $("#punch-size_y-filter").val("");

  if (machine === "Trumpf Laser") {
    $("div.trumpf").removeClass("hidden");
    createTrumpfTable(trumpfData);
    $("table.trumpf").removeClass("hidden");
    $(".trumpf-filter").on("keyup", trumpfFiltering);
  }

  if (machine === "Amada Laser") {
    $("div.amada").removeClass("hidden");
    createAmadaTable(amadaData);
    $("table.amada").removeClass("hidden");
    $(".amada-filter").on("keyup", amadaFiltering);
  }

  if (machine === "Punch") {
    $("div.punch").removeClass("hidden");
    createPunchTable(punchData);
    $("table.punch").removeClass("hidden");
    $(".punch-filter").on("keyup", punchFiltering);
  }

  if (machine === "Forming") {
    $("div.forming").removeClass("hidden");
    createFormingTable(formingData);
  }
}

/** createTrumpfTable
 *
 * @param {JSON} data
 * Will iterate first MAX_ROW elements (for loading speed)
 * Create table row and table data elements (Every other one striped for readability)
 * Append to #results
 *
 */
function createTrumpfTable(data) {
  try {
    for (let nest = 0; nest < MAX_ROWS; nest++) {
        $(".results").append(
          $(`
      <tr class='table-row'>
        <td class='nest text-center align-middle'>${data[nest]["nest_name"]}</td>
        <td class='nested_with text-center align-middle'>${data[nest]["nested_with"]}</td>
        <td class='gage text-center align-middle'>${data[nest]["gauge"]}</td>
        <td class='material text-center align-middle'>${data[nest]["material"]}</td>
        <td class='size_x text-center align-middle'>${data[nest]["sheet_x"]}</td>
        <td class='size_y text-center align-middle'>${data[nest]["sheet_y"]}</td>
        <td class='rough_scrap text-center align-middle'>${data[nest]["scrap"]}</td>
        <td class='time text-center align-middle'>${data[nest]["process_time"]}</td>
        <td class='date text-center align-middle'>${data[nest]["date"]}</td>
      </tr>`)
        );
    }
  } catch (err) {
    console.error(err);
  }
}

/** createAmadaTable
 *
 * @param {JSON} data
 * Will iterate first MAX_ROW elements (for loading speed)
 * Create table row and table data elements (Every other one striped for readability)
 * Append to #results
 *
 */
function createAmadaTable(data) {
  for (let nest = 0; nest < MAX_ROWS; nest++) {
    try {
        $(".results").append(
          $(`
      <tr class='table-row'>
        <td class='nest text-center align-middle'>${data[nest]["nest_name"]}</td>
        <td class='nested_with text-center align-middle'>${data[nest]["nested_with"]}</td>
        <td class='gage text-center align-middle'>${data[nest]["gauge"]}</td>
        <td class='material text-center align-middle'>${data[nest]["material"]}</td>
        <td class='size_x text-center align-middle'>${data[nest]["sheet_x"]}</td>
        <td class='size_y text-center align-middle'>${data[nest]["sheet_y"]}</td>
        <td class='scrap text-center align-middle'>${data[nest]["scrap"]}</td>
        <td class='time text-center align-middle'>${data[nest]["process_time"]}</td>
        <td class='date text-center align-middle'>${data[nest]["date"]}</td>
      </tr>`)
        );
    } catch (error) {
      console.log(error);
    }
  }
}

/** createPunchTable
 *
 * @param {JSON} data
 * Will iterate first MAX_ROW elements (for loading speed)
 * Create table row and table data elements (Every other one striped for readability)
 * Append to #results
 *
 */
function createPunchTable(data) {
  for (let nest = 0; nest < MAX_ROWS; nest++) {
    try {
      $("#punch-results").append(
          $(`
      <tr class='table-row'>
        <td class='nest text-center align-middle'>${data[nest]["nest_name"]}</td>
        <td class='nested_with text-center align-middle'>${data[nest]["nested_with"]}</td>
        <td class='gage text-center align-middle'>${data[nest]["gauge"]}</td>
        <td class='material text-center align-middle'>${data[nest]["material"]}</td>
        <td class='size_x text-center align-middle'>${data[nest]["sheet_x"]}</td>
        <td class='size_y text-center align-middle'>${data[nest]["sheet_y"]}</td>
        <td class='scrap text-center align-middle'>${data[nest]["punch_forming"]}</td>
        <td class='rough_scrap text-center align-middle'>${data[nest]["clamp_position_change"]}</td>
        <td class='date text-center align-middle'>${data[nest]["date"]}</td>
      </tr>`)
        );
    } catch (error) {
      console.log(error);
    }
  }
}

/** User Input Filters - Punch
 * Filter input boxes on keyup
 * If another keyup before timer finished, canceled
 * Filter data to include user input
 */
function punchFiltering() {
  if (
    !$("#punch-nest-filter").val() &&
    !$("#punch-gauge-filter").val() &&
    !$("#punch-nested_with-filter").val() &&
    !$("#punch-material-filter").val() &&
    !$("#punch-size_x-filter").val() &&
    !$("#punch-size_y-filter").val()
  ) {
    console.log('All data is empty');
    currentPunchData = punchData;
  }

  clearTimeout(filtering);

  filtering = setTimeout(() => {
    let filteredData = currentPunchData;

    filteredData = filteredData.filter((nest) => {
      return (
          nest.nest_name.includes($("#punch-nest-filter").val()) &&
          String(nest.gauge).includes($("#punch-gauge-filter").val()) &&
          nest.nested_with.includes($("#punch-nested_with-filter").val()) &&
          nest.material.includes($("#punch-material-filter").val()) &&
          String(nest.sheet_x).includes($("#punch-size_x-filter").val()) &&
          String(nest.sheet_y).includes($("#punch-size_y-filter").val())
        );
      
    });
    
    $("#punch-results").empty();
    
    createPunchTable(filteredData);
    }, 200);
}

/** User Input Filters - Amada
 * Filter input boxes on keyup
 * If another keyup before timer finished, canceled
 * Filter data to include user input
 */
function amadaFiltering() {
  if (
    !$("#amada-nest-filter").val() &&
    !$("#amada-gauge-filter").val() &&
    !$("#amada-nested_with-filter").val() &&
    !$("#amada-material-filter").val() &&
    !$("#amada-size_x-filter").val() &&
    !$("#amada-size_y-filter").val()
  ) {
    console.log('All data is empty');
    currentAmadaData = amadaData;
  }

  clearTimeout(filtering);

  filtering = setTimeout(() => {
    let filteredData = currentAmadaData;

    filteredData = filteredData.filter((nest) => {
      return (
          nest.nest_name.includes($("#amada-nest-filter").val()) &&
          String(nest.gauge).includes($("#amada-gauge-filter").val()) &&
          nest.nested_with.includes($("#amada-nested_with-filter").val()) &&
          nest.material.includes($("#amada-material-filter").val()) &&
          String(nest.sheet_x).includes($("#amada-size_x-filter").val()) &&
          String(nest.sheet_y).includes($("#amada-size_y-filter").val())
        );
      
    });
    
    $("#amada-results").empty();
    
    createAmadaTable(filteredData);
    }, 200);
}

/** User Input Filters - Trumpf
 * Filter input boxes on keyup
 * If another keyup before timer finished, canceled
 * Filter data to include user input
 */
function trumpfFiltering() {
  if (
    !$("#trumpf-nest-filter").val() &&
    !$("#trumpf-gauge-filter").val() &&
    !$("#trumpf-nested_with-filter").val() &&
    !$("#trumpf-material-filter").val() &&
    !$("#trumpf-size_x-filter").val() &&
    !$("#trumpf-size_y-filter").val()
  ) {
    console.log('All data is empty');
    currentTrumpfData = trumpfData;
  }

  clearTimeout(filtering);

  filtering = setTimeout(() => {
    let filteredData = currentTrumpfData;

    filteredData = filteredData.filter((nest) => {
      return (
          nest.nest_name.includes($("#trumpf-nest-filter").val()) &&
          String(nest.gauge).includes($("#trumpf-gauge-filter").val()) &&
          nest.nested_with.includes($("#trumpf-nested_with-filter").val()) &&
          nest.material.includes($("#trumpf-material-filter").val()) &&
          String(nest.sheet_x).includes($("#trumpf-size_x-filter").val()) &&
          String(nest.sheet_y).includes($("#trumpf-size_y-filter").val())
        );
      
    });
    
    $("#trumpf-results").empty();
    
    createTrumpfTable(filteredData);
    }, 200);
}


