let data;

axios.get('/errors/data').then((response) => {
   data = response.data;
})

/**
 * Button event that filters list of blanks based on material
 */
$(".mat-butts").on("click", (event) => {
  $(".mat-butts").removeClass("mat-butts-active");
  $(event.target).addClass("mat-butts-active");
  $("#results").empty();
  
  createTable($(event.target).text())
});


function createTable(selection) {
    if(selection === 'LASERS') selection = 'Laser'
    if(selection === 'FORMING') selection = 'Forming'
    if(selection === 'OTHER') selection = 'Other'

    let errors = data

    for (let error of errors) {
        if (error.machine.includes(selection)) {
            $("#results").append(`
                <tr>
                    <td class="text-center align-middle"><a href="/errors/edit/${
                      error.id
                    }"><i class="fa-solid fa-pencil"></i></a></td>
                    <td class="text-center align-middle">${
                      error.part_number
                    }</td>
                    <td class="text-center align-middle">${error.machine}</td>
                    <td class="text-center align-middle">${
                      error.description
                    }</td>
                    <td class="text-center align-middle">${
                      error.root_cause
                    }</td>
                    <td class="text-center align-middle">${error.notes}</td>
                    <td class="text-center align-middle">${error.name}</td>
                    <td class="text-center align-middle">${getFormattedDate(
                      error.date)}</td>
                    <td class="text-center align-middle"><a href="/errors/${error.id}"><i class="fa-solid fa-circle-info"></i></a></td>
               </tr>
            `);
        }
    }
}

function getFormattedDate(date) {
    const MONTHS = {
        "Jan": "01",
        "Feb": "02",
        "Mar": "03",
        "Apr": "04",
        "May": "05",
        "Jun": "06",
        "Jul": "07",
        "Aug": "08",
        "Sep": "09",
        "Oct": "10",
        "Nov": "11",
        "Dec": "12"
    } 

    date = date.split(" ")

    let month = MONTHS[date[2]]
    let day = date[1]
    let year = date[3]

    return `${month}/${day}/${year}`
}
