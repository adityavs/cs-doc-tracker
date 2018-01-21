$.fn.editable.defaults.mode = 'inline';

$('.edit-link').each(function() { 
  var id = $(this).attr('id').substring(9);
  $('.' + id).each(function() {
    $(this).editable({type: 'text', pk: id, url: window.location.href + '/edit/' + id});
  });
});
