let amadaData = [];
let trumpfData = [];
let punchData = [];

const amadaColumns = [
  { name: "Nest", sort: { enabled: true } },
  "Nested With",
  { name: "Gauge", sort: { enabled: true }, width: "120px" },
  { name: "Material", sort: { enabled: true }, width: "125px" },
  { name: "Size X", sort: { enabled: true }, width: "115px" },
  { name: "Size Y", sort: { enabled: true }, width: "115px" },
  "Scrap",
  "Time (Min)",
  "Date",
];

const trumpfColumns = [
  { name: "Nest", sort: { enabled: true } },
  "Nested With",
  { name: "Gauge", sort: { enabled: true }, width: "120px" },
  { name: "Material", sort: { enabled: true }, width: "125px" },
  { name: "Size X", sort: { enabled: true }, width: "115px" },
  { name: "Size Y", sort: { enabled: true }, width: "115px" },
  "Scrap",
  "Time (Min)",
  "Date",
];

const punchColumns = [
  { name: "Nest", sort: { enabled: true }, width: "85px" },
  { name: "Nested With", width: "30vw" },
  { name: "Gauge", sort: { enabled: true }, width: "115px" },
  { name: "Material", sort: { enabled: true }, width: "150px" },
  { name: "Size X", sort: { enabled: true }, width: "115px" },
  { name: "Size Y", sort: { enabled: true }, width: "115px" },
  { name: "Forming?", sort: { enabled: true }, width: "135px" },
  { name: "Workholding Change?", sort: { enabled: true }, width: "250px" },
  "Date",
];

$("#trumpf-button").on("click", async () => {
  $("#amada-wrapper").hide();
  $("#punch-wrapper").hide();
  $("#trumpf-wrapper").show();
  $(".explorer-buttons").removeClass("explorer-buttons-active");
  $("#trumpf-button").addClass("explorer-buttons-active");

  if (trumpfData.length === 0) {
    await axios.get("/trumpf/data").then((response) => {
      for (let i of response.data) {
        trumpfData.push([
          i.nest_name,
          i.nested_with,
          i.gauge,
          i.material,
          i.sheet_x,
          i.sheet_y,
          i.scrap,
          i.time,
          i.date,
        ]);
      }
    });
  }

  new gridjs.Grid({
    columns: trumpfColumns,
    data: trumpfData,
    fixedHeader: true,
    height: "72vh",
    autoWidth: true,
    pagination: {
      enabled: true,
      limit: 30,
    },
    search: {
      enabled: true,
    },
  }).render(document.getElementById("trumpf-wrapper"));
});

$("#punch-button").on("click", async () => {
  $("#trumpf-wrapper").hide();
  $("#punch-wrapper").hide();
  $("#punch-wrapper").show();
  $(".explorer-buttons").removeClass("explorer-buttons-active");
  $("#punch-button").addClass("explorer-buttons-active");
  console.log(punchData);
  if (punchData.length === 0) {
    await axios.get("/punch/data").then((response) => {
      for (let i of response.data) {
        punchData.push([
          i.nest_name,
          i.nested_with,
          i.gauge,
          i.material,
          i.sheet_x,
          i.sheet_y,
          String(i.punch_forming),
          String(i.clamp_position_change),
          i.date,
        ]);
      }
    });
  }

  new gridjs.Grid({
    columns: punchColumns,
    data: punchData,
    fixedHeader: true,
    height: "72vh",
    pagination: {
      enabled: true,
      limit: 30,
    },
    search: {
      enabled: true,
    },
  }).render(document.getElementById("punch-wrapper"));
});

$("#amada-button").on("click", async () => {
  $("#trumpf-wrapper").hide();
  $("#punch-wrapper").hide();
  $("#amada-wrapper").show();
  $(".explorer-buttons").removeClass("explorer-buttons-active");
  $("#amada-button").addClass("explorer-buttons-active");

  if (amadaData.length === 0) {
    await axios.get("/amada/data").then((response) => {
      for (let i of response.data) {
        amadaData.push([
          i.nest_name,
          i.nested_with,
          i.gauge,
          i.material,
          i.sheet_x,
          i.sheet_y,
          i.scrap,
          i.time,
          i.date,
        ]);
      }
    });
  }

  new gridjs.Grid({
    columns: amadaColumns,
    data: amadaData,
    fixedHeader: true,
    height: "72vh",
    autoWidth: true,
    pagination: {
      enabled: true,
      limit: 30,
    },
    search: {
      enabled: true,
    },
  }).render(document.getElementById("amada-wrapper"));
});
