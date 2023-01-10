/**
 * Button event that filters list of prototypes
 */
$(".mat-butts").on("click", async (event) => {
  $(".mat-butts").removeClass("mat-butts-active");
  $(event.target).addClass("mat-butts-active");

  let status = $(event.target).text();

  $("thead").empty()
  $("tbody").empty()

  if (status === "Incomplete") {

    $("thead").append(`
      <tr>
        <th scope="col" class="text-center">Project Name</th>
        <th scope="col" class="text-center">Created</th>
        <th scope="col" class="text-center">Last Updated</th>
        <th scope="col" class="text-center">By</th>
        <th scope="col" class="text-center">Type</th>
        <th scope="col" class="text-center">Product Line</th>
        <th scope="col" class="text-center">ECO #</th>
        <th scope="col" class="text-center">Requested Completion Date</th>
        <th scope="col" class="text-center">Notes</th>
      </tr>
    `);

    axios.get(`/proto/get_my_projects_incomplete`).then((response) => {
      for (let i = 0; i < response.data.length; i++) {
        $("tbody").append(`
            <tr>
              <th scope="row" class="text-center"><a href="/proto/${response.data[i].project_name}">${response.data[i].project_name}</a></td>
              <td class="text-center">${response.data[i].created}</td>
              <td class="text-center">${response.data[i].updated}</td>
              <td class="text-center">${response.data[i].updated_by}</td>
              <td class="text-center">${response.data[i].project_type}</td>
              <td class="text-center">${response.data[i].product_line}</td>
              <td class="text-center">${response.data[i].eco}</td>
              <td class="text-center">${response.data[i].date_requested}</td>
              <td class="text-center">${response.data[i].notes}</td>
            </tr>
        `);
      }
    });
  } else {

    $("thead").append(`
      <tr>
        <th scope="col" class="text-center">Project Name</th>
        <th scope="col" class="text-center">Created</th>
        <th scope="col" class="text-center">Last Updated</th>
        <th scope="col" class="text-center">Completed</th>
        <th scope="col" class="text-center">Type</th>
        <th scope="col" class="text-center">Product Line</th>
        <th scope="col" class="text-center">ECO #</th>
        <th scope="col" class="text-center">Requested Completion Date</th>
        <th scope="col" class="text-center">Notes</th>
      </tr>
    `);
  

    axios.get(`/proto/get_my_projects_complete`).then((response) => {
      for (let i = 0; i < response.data.length; i++) {
        $("tbody").append(`
            <tr>
              <th scope="row" class="text-center"><a href="/proto/${response.data[i].project_name}">${response.data[i].project_name}</a></td>
              <td class="text-center">${response.data[i].created}</td>
              <td class="text-center">${response.data[i].updated}</td>
              <td class="text-center">${response.data[i].completed}</td>
              <td class="text-center">${response.data[i].project_type}</td>
              <td class="text-center">${response.data[i].product_line}</td>
              <td class="text-center">${response.data[i].eco}</td>
              <td class="text-center">${response.data[i].date_requested}</td>
              <td class="text-center">${response.data[i].notes}</td>
            </tr>
        `);
      }
    });
  }
});
