$("#Home-nav").removeClass("active");
$("#eco-nav").removeClass("active");
$("#nestCalc-nav").toggleClass("active");
$("#Todo-nav").removeClass("active");
$("button:contains('SOPs')").removeClass("active");

/**
 * Set all inputs to empty
 */
document.addEventListener("DOMContentLoaded", () => {
  $("#bends").val("");
  $("#rolls").val("");
  $("#hours").val("");
  $("#minutes").val("");
  $("#seconds").val("");
  $("#fillers").val("None");
  $("#part_x").val("");
  $("#part_y").val("");
  $("#sheet_x").val("");
  $("#sheet_y").val("");
  $("#spacing").val("");
  $("#forming-time").text("N/A");
  $("#laser-time").text("N/A");
});

const body = $("body");
const nestingSubmitButton = $("#nest-submit");
const results = $("#nesting-results");
let fillerNum;

$(nestingSubmitButton).on("click", (event) => {
  event.preventDefault();
  $("#nesting-results").empty();

  data = checkInput();
  displayResults(data);
});

$(body).on("keydown", () => {
  getRoutingInput();
});
$(body).on("keyup", () => {
  getRoutingInput();
});
