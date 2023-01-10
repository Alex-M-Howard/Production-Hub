$("#confirmPassword").keyup(() => {
  console.log($("#password").val()); 

  if ($("#password").val() !== $("#confirmPassword").val()) {
    $("#confirmPassword").focus($("#confirmPassword").css("box-shadow", "0 0 0 0.25rem #dc3545"))
    $("#submitButton").disabled = true;
    console.log('Passwords do not match');
  } else {
    $("#confirmPassword").focus(
      $("#confirmPassword").css("box-shadow", "0 0 0 0.25rem #198754")
    );
    $("#submitButton").prop("disabled", false);
  }
})
