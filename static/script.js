
function addLoader(){
  document.getElementById("overlay").style.display = "block";
}

function getStatistics(filename){
    $.get( "/statistic/" + filename, function( data ) {
        if(!data['error']){
          document.getElementById('validNumber').innerHTML = data['validNumber'];
          document.getElementById('discardNumber').innerHTML = data['discardNumber'];
        }
    });
}

function validateForm(){
  let form = document.forms["save"],
      phonePrefix = form["phonePrefix"].value.split(","),
      error = false;

  if(phonePrefix[phonePrefix.length - 1] === ""
    || phonePrefix[phonePrefix.length - 1] === " "){
    document.getElementsByName('phonePrefix')[0].style.borderColor = "red";
    error = true;
  }else{
    document.getElementsByName('phonePrefix')[0].style.borderColor = "#ced4da";
  }

  if($(form['createDiscardSheet']).val() === "on" && form["discardName"].value === ""){
    document.getElementsByName('discardName')[0].style.borderColor = "red";
    error = true;
  }else{
    document.getElementsByName('discardName')[0].style.borderColor = "#ced4da";
  }

  return !error;
}
