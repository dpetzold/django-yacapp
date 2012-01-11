(function() {

    window.comment_edit = function(comment, event) {

      event.preventDefault();

      var comment_id = $(comment).attr('id').replace('edit', 'comment');
      var comment = $('#' + comment_id + ' p');
      $('#comment_id').attr('value', comment_id);
      $('#id_edit').text(comment.text());
      $('.comment-edit').dialog({width: 640, height: 700});
    }

    window.comment_editsave = function(event) {

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

    window.comment_delete = function(comment, event) {

      event.preventDefault();

      var comment_id = $(comment).attr('id').replace('delete', 'comment');
      var comment = '#' + comment_id;
      $.post('/comment/delete/', {
          'comment_id': comment_id,
          'object_pk': object_pk,
          'content_type': content_type,
          'csrfmiddlewaretoken': csrf_token,
      }, function(response) {
        $(comment).hide('fast');
        container = $('.comments');

        if ( response.data.comment_count == 1 ) {
            $('.comment-count').text(response.data.comment_count + ' Comment');
        } else {
            $('.comment-count').text(response.data.comment_count + ' Comments');
        }
      });
    }

    window.comment_reply = function(comment, event) {

      event.preventDefault();

      var comment_id = $(comment).attr('id').replace('reply', 'comment');
      var comment = $('#' + comment_id + ' p');
      $('#parent_id').attr('value', comment_id);
      $('.comment-text').text(comment.html()));

      /* XXX: This is a werid hardcode. That is doesn't quite work but
       * I suppose its close enough. */
      if (comment.height() == 16) {
          $(".comment-reply").dialog({width: 590, height: 730});
      } else {
          $(".comment-reply").dialog({width: 590, height: 790 + comment.height()});
      }
    }

    window.comment_postreply = function(event) {

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
          $('.comment-count').text(response.data.comment_count);
          $('#' + comment_id).append(response.data.comment)
        }
        else {
          $('.error').html('<h3>' + response.error + '</h3>');
        }
      }, "json");
    }

    window.comment_post = function(event) {

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

          if ( response.data.comment_count == 1 ) {
              $('.comment-count').text(response.data.comment_count + ' Comment');
          } else {
              $('.comment-count').text(response.data.comment_count + ' Comments');
          }

          $('.comments').append(response.data.comment)
        }
        else {
          $('.error').html('<h3>' + response.error + '</h3>');
        }
      }, "json");
    }
})();

$(document).ready(function() {

    $('.edit-save').click(function(e) {
        comment_editsave(e);
    });

    $('.post-reply').click(function(e) {
        comment_postreply(e);
    });

    $('.post-button').click(function(e) {
        comment_post(e);
    });
});
