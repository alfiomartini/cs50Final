document.addEventListener('DOMContentLoaded', listeners)

function listeners(){

    let input = document.querySelector('input[name="username"]');
    let form = document.querySelector('form');

    input.addEventListener('change', checkUser);
    form.addEventListener('submit', checkPass);

    function checkUser(){
        let container = document.getElementById('modal-div');
        let modal = new Modal('');
        var value = input.value;
        $.get('/check?username='+value, function(data){
            var avail = JSON.parse(data);
            if (!avail) {
                modal.setModal('Name already in use.');
                container.innerHTML = modal.getModal();
                modal.fireModal();
                input.value= '';
                input.focus();
            }   
        });
    }

    function checkPass(event){
        event.preventDefault();
        let container = document.getElementById('modal-div');
        let modal = new Modal('');
        let pass = document.getElementById('pass');
        let conf = document.getElementById('conf');
        if (pass.value !== conf.value){
            modal.setModal("Password and confirmation don't match.");
            container.innerHTML = modal.getModal();
            modal.fireModal();
            pass.value= '';
            conf.value = '';
            pass.focus();
        }
        else form.submit();
    }
}