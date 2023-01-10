const SECONDS_IN_HOUR = 3600;
const SECONDS_IN_MIN = 60;
const SETUP_TIME = 30;
const BEND_TIME = 20;
const ROLL_TIME = 180;


function calculatePressTime(bendInput, rollInput) {
    const bendSeconds = bendInput * BEND_TIME;
    const rollSeconds = rollInput * ROLL_TIME;

    return ((bendSeconds + rollSeconds + SETUP_TIME) / SECONDS_IN_HOUR).toFixed(6);
}

function calculateLaserTime(hoursInput, minuteInput, secondsInput) {

    const hourTime = hoursInput * SECONDS_IN_HOUR;
    const minTime = minuteInput * SECONDS_IN_MIN;
    const totalTime = hourTime + minTime + secondsInput;

    return (totalTime / SECONDS_IN_HOUR).toFixed(6);
}

function getRoutingInput() {

    let bends = parseInt($("#bends").val());
    let rolls = parseInt($("#rolls").val());
    let hours = parseInt($("#hours").val());
    let minutes = parseInt($("#minutes").val());
    let seconds = parseInt($("#seconds").val());

    if (!bends) {
      bends = 0;
    }
    if (!rolls) {
      rolls = 0;
    }
    if (!hours) {
      hours = 0;
    }
    if (!minutes) {
      minutes = 0;
    }
    if (!seconds) {
      seconds = 0;
    }

    if (bends !== 0 || rolls !== 0) {
      let formTime = calculatePressTime(bends, rolls);
      $("#forming-time").text(formTime);
      formTime = calculatePressTime(bends, rolls);
        $("#forming-time").text(formTime);
        
    } else {
      $("#forming-time").text("N/A");
    }

    if (hours !== 0 || minutes !== 0 || seconds !== 0) {
      let laserTime = calculateLaserTime(hours, minutes, seconds);
      $("#laser-time").text(laserTime);
      laserTime = calculateLaserTime(hours, minutes, seconds);
      $("#laser-time").text(laserTime);
    } else {
      $("#laser-time").text("N/A");
    }
}