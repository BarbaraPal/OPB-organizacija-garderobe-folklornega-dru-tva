function OznacenKvadratek(){

    $(document).ready(function () {
        $("#inlineFormCustomSelect").change(function () {
          // Preveri ali je izbrano karkoli ustreznega 
          if ($(this).val() !== "Izberi...") {
            // Če je izbrana ustrezna možnost, omogoči klik na gumb
            $("#submitBtn4").attr("disabled", false);
            $('#submitBtn4').addClass('btn-secondary').removeClass('btn-primary');
            $(this).removeClass("is-invalid").addClass("is-valid");
          } else {
            // Če ni izbrana nobena od ustreznih možnosti, onemogoči klik na gumb
            $(this).removeClass("is-valid").addClass("is-invalid");
            $("#submitBtn4").attr("disabled", true);
            $('#submitBtn4').addClass('btn-secondary').removeClass('btn-primary');
            
          }
        });
        if ($("#inlineFormCustomSelect").val() === "Izberi...") {
          $("#submitBtn4").attr("disabled", true);
        } else {
          $("#submitBtn4").attr("disabled", false);
        }        
      });
      
      
}

