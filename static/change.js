document.addEventListener('DOMContentLoaded', listeners);

function listeners(){
    let button = document.getElementById('btn-chg');
    let form = document.getElementById('change');
    let toggleForm = new HideForm();

    button.addEventListener('click', formToggle);
    form.addEventListener('submit', checkPass);

    function formToggle(){
        if (toggleForm.getHidden()){
            if (form.getAttribute('hidden') !== null)
                form.removeAttribute('hidden');
            $('#change').show();
            toggleForm.setHidden(false);
        }
        else{
            $('#change').hide();
            toggleForm.setHidden(true); 
        }
    }

    function checkPass(event){
        event.preventDefault();
        let container = document.getElementById('modal-div');
        let modal = new Modal('');
        var newpass = document.getElementById('new');
        var confpass = document.getElementById('conf');
        if (newpass.value !== confpass.value){
            modal.setModal("Password and confirmation don't match.");
            container.innerHTML = modal.getModal();
            modal.fireModal();
            newpass.value= '';
            confpass.value = '';
            newpass.focus();
        }
        else form.submit();
        }
}

 