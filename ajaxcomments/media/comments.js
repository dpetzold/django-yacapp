function trim(s) {
    s = s.replace(/(^\s*)|(\s*$)/gi,"");
    s = s.replace(/[ ]{2,}/gi," ");
    s = s.replace(/\n /,"\n");
    return s;
}

function comment_edit(comment, event) {

  event.preventDefault();

  var comment_id = $(comment).attr('id').replace('edit', 'comment');
  var comment = $('#' + comment_id + ' p');
  $('#comment_id').attr('value', comment_id);
  $('#id_edit').text(trim(comment.text()));
  $('.comment-edit').dialog({width: 640, height: 700});
}

function comment_editsave(event) {

  event.preventDefault();

  var comment_id = $('#comment_id').val();
  var p_id = comment_id.replace('comment', 'p');

  $.post('/comment/edit/', {
    'text': $('#id_edit').val(),
    'comment_id': comment_id,
    'object_pk': object_pk,
    'content_type': content_type,
    'csrfmiddlewaretoken': csrf_token,
  }, function(response) {
    if (response.success) {
      $('#id_edit').val('');
      $('.comment-edit').dialog('close');
      $('#' + p_id).text(response.data.text);
    }
    else {
      $('.error').html('<h3>' + response.error + '</h3>');
    }
  }, "json");
}


function comment_delete(comment, event) {

  event.preventDefault();

  var comment_id = $(comment).attr('id').replace('delete', 'comment');
  var comment = '#' + comment_id;
  $.post('/comment/delete/', {
      'comment_id': comment_id,
      'csrfmiddlewaretoken': csrf_token,
  }, function(response) {
    $(comment).hide('fast');
    container = $('.comments');
    //$('html, body').animate({ scrollTop: container.offset().top }, 200);
  });
}

function comment_reply(comment, event) {

  event.preventDefault();

  var comment_id = $(comment).attr('id').replace('reply', 'comment');
  var comment = $('#' + comment_id + ' p');
  $('#parent_id').attr('value', comment_id);
  $('.comment-text').text(comment.html());
  $("#dialog").dialog({width: 640, height: 800});
}

function comment_postreply(event) {

  event.preventDefault();

  var comment_id = $('#parent_id').attr('value');
  $.post('/comment/post/', {
    'text': $('#id_reply').val(),
    'parent_id': $('#parent_id').val(),
    'object_pk': object_pk,
    'content_type': content_type,
    'csrfmiddlewaretoken': csrf_token,
  }, function(response) {
    if (response.success) {
      $('.comment-reply').dialog('close');
      $('#id_reply').val('');
      $('#' + comment_id).append(response.data.comment)
    }
    else {
      $('.error').html('<h3>' + response.error + '</h3>');
    }
  }, "json");
}

function comment_post(event) {

  event.preventDefault();

  $.post('/comment/post/', {
    'text': $('#id_text').val(),
    'object_pk': object_pk,
    'content_type': content_type,
    'csrfmiddlewaretoken': csrf_token,
  }, function(response) {
    if (response.success) {
      $('.error').val('');
      $('textarea').val('');
      $('#id_title').val('');
      $('.comment-form').hide();
      $('.comments').append(response.data.comment)
    }
    else {
      $('.error').html('<h3>' + response.error + '</h3>');
    }
  }, "json");

}

$(document).ready(function() {

    $('.edit-save').click(function(e) {
        comment_editsave(e);
    });

    $('.post-reply').click(function(e) {
        comment_postreply(e);
    });

    $('.post').click(function(e) {
        comment_post(e);
    });
});
