addEventListener('DOMContentLoaded', menuItems);

function menuItems(){
  let menuItems = document.querySelectorAll('.status');
  // console.log(menuItems);
  for (let k = 0; k < menuItems.length; k++){
    let str = menuItems[k].innerHTML;
    if (str.search(/On/i) > -1){
      menuItems[k].style.color = 'lightsteelblue';
    }
  }
}