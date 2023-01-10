/**
 * 
 * @param {float} part_x 
 * @param {float} part_y 
 * @param {float} sheet_x 
 * @param {float} sheet_y 
 * @param {float} margins 
 * @param {float} spacing 
 * @returns [#partsXdirection, #partsYdirection, ExpectedTotal,RoughScrap%]
 */
const parts_possible_on_sheet = (
  part_x,
  part_y,
  sheet_x,
  sheet_y,
  margins,
  spacing
) => {
  let real_sheet_x = sheet_x - margins * 2;
  let real_sheet_y = sheet_y - margins * 2;

  let parts_in_x = Math.floor(real_sheet_x / part_x);
  let parts_in_y = Math.floor(real_sheet_y / part_y);

  let part_spacing_x = (parts_in_x - 1) * spacing;
  let part_spacing_y = (parts_in_y - 1) * spacing;

  while (parts_in_x * part_x + part_spacing_x > real_sheet_x) {
    parts_in_x--;
  }
  while (parts_in_y * part_y + part_spacing_y > real_sheet_y) {
    parts_in_y--;
  }

  let expected_output = parts_in_x * parts_in_y;
  let rough_scrap =
    100 - ((expected_output * (part_x * part_y)) / (sheet_x * sheet_y)) * 100;
  rough_scrap = Math.round((rough_scrap + Number.EPSILON) * 100) / 100;

  return [parts_in_x, parts_in_y, expected_output, rough_scrap];
};

/**
 * 
 * @returns JSON of parts possible on sheet
 */
function checkInput() {
  let filler = $("#fillers").val();
  let partX = $("#part_x").val();
  let partY = $("#part_y").val();
  let sheetX = $("#sheet_x").val();
  let sheetY = $("#sheet_y").val();
  let spacing = $("#spacing").val();
  let material = filler.slice(4);
  let gauge = filler.slice(0, 3);
  let rotate = $("#rotate").is(":checked");

  if (!partX && !partY && !sheetX && !sheetY) return;
  if (spacing === "") {
    spacing = 0.4;
  }

  const results = {
    regular: [],
    rotated: [],
    "filler-top": [],
    "filler-side": [],
    "filler-top-rotated": [],
    "filler-side-rotated": [],
  };

  for (let i = 0.2; i < 0.6; i += 0.1) {
    if (i > 0.2 && i < 0.4) {
      i = 0.3;
    }

    results["regular"].push(
      parts_possible_on_sheet(partX, partY, sheetX, sheetY, i, spacing)
    );
    if (rotate) {
      results["rotated"].push(
        parts_possible_on_sheet(partY, partX, sheetX, sheetY, i, spacing)
      );
    }

    if (filler !== "None") {
      fillerNum = fillerParts[0][gauge][material][0]["partNum"];
      let fillerX = fillerParts[0][gauge][material][0]["partX"];
      let fillerY = fillerParts[0][gauge][material][0]["partY"];
      let sideX =
        sheetX - results["regular"][results["regular"].length - 1][0] * partX;
      let topY =
        sheetY - results["regular"][results["regular"].length - 1][1] * partY;

      results["filler-top"].push(
        parts_possible_on_sheet(fillerX, fillerY, sheetX, topY, i, spacing)
      );
      results["filler-side"].push(
        parts_possible_on_sheet(fillerX, fillerY, sideX, sheetY, i, spacing)
      );
      if (rotate) {
        results["filler-top-rotated"].push(
          parts_possible_on_sheet(fillerY, fillerX, sheetX, topY, i, spacing)
        );
        results["filler-side-rotated"].push(
          parts_possible_on_sheet(fillerY, fillerX, sideX, sheetY, i, spacing)
        );
      }
    }
  }
  return results;
}

/**
 * 
 * @param {JSON} data
 * Creates table with expected output 
 */
function displayResults(data) {
  const resultsTable = $("#nesting-results");
  for (array in data) {
    array.includes("filler") ? (fillnum = fillerNum) : (fillnum = "");

    if (data[array].length > 0) {
      resultsTable.append(
        $(`<table class="table my-2" id=${array}>
          <caption class="text-center">${array} ${fillnum}</caption>
                  <tr>
                      <th scope="col">Margins</th>
                      <th scope="col">Expected X</th>
                      <th scope="col">Expected Y</th>
                      <th scope="col">Expected Total</th>
                      <th scope="col">Rough Scrap</th>
                  </tr>
            </table>
            <br>   
        `)
      );

      for (let idx = 0, i = 0.2; idx < data[array].length; idx++, i += 0.1) {
        if (i > 0.2 && i < 0.4) {
          i = 0.3;
        }

        $(`#${array}`)
          .last("tr")
          .append(
            $("<tr scope='row'>"),
            $(`<td>${i}</td>`),
            $(`<td>${data[array][idx][0]}</td>`),
            $(`<td>${data[array][idx][1]}</td>`),
            $(`<td>${data[array][idx][2]}</td>`),
            $(`<td>${data[array][idx][3]}%</td>`),
            $("<tr>")
          );
      }
    }
  }
}
