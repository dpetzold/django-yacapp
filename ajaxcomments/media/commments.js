urls = [];

function hideForm() {
  console.log('hideForm');
  $('textarea').hide();
  $('.post').hide();
  $('.add').text('Add').click(function(e) {
      showForm();
  });
}

function showForm() {
  $('textarea').show();
  $('.post').show();
  // scroll to the bottom
  $("html, body").animate({ scrollTop: $(document).height()-$(window).height() });
  $('.add').text('Hide').click(function(e) {
     hideForm();
  });
}

function editFunc(elem) {
  comment_id = $(elem).attr('id').replace('edit', 'comment');
  comment = $('#' + comment_id + ' p');
  html = comment.html().replace('<br>', '\n', 'g').replace(/^\s+|\s+$/g, '');
  $('.add').hide();
  comment.html(
      '<form id="comment_edit" name="notes" action="#" method="post">' +
      '<textarea>' + html + '</textarea></form>');

  $('#' + comment_id + ' textarea').width(comment.width());
  $('#' + comment_id + ' textarea').height(comment.height() * 3);
  $('html, body').animate({ scrollTop: comment.offset().top }, 200);

  $(elem).unbind();
  $(elem).text('Save').click(function() {

    p_id = $(elem).attr('id').replace('edit', 'p');
    text = $('#' + p_id + ' form textarea').val();
    $.post('/plan/comment/' + token + '/edit/' + comment_id + '/', {
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

function ping() {
    console.log(urls);
    $.post('/plan/ping/' + token + '/', {
      'urls': JSON.stringify(urls),
      'csrfmiddlewaretoken': csrf_token,
    }, function(response) {
       if (response.success) {
         urls = [];      
       }
    }, "json");
}


$(document).ready(function() {
    setInterval(function() { ping() }, 30000); 

    $('a').mouseover(function(e) {
      url = $(this).attr('href');
      if (url == undefined) {
        url = $(this).attr('name');
      }

      obj = {
        'url': url, 
        'action': 'mouseover', 
        'time': new Date().getTime() / 1000
      }
      console.log(obj);
      urls.push(obj)
    });

    $('a').click(function(e) {
      url = $(this).attr('href');
      if (url == undefined) {
        url = $(this).attr('name');
      }

      obj = {
        'url': url, 
        'action': 'click', 
        'time': new Date().getTime() / 1000
      }
      console.log(obj);
      urls.push(obj)
    });


    $('.add').click(function(e) {
      showForm();
    });

    $('.header').click(function(e) {
      $(this).next().toggle();
      
      if ($(this).find('.icon').hasClass('plus')) {
        $(this).find('.icon').removeClass('plus');
        $(this).find('.icon').addClass('minus');
      } else {
        $(this).find('.icon').removeClass('minus');
        $(this).find('.icon').addClass('plus');
      }
    });

    $('.edit').click(function(e) {
      editFunc(this);
    });
 
    $('.delete').click(function(e) {
      var comment_id = $(this).attr('id').replace('delete', 'comment');
      var comment = '#' + comment_id;
      $.get('/plan/comment/' + token + '/delete/' + comment_id + '/', function() {
        $(comment).hide('fast');
        container = $('.comments');
        $('html, body').animate({ scrollTop: container.offset().top }, 200);
      });
    });

    $('.post').click(function(e) {
      $.post('/plan/comment/', {
        'comment': $('textarea').val(),
        'csrfmiddlewaretoken': csrf_token,
      }, function(response) {
        if (response.success) {
          $('textarea').val('');
          hideForm();
          $('.comments').append(response.data.comment)
        }
        else {
          $('.comments').html('<h3>' + response.error + '</h3>'); 
        }
      }, "json");
    });
});
