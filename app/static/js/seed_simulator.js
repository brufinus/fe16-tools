$(document).ready(function () {
  function updateInfo() {
    var seed1SelectedOption = $('#seed1_dropdown').val();
    var seed2SelectedOption = $('#seed2_dropdown').val();
    var seed3SelectedOption = $('#seed3_dropdown').val();
    var seed4SelectedOption = $('#seed4_dropdown').val();
    var seed5SelectedOption = $('#seed5_dropdown').val();
    var cultivationSelectedOption = $('#cultivation_dropdown').val();

    $.ajax({
      url: '/tools/get_seed_data',
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify({
        seed1_selected_option: seed1SelectedOption,
        seed2_selected_option: seed2SelectedOption,
        seed3_selected_option: seed3SelectedOption,
        seed4_selected_option: seed4SelectedOption,
        seed5_selected_option: seed5SelectedOption,
        cultivation_selected_option: cultivationSelectedOption
      }),
      success: function (response) {
        $('#info').empty();

        $('#info').append('<b>Score</b>: ')
        $('#info').append(response.score)

        $('#info').append('<br><b>Yield</b>: ')
        $('#info').append(response.yield)

        $('#info').append('<br><b>Low-high ratio</b>: ')
        $('#info').append(response.ratio)

        $('#info').append('<br><b>Coefficient</b>: ')
        $('#info').append(response.coefficient)
      },
      error: function (error) {
        console.log("Error:", error);
      }
    });
  }

  $('#seed1_dropdown, #seed2_dropdown, #seed3_dropdown, #seed4_dropdown, #seed5_dropdown, #cultivation_dropdown').change(function () {
    updateInfo();
  });

  updateInfo();
});
