document.addEventListener('DOMContentLoaded', listeners)

function listeners(){
    let inputURL =  document.querySelector("input[name='url']");
    let select = document.querySelector('select');
    let catched = false;
    let form = document.getElementById('form-create');

    // inputURL.addEventListener('paste', checkTimeout);
    // inputURL.addEventListener('change', checkURL);
    // $("input[name='url']").on('paste change', checkTimeout);
    form.addEventListener('submit', checkURL)
    select.addEventListener('change',selectCat);

    function checkTimeout(){
        // this is a hack, but a good one
        // see: https://stackoverflow.com/questions/9857801/how-to-get-the-new-value-of-a-textarea-input-field-on-paste
        setTimeout(checkURL, 100);
    }
    /*
        - The value returned by an event handler is usually ignored.
        - The only exception is return false from a handler assigned using 
        on<event>.
        - In all other cases, return value is ignored. In particular, 
        there’s no sense in returning true.
    */
   function checkURL(event){
    event.preventDefault();
    let modal = new Modal('');
    let urlStr = inputURL.value;
    //console.log('url value', urlStr);
    try{
        url = new URL(urlStr);
    }
    catch(_){
        modal.show(`Invalid url: ${urlStr}`);
        // inputURL.value = '';
        // inputURL.focus();
        return;
    }
    if (!(url.protocol === 'http:' || url.protocol === 'https:')){
        modal.show(`URL protocol must be http: or https: instead of ${url.protocol}`);
        // inputURL.value = '';
        // inputURL.focus();
    }
    else form.submit()
}

    function selectCat(){
        let selected = document.getElementById('known').value;
        document.getElementById('category').value = selected;
    }
}