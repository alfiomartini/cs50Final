// I could use delegation, as far as I understood.
// But this way is simpler (to understand)
// see: https://javascript.info/event-delegationS
function edit(anchor){
  //console.log('Post id:' + anchor.id + '\n' 
      // + 'Type of id: ' + typeof anchor.id);
  post_id = anchor.id;
  // transfer to url
  // Is there a bettwer way to do it?
  window.location.assign('edit_id/' + post_id);
};