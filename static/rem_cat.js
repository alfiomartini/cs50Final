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
        var answer = prompt('Are you sure you want to remove it (yes/no)');
        answer = answer.toLowerCase();
        if (answer == 'yes' || answer == 'y'){
            form.submit();
        }

    }
}
