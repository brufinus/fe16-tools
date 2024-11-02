
$(document).ready(function () {
  $('#search-bar').on('keypress', function (event) {
    if (event.which === 13) {
      event.preventDefault();
      $('#search-bar').val('');
      $('#info').empty();
    }
  });

  $('#search-bar').on('input', function () {
    const query = $(this).val();
    if (query.length > 0) {
      $.ajax({
        url: '/tools/get_lecture_data',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ q: query }),
        success: function (response) {
          const results = response.data;

          $('#info').empty();

          if (results.length > 0) {
            results.forEach(result => {
              $('#info').append('<p>' + result.question + '<ul><li style="color:DodgerBlue;">' + result.answer + '</li></ul></p>');
            });
          }
          else {
            $('#info').append('<p>No results</p>');
          }
        }
      });
    }
    else {
      $('#info').empty();
    }
  });
});
