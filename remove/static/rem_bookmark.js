function remove(anchor){ 
  let prompt = new Prompt('');
  prompt.show(`Are you sure you want it removed?`);
  let yesBtn = document.getElementById('modal-yes');
  console.log(yesBtn);
  yesBtn.onclick= function(){
      post_id = anchor.id;
      $.get('rem_book_id/' + post_id, function(data){
          $("[data-toggle='tooltip']").tooltip('hide');
          // data is the index route: '/'
          window.location.assign(data);
      });
  } 
}