addEventListener('DOMContentLoaded', listeners);

// an attempt to make things as locally as possible.
// I could also pass the three variables below as
// arguments (using currying). I have to take a look
// at this.
function listeners(){
    let input = document.querySelector('#search-input');
    let debounceTimeout = null;
    let readme = document.querySelector('.readme');

    input.addEventListener('keyup', search_get);
    input.addEventListener('change', search_get);
    input.addEventListener('paste', search_get);


    function searchEvents(){
        let input = document.querySelector('input');
        let term = input.value;
        //remove spaces from both sides
        term = term.trim();
        if (term){
            $.ajax({
            url: 'search/' + term,
            method: 'get',
            async: true, // notice this line
            })
            .done(function(data, status, xhr){
                if (readme){
                    readme.innerHTML='';
                    readme.style.padding = '0';
                    readme.style.margin = '0';
                }
                document.querySelector('#search').innerHTML = data;
            })
            .fail(function(xhr, status, error){
                    console.log(error);
            });
        }
        else{
           document.querySelector('#search').innerHTML = ''; 
        }
    }
    
// see: https://medium.com/spritle-software/two-things-you-must-do-when-building-your-own-simple-ajax-search-64992d5c9991
// see: https://levelup.gitconnected.com/debounce-in-javascript-improve-your-applications-performance-5b01855e086
    function search_get(event){
        clearTimeout(debounceTimeout);
        debounceTimeout = setTimeout(searchEvents, 300);
    }

}