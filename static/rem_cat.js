document.addEventListener('DOMContentLoaded', listeners)

function listeners(){

    let select = document.getElementById('known')
    let form = document.querySelector('#form-cat');

    select.addEventListener('change', changeCat);
    form.addEventListener('submit', checkSubmit);

    function changeCat(){
        var selected = select.value;
        document.getElementById('category').value = selected;
    }

    function checkSubmit(event){
        event.preventDefault();
        let container = document.getElementById('modal-div');
        let modal = new Prompt('');
        modal.setPrompt(`Are you sure you want it removed?`);
        container.innerHTML = modal.getPrompt();
        modal.firePrompt();
        // this is not ideal, but simple. Improve later, when
        // a better idea comes
        yesBtn = document.getElementById('modal-yes');
        yesBtn.onclick= function(){
            form.submit();
        }
    }
}
