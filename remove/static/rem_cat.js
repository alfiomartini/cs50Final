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
        let prompt = new Prompt('');
        prompt.show(`Are you sure you want it removed?`);
        yesBtn = document.getElementById('modal-yes');
        yesBtn.onclick= function(){
            form.submit();
        }
    }
}
