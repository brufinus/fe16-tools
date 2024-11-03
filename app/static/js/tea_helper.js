$(document).ready(function () {
  function updateInfo() {
    var selectedOption = $('#dropdown').val();

    $.ajax({
      url: '/tools/get_tea_data',
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify({
        selected_option: selectedOption
      }),
      success: function (response) {
        var teaCount = response.tea_count;
        var prefixMessage = '';

        $('#tea_info').empty();
        $('#topic_info').empty();
        $('#final_topic_info').empty();

        if (teaCount > 1) {
          prefixMessage = 'Favorite teas:';
        }
        else {
          prefixMessage = 'Favorite tea:';
        }

        $('#tea_info').append('<p><b>' + prefixMessage + '</b></p>');
        var ul = $('<ul></ul>')
        response.tea.forEach(function (tea) {
          ul.append('<li>' + tea.tea + '</li>');
        });
        $('#tea_info').append(ul);

        response.topics.forEach(function (topics) {
          $('#topic_info').append('<div class="topic-item">' + topics.topic + '</div>');
        });

        var gridContainer = $('<div>').addClass('comment-grid-container');
        response.comments.forEach(function (c, index) {
          var a = response.answers[index];
          var commentDiv = $('<div>').addClass('comment-item').text(c.comment);
          var answerDiv = $('<div>').addClass('answer-item').text(a.answer);
          gridContainer.append(commentDiv);
          gridContainer.append(answerDiv);
        });
        $('#final_topic_info').append(gridContainer);
      },
      error: function (error) {
        console.log("Error:", error);
      }
    });
  }

  $('#dropdown').change(function () {
    updateInfo();
  });

  updateInfo();
});
