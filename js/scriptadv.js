// -=[ Cross out Event Expired ]=-
$('ul').on('click','li',function(){
  $(this).toggleClass('completed');
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
    // Event 13 is 'return' on the ASCII code
  	if(event.which == 13){
      // .val() Set the value of the <input> field
      var input = $(this).val();
      // .append('selector') Insert content at the end of the selector
      // this instead of UL for parent (isolated) element adjustment - Get the immediately following sibling of each element in the set of matched elements. If a selector is provided, it retrieves the next sibling only if it matches that selector.
      $(this).next().append('<li><span><i class="fa fa-trash"></i></span> '+input+'</li>');
      $(this).val('');
    }
});

$('.fa-plus').click(function(){
  $('input').fadeToggle(1000);

});


