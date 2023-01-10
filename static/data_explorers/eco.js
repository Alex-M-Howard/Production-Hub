const MAX_ROWS = 200;

$('#Home-nav').removeClass('active')
$('#eco-nav').toggleClass('active')
$('#nestCalc-nav').removeClass('active')
$('#Todo-nav').removeClass('active')
$("button:contains('SOPs')").removeClass("active");
$("button:contains('Data Explorers')").removeClass("active");
$("button:contains('Production')").removeClass("active");

let currentData;
let originalData;
let filtering;
let obsolete;




/**
 * 
 * First visit to page -> get eco data
 * call createTable
 */
axios.get("/eco/data").then((response) => {
  $("#results").empty();
  $("#loading").hide();
  $("table").toggleClass("hidden");

  for (each in response.data) {
    let date = new Date(response.data[each]["date"]);
    response.data[each]["date"] = `${date.getMonth()+1}-${date.getDate()+1}-${date.getFullYear()}`;
    
    if (response.data[each]["replaces"] == null) {
      response.data[each]["replaces"] = "";
    }
  }
  createTable(response.data);
  currentData = response.data;
  originalData = response.data;
});




/** createTable
 * 
 * @param {JSON} data 
 * Will iterate first MAX_ROW elements (for loading speed)
 * Create table row and table data elements (Every other one striped for readability)
 * Append to #results
 * Call markObsolete after table rows created
 * 
 */
const createTable = (data) => {
  let punchStatus, amadaStatus, trumpfStatus, formingStatus;

  for (let nest = 0; nest < MAX_ROWS; nest++) {
    if (data[nest]["punch"] == "Completed") {
      punchStatus = '<i class="fa-solid fa-check text-success"></i>';
    } else if (data[nest]["punch"] == "N/A") {
      punchStatus = "N/A";
    } else {
      punchStatus = '<i class="fa-solid fa-xmark text-danger"></i>';
    }
    
    if (data[nest]["amada"] == "Completed") {
      amadaStatus = '<i class="fa-solid fa-check text-success"></i>';
    } else if (data[nest]["amada"] == "N/A") {
      amadaStatus = "N/A";
    } else {
      amadaStatus = '<i class="fa-solid fa-xmark text-danger"></i>';
    }
    
    if (data[nest]["trumpf"] == "Completed") {
      trumpfStatus = '<i class="fa-solid fa-check text-success"></i>';
    } else if (data[nest]["trumpf"] == "N/A") {
      trumpfStatus = "N/A";
    } else {
      trumpfStatus = '<i class="fa-solid fa-xmark text-danger"></i>';
    }
    
    if (data[nest]["form"] == "Completed") {
      formingStatus = '<i class="fa-solid fa-check text-success"></i>';
    } else if (data[nest]["forming"] == "N/A") {
      formingStatus = 'N/A';
    } else {
      formingStatus = '<i class="fa-solid fa-xmark text-danger"></i>';
    }



    try {
        $("#results").append(
          $(`
      <tr class='table-row'>
        <td class='eco text-center align-middle'>${data[nest]["eco"]}</td>
        <td class='part text-center align-middle'>${data[nest]["part"]}</td>
        <td class='description align-middle'>${data[nest]["description"]}</td>
        <td class='revision text-center align-middle'>${data[nest]["revision"]}</td>
        <td class='measuring_unit text-center align-middle'>${data[nest]["measuring_unit"]}</td>
        <td class='item_type text-center align-middle'>${data[nest]["item_type"]}</td>
        <td class='material_code text-center align-middle'>${data[nest]["material_code"]}</td>
        <td class='replaces text-center align-middle'>${data[nest]["replaces"]}</td>
        <td class='material_dis text-center align-middle'>${data[nest]["material_dis"]}</td>
        <td class='effectivity text-center align-middle'>${data[nest]["effectivity"]}</td>
        <td class='continue_to_buy text-center align-middle'>${data[nest]["continue_to_buy"]}</td>
        <td class='comments text-center align-middle'>${data[nest]["comments"]}</td>
        <td class='punch text-center align-middle'>${punchStatus}</td>
        <td class='amada text-center align-middle'>${amadaStatus}</td>
        <td class='trumpf text-center align-middle'>${trumpfStatus}</td>
        <td class='form text-center align-middle'>${formingStatus}</td>
        <td class='date text-center align-middle'>${data[nest]["date"]}</td>
        <td class='status text-center align-middle'>${data[nest]["status"]}</td>
      </tr>`)
        );

    } catch (err) {
      if (err instanceof TypeError) {
        console.log("Reached end of data");
        break;
      }
    }
  }
  
  markObsolete();
};


/** User Input Filters
 * Filter input boxes on keyup
 * If another keyup before timer finished, canceled
 * Filter data to include user input
 */
$(".filter").on("keyup", () => {
  if (
    !$("#eco-filter").val() &&
    !$("#part-filter").val() &&
    !$("#description-filter").val() &&
    !$("#replaces-filter").val() &&
    !$("#status-filter").val()
  ) {
    currentData = originalData;
  }

  clearTimeout(filtering);

  filtering = setTimeout(() => {
    let filteredData = currentData;

    filteredData = filteredData.filter((nest) => {
      return (
          nest.eco.includes($("#eco-filter").val()) &&
          nest.part.includes($("#part-filter").val()) &&
          nest.description.includes($("#description-filter").val()) &&
          nest.replaces.includes($("#replaces-filter").val()) &&
          nest.status.includes($("#status-filter").val())
        );
      
    });
      $("#results").empty();
      
    createTable(filteredData);
  
      
    }, 200);
});


/** markObsolete
 * 
 * Select Table Rows
 * If TD[1](Part #) is in obsolete parts
 * Create badge marking 'Obsolete'
 * If part pending, create badge marking 'Pending'
 */
async function markObsolete() {

  // If obsolete data exists don't do another axios call
  if (!obsolete) {
    let response = await axios.get("/eco/data/obsolete");
    obsolete = response.data;
  }

  let rows = $("tr");

  for (row of rows) {
    if (row === rows[0] || row === rows[1]) continue;

    try {
      if (
        obsolete.indexOf($(row).children("td")[1].innerText) !== -1 ||
        $(row).children("td")[11].innerText.includes('Obsolete')
      ) {
        let partNum = $(row).children("td")[1];

        $(partNum).append($(`<br><span class="badge bg-secondary obsolete">Obsolete</span>`));
      }
      if ($(row).children("td")[17].innerText.includes('Pending')) {
        let partNum = $(row).children("td")[0];

        $(partNum).append($(`<br><span class="badge bg-secondary pending">Pending</span>`));
      }
    } catch (err) {
      if (err instanceof TypeError) {
        console.log("Reached end of data");
      }
    }
  }
}
