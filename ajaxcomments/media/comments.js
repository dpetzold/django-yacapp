function edit(elem) {
  comment_id = $(elem).attr('id').replace('edit', 'comment');
  comment = $('#' + comment_id + ' p');
  html = comment.html().replace('<br>', '\n', 'g').replace(/^\s+|\s+$/g, '');
  $('.add').hide();
  comment.html(
      '<form id="comment_edit" name="notes" action="#" method="post">' +
      '<textarea>' + html + '</textarea></form>');

  $('#' + comment_id + ' textarea').width(comment.width());
  $('#' + comment_id + ' textarea').height(comment.height());
  $('html, body').animate({ scrollTop: comment.offset().top }, 200);

  $(elem).unbind();
  $(elem).text('Save').click(function() {

    p_id = $(elem).attr('id').replace('edit', 'p');
    text = $('#' + p_id + ' form textarea').val();
    $.post('/comment/edit/', {
      'comment_id': comment_id,
      'csrfmiddlewaretoken': csrf_token,
      'text': text,
    }, function(response) {
      if (response.success) {
        $('#' + p_id).html(response.data.text);
        $('html, body').animate({ scrollTop: $('#' + p_id).offset().top }, 200);
        $('.add').show();
        $(elem).unbind();
        $(elem).text('Edit').click(function() {
          editFunc(this);
        });
      }
      else {
        $('#' + comment_id).html('<h3>' + escape(response.error) + '</h3>');
      }
      return false;
    }, "json");
  });
}

function delete_comment(comment) {

  var comment_id = $(comment).attr('id').replace('delete', 'comment');
  var comment = '#' + comment_id;
  $.post('/comment/delete/', {
      'comment_id': comment_id,
      'csrfmiddlewaretoken': csrf_token,
  }, function(response) {
    $(comment).hide('fast');
    container = $('.comments');
    $('html, body').animate({ scrollTop: container.offset().top }, 200);
  });
}

function reply_comment(comment) {

  var comment_id = $(comment).attr('id').replace('reply', 'comment');
  var comment = $('#' + comment_id + ' p');
  $('#parent_id').attr('value', comment_id);
  $('.comment-text').text(comment.html());
  $("#dialog").dialog({width: 640, height: 800});
}

$(document).ready(function() {

    $('.reply-post').click(function(e) {
      var comment_id = $('#parent_id').attr('value');

      $.post('/comment/post/', {
        'text': $('#id_reply').val(),
        'parent_id': $('#parent_id').val(),
        'object_pk': object_pk,
        'content_type': content_type,
        'csrfmiddlewaretoken': csrf_token,
      }, function(response) {
        if (response.success) {
          $("#dialog").dialog('close');
          $('#id_reply').val('');
          $('#' + comment_id).append(response.data.comment)
        }
        else {
          $('.error').html('<h3>' + response.error + '</h3>');
        }
      }, "json");
    });

    $('.post').click(function(e) {
      $.post('/comment/post/', {
        'text': $('#id_text').val(),
        'object_pk': object_pk,
        'content_type': content_type,
        'csrfmiddlewaretoken': csrf_token,
      }, function(response) {
        if (response.success) {
          $('textarea').val('');
          $('#id_title').val('');
          $('.comments').append(response.data.comment)
          $('.comment-form').hide();
          $('.error').val('');
        }
        else {
          $('.error').html('<h3>' + response.error + '</h3>');
        }
      }, "json");
    });
});
