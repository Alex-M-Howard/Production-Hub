let data;

axios.get("/issues/data").then((response) => {
  data = response.data;
  addEvents();
});

function addEvents() {
  $(".mat-butts").on("click", (event) => {
    $(".mat-butts").removeClass("mat-butts-active");
    $(event.target).addClass("mat-butts-active");
    $("#issues").empty();
    createIssueCards($(event.target).attr("id"));
  });
}
async function createIssueCards(status) {
  console.log(data);
  if (status === "incomplete") {
    for (let issue of data) {
      console.log(issue.state);
      if (issue.state === "open") {
        $("#issues").append(`
            <div class="card my-3">
                <div class="container">
                    <div class="row card-header">
                        <div class="col-8">
                            <h3>${issue.title}</h3>
                        </div>
                        <div class="col-4">
                            <h6 class="text-center">${issue.created_at}</h6>
                        </div>
                    </div>
                </div>
                <div class="card-body">
                    <p class="card-text">${issue.body}</p>    
                </div>
            </div>`);
      }
    }
  } else {
    for (let issue of data) {
      console.log(issue.state);
      if (issue.state === "closed") {
        $("#issues").append(`
            <div class="card my-3">
                <div class="container">
                    <div class="row card-header">
                        <div class="col-8">
                            <h3>${issue.title}</h3>
                        </div>
                        <div class="col-4">
                            <h6 class="text-center">${issue.created_at}</h6>
                        </div>
                    </div>
                </div>
                <div class="card-body">
                    <p class="card-text">${issue.body}</p>    
                </div>
            </div>`);
      }
    }
  }
}
