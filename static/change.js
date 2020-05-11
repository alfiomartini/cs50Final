$('#change').hide();
var HIDDEN = true;
var button = document.getElementById('btn-chg');
button.onclick = function(){
    if (HIDDEN) {
        $('#change').show();
        HIDDEN = false;
    }
    else {
        $('#change').hide();
        HIDDEN = true;
    }
};
function checkPass(){
    var form = document.querySelector('form');
    var newpass = document.getElementById('new');
    var confpass = document.getElementById('conf');
    if (newpass.value !== confpass.value){
        alert("New password and confirmation don't match");
        newpass.value= '';
        confpass.value = '';
        newpass.focus();
    }
    else form.submit();
};