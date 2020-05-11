function getHTML(html){
    //alert(html);
    var elem = document.querySelector('input[name="title"]');
    var doc = new DOMParser().parseFromString(html, 'text/html');
    var title = doc.querySelector('title').innerHTML;
    elem.value = title;
    elem.focus();
};

 
function checkURL(){
    var url = document.querySelector("input[name='url']")
    var urlStr = url.value;
    try{
        url = new URL(urlStr);
        //alert(url);
    }
    catch(_){
        alert('Invalid url');
        url.value = '';
        url.focus();
        return false;
    }
    if (url.protocol === 'http:' || url.protocol === 'https:')
    {
        return true;
    }
    else return false;
}
    
$(document).ready(function(){ 
    $("select").change(function(){
        var selected = document.getElementById('known').value;
        document.getElementById('category').value = selected;
    });
});