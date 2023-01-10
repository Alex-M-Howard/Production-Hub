document.addEventListener("DOMContentLoaded", function (event) {
  function OTPInput() {
    const inputs = document.querySelectorAll(".otp");

    console.log(inputs);
    for (let i = 0; i < inputs.length; i++) {
      inputs[i].addEventListener("keydown", function (event) {
        console.log(event);
        if (event.key === "Backspace") {
          inputs[i].value = "";
          if (i !== 0) inputs[i - 1].focus();
        } else {
          if (i === inputs.length - 1 && inputs[i].value !== "") {
            return true;
          } else if (event.keyCode > 47 && event.keyCode < 58 || event.keyCode > 95 && event.keyCode < 106) {
            inputs[i].value = event.key;
            if (i !== inputs.length - 1) inputs[i + 1].focus();
            event.preventDefault();
          } else if (event.keyCode === 32 || event.keyCode === 13) {
            return true;
          }
          else {
            event.preventDefault();
            return;
          }
        }
      });
    }
  }
  OTPInput();


  const button = document.querySelectorAll("#verify");
  button[0].addEventListener("focus", function (event) {
    document.getElementById("verify").click();
    $("#verify").attr("disabled", true);
  });

});
