
// $('cssselector').event, function(){
//     $('cssselector').effect()
// }

// -=[ Cross out Event Expired ]=-
$('ul').on('click','li',function(){
  $('li').toggleClass('completed');
});

// -=[ Remove Event ]=-
$('ul').on('click','span',function(event){
  $(this).parent().fadeOut(1000,function(){
    $(this).remove();
  });
  event.stopPropagation();
});


// -=[ Add Event ]=-
$('input[type="text"]').on('keypress',function(event){
    // Event 13 is return on the ASCII code
  	if(event.which == 13){
      // .val() Set the value of the <input> field
      var input = $(this).val();
      // .append('selector') Insert content at the end of the selector
      $('ul').append('<li><span><i class="fa fa-trash"></i></span> '+input+'</li>')
      $(this).val('');
    }
});

$('.fa-plus').click(function(){
  $('input').fadeToggle(1000);
});