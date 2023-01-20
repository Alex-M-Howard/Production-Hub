let currentData;
let originalData;

createUseButtons();


/**
 * Button event that filters list of blanks based on material
 */

function materialClick(click) {
  $(".mat-butts").removeClass("mat-butts-active");
  $("#blanks-table").removeClass("hidden");
  $(click.target).addClass("mat-butts-active");
  $("#results").empty();

  axios.get("/blanks/data").then((response) => {
    currentData = response.data;
    originalData = response.data;

    let material = $(click.target).text();
    let blanks = getBlanks(material);
    createTable(blanks);
    createUseButtons();
  });
}


$(".mat-butts").on("click", (click) => {
  materialClick(click)
})


/**
 * 
 * First visit to page -> get blanks data
 * call createTable
 */
axios.get("/blanks/data").then((response) => {
    currentData = response.data;
})


/**
 * 
 * @param {string} material 
 * @returns array containing filtered material
 */
const getBlanks = (material) => {

  let filteredData = currentData;

  console.log(filteredData);
  
  return filteredData.filter(blank => {
      return blank.material_name.includes(material)
  })

}


/** createTable
 * 
 * @param {JSON} data 
 * Create table row and table data elements (Every other one striped for readability)
 * Append to #results
 * 
 */
const createTable = (blanks) => {
    blanks.forEach((blank) => {
            $("#results").append(
              $(`
                <tr>
                    <td class='use-box'>
                      <div class="d-grid">
                        <button class="btn btn-primary use-button">Use</button>
                      </div>
                    </td>
                    <td class='text-center quantity'>${blank.quantity}</td>
                    <td class='text-center gauge'>${blank.gauge}</td>
                    <td class='text-center length'>${blank.length}</td>
                    <td class='text-center width'>${blank.width}</td>
                </tr>`)
            );
    })
  $("table").removeClass("hidden");
}


/** Sorting
 * 
 * Sort events
 * Calls app.js dynamicSort() and dynamicReverseSort()
 * Calls createTable()
 * 
 */
$("#gauge-sort").on("click", () => {
  let material = $(".mat-butts-active").text();
  let blanks = getBlanks(material);

  $("#results").empty();
  createTable(blanks.sort(numberSort("gauge")));
      createUseButtons();

});

$("#gauge-rev-sort").on("click", () => {
    let material = $(".mat-butts-active").text();
    let blanks = getBlanks(material);

  $("#results").empty();
  createTable(blanks.sort(numberReverseSort("gauge")));
      createUseButtons();

});

$("#quantity-sort").on("click", () => {
  let material = $(".mat-butts-active").text();
  let blanks = getBlanks(material);

  $("#results").empty();
  createTable(blanks.sort(numberSort("quantity")));
      createUseButtons();

});

$("#quantity-rev-sort").on("click", () => {
  let material = $(".mat-butts-active").text();
  let blanks = getBlanks(material);

  $("#results").empty();
  createTable(blanks.sort(numberReverseSort("quantity")));
      createUseButtons();
});

$("#length-sort").on("click", () => {
  let material = $(".mat-butts-active").text();
  let blanks = getBlanks(material);

  $("#results").empty();
  createTable(blanks.sort(numberSort("length")));
      createUseButtons();

});

$("#length-rev-sort").on("click", () => {
  let material = $(".mat-butts-active").text();
  let blanks = getBlanks(material);

  $("#results").empty();
  createTable(blanks.sort(numberReverseSort("length")));
      createUseButtons();

});

$("#width-sort").on("click", () => {
  let material = $(".mat-butts-active").text();
  let blanks = getBlanks(material);

  $("#results").empty();
  createTable(blanks.sort(numberSort("width")));
      createUseButtons();

});

$("#width-rev-sort").on("click", () => {
  let material = $(".mat-butts-active").text();
  let blanks = getBlanks(material);

  $("#results").empty();
  createTable(blanks.sort(numberReverseSort("width")));
      createUseButtons();
});

/**
 *  Add blank to database
 */
$("#add-blank").on("click", async (event) => {
  event.preventDefault();
  let errorFlag = false;
  $("#alerts").empty();

  let gauge = $("#gauge").val()
  let material = $("#material").val()
  let quantity = $("#quantity").val()
  let length = $("#length").val()
  let width = $("#width").val()

  if (!gauge) {
    showAlert("Please enter a gauge")
    errorFlag = true;
  }
  if (material === "Choose...") {
    showAlert("Please select a material")
    errorFlag = true;
  }
  if (!quantity) {
    quantity = 1;
  }
  if (!length) {
    showAlert("Please enter the length")
    errorFlag = true;
  }
  if (!width) {
    showAlert("Please enter the width")
    errorFlag = true;
  }

  if (errorFlag) { return }
    

  let newMaterial = material
  let success = true

  await axios
    .post("/blanks/inventory", { gauge, material, quantity, length, width })
    .then((response) => {
      if (response.data["success"] === false) {
          showAlert("Material not found. Check gauge and material selection.");
        success = false;
        return
      }
      
      axios.get("/blanks/data").then((response) => {
        console.log(response.data);

        currentData = response.data;
        $("#results").empty();

        
        $(".mat-butts").removeClass("mat-butts-active");
        if ($(`.mat-butts:contains(${newMaterial})`).length === 0) {
          $(".mat-butts").append(
            $(
              `<a class="nav-link mat-butts mx-1 my-1" href="#" style="width:30%;">${newMaterial}</a>`
            ));
          $(".mat-butts").on("click", (click) => {
            materialClick(click)
          });
        }
        $(`.mat-butts:contains(${newMaterial})`).addClass("mat-butts-active");

        let blanks = getBlanks(newMaterial);
        createTable(blanks);
        createUseButtons();


      });
    });
  if (!success) { return; }
  
   
  gauge = $("#gauge").val('');
  material = $("#material").val("Choose...");
  quantity = $("#quantity").val('');
  length = $("#length").val('');
  width = $("#width").val('');
  

})


/**
 * 
 * @param {string} message
 * Shows bootstrap alert based on input verification 
 */
function showAlert(message) {
  let error = $(`<div class='alert alert-danger my-0' role='alert'>${ message }</div>`)
  
  $("#alerts").append(error)
}

/**
 * Creates use button to consume a blank from inventory
 */
function createUseButtons() {
  $(".use-button").on("click", (event) => {
    let row = $(event.target).closest('tr').children();
    
    let quantity = $(row)[1].innerText;
    let gauge = $(row)[2].innerText;
    let material = $(".mat-butts-active").text();
    let length = $(row)[3].innerText;
    let width = $(row)[4].innerText;

    console.table({ quantity, gauge, material, length, width });
    
    axios.delete("/blanks/inventory", { data: { gauge, material, quantity, length, width } })

    $(row)[1].innerText = parseInt($(row)[1].innerText) - 1;
    if (parseInt($(row)[1].innerText) < 1) {
      $(event.target).closest('tr').remove()
    }

    if($("table tbody tr").length === 0) {
      $("table").addClass("hidden");
      $(`.mat-butts:contains(${material})`).remove();
    }

  })
}