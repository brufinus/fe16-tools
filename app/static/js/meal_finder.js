$(document).ready(function () {
  function updateInfo() {
    var selectedOption1 = $('#dropdown1').val();
    var selectedOption2 = $('#dropdown2').val();

    $.ajax({
      url: '/tools/get_meal_data',
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify({
        selected_option1: selectedOption1,
        selected_option2: selectedOption2
      }),
      success: function (response) {
        var mealsCount = response.meals_count;
        var numChars = response.num_chars;
        var prefixMessage = '';

        $('#info').empty();

        if (mealsCount > 1 && numChars > 1) {
          prefixMessage = 'Like these meals:';
        }
        else if (mealsCount > 1 && numChars == 1) {
          prefixMessage = 'Likes these meals:';
        }
        else if (mealsCount === 1) {
          prefixMessage = 'Like this meal:';
        }
        else if (mealsCount === 0) {
          prefixMessage = "Share no liked meals.";
        }

        $('#info').append('<p><b>' + prefixMessage + '</b></p>');
        var ul = $('<ul></ul>');
        response.meals.forEach(function (meal) {
          ul.append('<li>' + meal.meal + '</li>');
        });
        $('#info').append(ul);
      },
      error: function (error) {
        console.log("Error:", error);
      }
    });
  }

  $('#dropdown1, #dropdown2').change(function () {
    updateInfo();
  });

  updateInfo();
});
