$('.card').each(function(i){
  setTimeout(function(){
    $('.card').eq(i).addClass('is-visible');
  }, 100 * i);
});
