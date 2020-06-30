function remove(anchor){ 
  let container = document.getElementById('modal-div');
  let modal = new Prompt('');
  modal.setPrompt(`Are you sure you want it removed?`);
  container.innerHTML = modal.getPrompt();
  modal.firePrompt();
  // this is not ideal, but simple. Improve later, when
  // a better idea comes
  yesBtn = document.getElementById('modal-yes');
  yesBtn.onclick= function(){
      post_id = anchor.id;
      $.get('rem_book_id/' + post_id, function(data){
          $("[data-toggle='tooltip']").tooltip('hide');
          // data is the index route: '/'
          window.location.assign(data);
      });
  } 
}