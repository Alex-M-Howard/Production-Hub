$("li").on("click", function (event) {

    let li = event.target.closest("li");
    
    li.classList.toggle("process-complete");
    li.querySelector(".checkmark").classList.toggle("hidden");

    let process = li.querySelector(".col-10").textContent.toLowerCase();
    let status = li.querySelector(".checkmark").classList.contains("hidden") ? false : true;

    updateProcessStatus(process, status)
    
});


function updateProcessStatus(process, status) {
    const projectName = document.querySelector("#project-name").textContent;
    const partName = document.querySelector("#part-number").textContent;

    axios.post("/proto/update_process", { projectName, partName, process, status })
}