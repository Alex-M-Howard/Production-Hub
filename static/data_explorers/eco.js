$("#Home-nav").removeClass("active");
$("#eco-nav").toggleClass("active");
$("#nestCalc-nav").removeClass("active");
$("#Todo-nav").removeClass("active");
$("button:contains('SOPs')").removeClass("active");
$("button:contains('Data Explorers')").removeClass("active");
$("button:contains('Production')").removeClass("active");

let obsolete;

const columns = [
  "ECO",
  "Part",
  "Description",
  "Rev",
  "Unit",
  "Type",
  "Material Code",
  "Replaces",
  "Material Disposition",
  "Effectivity Date",
  "Continue to Buy",
  "Comments",
  {
    name: "Punch",
    sort: { enabled: true },
  },
  {
    name: "Amada",
    sort: { enabled: true },
  },
  {
    name: "Trumpf",
    sort: { enabled: true },
  },
  {
    name: "Forming",
    sort: { enabled: true },
  },
  {
    name: "Added",
    sort: true,
  },
  "Status",
];

// /**
//  *
//  * First visit to page -> get eco data
//  * call createTable
//  */
axios.get("/eco/data").then((response) => {
  for (each in response.data) {
    let date = new Date(response.data[each]["date"]);
    response.data[each]["date"] = `${date.getMonth() + 1}-${
      date.getDate() + 1
    }-${date.getFullYear()}`;

    if (response.data[each]["replaces"] == null) {
      response.data[each]["replaces"] = "";
    }
  }

  data = [];

  for (let i of response.data) {
    data.push([
      i.eco,
      i.part,
      i.description,
      i.revision,
      i.measuring_unit,
      i.item_type,
      i.material_code,
      i.replaces,
      i.material_dis,
      i.effectivity,
      i.continue_to_buy,
      i.comments,
      i.punch,
      i.amada,
      i.trumpf,
      i.form,
      i.date,
      i.status,
    ]);
  }

  new gridjs.Grid({
    columns: columns,
    data: data,
    fixedHeader: true,
    height: "72vh",
    pagination: {
      enabled: true,
      limit: 30,
    },
    search: {
      enabled: true,
    },
  }).render(document.getElementById("wrapper"));

  markObsolete();
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
        $(row).children("td")[11].innerText.includes("Obsolete")
      ) {
        let partNum = $(row).children("td")[1];

        $(partNum).append(
          $(`<br><span class="badge bg-secondary obsolete">Obsolete</span>`)
        );
      }
      if ($(row).children("td")[17].innerText.includes("Pending")) {
        let partNum = $(row).children("td")[0];

        $(partNum).append(
          $(`<br><span class="badge bg-secondary pending">Pending</span>`)
        );
      }
    } catch (err) {
      if (err instanceof TypeError) {
        console.log("Reached end of data");
      }
    }
  }
}
