function OznacenKvadratek(){

    $(document).ready(function () {
        // Attach a change event listener to the dropdown menu
        $("#inlineFormCustomSelect").change(function () {
          // Check if a valid option is selected (not the default "Izberi...")
          if ($(this).val() !== "") {
            // If a valid option is selected, enable the submit button
            $("#submitBtn4").attr("disabled", false);
            $('#submitBtn4').addClass('btn-secondary').removeClass('btn-primary');
            $(this).removeClass("is-invalid").addClass("is-valid");
          } else {
            // If no valid option is selected, disable the submit button
            $("#submitBtn4").attr("disabled", true);
            $('#submitBtn4').addClass('btn-secondary').removeClass('btn-primary');
            $(this).removeClass("is-valid").addClass("is-invalid");
          }
        });
      });
      
      
}