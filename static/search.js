function searchEvents(){
    //alert('hello');
    let input = document.getElementById('search-input');
    let term = input.value;
    //remove spaces from both sides
    term = term.trim();
    if (term){
        //alert(term);
        $.ajax({
        url: 'search/' + term,
        method: 'get',
        async: true, // notice this line
        })
        .done(function(data, status, xhr){
            document.querySelector('#search').innerHTML = data;
            request = null;
        })
        .fail(function(xhr, status, error){
                console.log(error);
                request = null;
        });
    }
    else{
       document.querySelector('#search').innerHTML = ''; 
       //$("#search").html('');
    }
   
}
// see: https://medium.com/spritle-software/two-things-you-must-do-when-building-your-own-simple-ajax-search-64992d5c9991
// see: https://levelup.gitconnected.com/debounce-in-javascript-improve-your-applications-performance-5b01855e086
/* 
 The debounce function delays the processing of the keyup event until the user has 
 stopped typing for a predetermined amount of time. This prevents your UI code from 
 needing to process every event and also drastically reduces the number of API calls 
 sent to your server.
*/
$(document).ready(function(){
    var debounceTimeout = null;
    $('#search-input').on('change keyup', function(event){
        clearTimeout(debounceTimeout);
        debounceTimeout = setTimeout(searchEvents, 300);
    });
});