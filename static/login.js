<script>
    document.querySelector('form').onsubmit = function(){
        if (!document.querySelector('input[name="username"]').value){
            alert('You must provide a username.');
            return false; // cancels form submission
        }
        if (!document.querySelector('input[name="password"]').value){
            alert('You must provide a password.');
            return false; // cancels form submission
        }
    }
</script>