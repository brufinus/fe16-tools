
$(document).ready(function () {
  function updateInfo() {
    var lostItemSelectedOption = $('#lost_item_dropdown').val();
    var characterSelectedOption = $('#character_dropdown').val();

    $.ajax({
      url: '/tools/get_item_data',
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify({
        lost_item_selected_option: lostItemSelectedOption,
        character_selected_option: characterSelectedOption
      }),
      success: function (response) {
        $('#lost_item_info').empty();
        $('#liked_gift_info').empty();

        $('#lost_item_info').append('Owner: ');
        response.character.forEach(function (character) {
          $('#lost_item_info').append('<b>' + character.character + '</b>');
        });

        var ul = $('<ul></ul>')
        response.gifts.forEach(function (gift) {
          ul.append('<li>' + gift.name + '</li>');
        });
        $('#liked_gift_info').append(ul);
      },
      error: function (error) {
        console.log("Error:", error);
      }
    });
  }

  $('#lost_item_dropdown, #character_dropdown').change(function () {
    updateInfo();
  });

  updateInfo();
});
