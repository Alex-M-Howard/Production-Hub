$("#submit").on("click", (event) => {
    event.preventDefault();
    $("#alerts").empty();
    let errors = false;
    
    if (!$("#requested_by").val()) {
        showAlert('Please enter your name');
        errors = true;
    }

    if (!$("#description").val()) {
        showAlert('Please enter a description. Quantity, Sheet Size, etc.');
        errors = true;
    }

    if (!$("#to_change").val()) {
        showAlert('Please enter a part or program to request/change');
        errors = true;
    }
    
    if (errors) { return }

    let requested_by = $("#requested_by").val()
    let to_change = $("#to_change").val()
    let description = $("#description").val()
    let request_type = $("#request_type").val()
    let job_number = null;

    axios.post("/requests/", { requested_by, to_change, description, request_type, job_number }).then(response => {
        // Unhide table and add new row
        if(response.data.success) {
            $("table").removeClass("hidden")

            let row = $(`
            <tr class="request-danger">
              <td class="text-center">${request_type}</td>
              <td class="text-center">${to_change}</td>
              <td class="text-center">${description}</td>
              <td class="text-center">${requested_by}</td>
              <td class="text-center"> </td>
            </tr>`);

            $("tbody").append(row);

            $("#requested_by").val("")
            $("#to_change").val("")
            $("#description").val("")
            $("#request_type").val("Part Request")
        }
    })
});


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
 * If admin is logged in, add a button to each row to complete the request
 */
$(".complete-btn").on("click", (event) => {
  let row = $(event.target).closest("tr").children();
  let id = $($(row)[0]).data("request_id")  // Get the id from the first td
  let job_number = $("#job_number").val()
    console.log(job_number);
  axios.delete("/requests/", {
    data: { id, job_number },
    }).then(response => {
        for (let i = 0; i < row.length; i++) {
            $(row[i]).addClass("request-success"); // Change color of row upon completion
            $(row[i]).removeClass("request-danger");
            $(row[i]).css("background-color", "#48c188");
        }  
    })
});
