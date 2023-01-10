// Prevents some pop ins on page load
document.addEventListener('DOMContentLoaded', function () { 
    $("body").removeClass('hidden');
   
    let timer = setTimeout(() => {
    $(".flashes").slideUp();
    }, 2500);
  
})