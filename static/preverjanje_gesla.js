function preveriVeljavnostGesla(){

    $("#novo_spremenjeno_geslo").on("input", function() {
        // Prebere vrednost vnesenega gesla.
        var geslo = $(this).val();
      
        // Preveri, ali je geslo veljavno (npr. dolžina od 8 do 25 znakov, črke, številke, in '_').
        var gesloRegex = /^\w{8,25}$/;
        var isGesloValid = gesloRegex.test(geslo);
      
        // Prikaže ustrezno sporočilo in nastavite barvo ozadja.
        if (isGesloValid) {
          $("#gesloValidFeedback3").text("Geslo je veljavno.");
          $(this).removeClass("is-invalid").addClass("is-valid");
        } else {
          $("#gesloInvalidFeedback3").text("Geslo mora biti dolgo od 8 do 25 znakov, ki so lahko črke, številke ali '_'.");
          $(this).removeClass("is-valid").addClass("is-invalid");
        }
      
        // Preveri veljavnost celotnega obrazca.
        var isFormValid = $("#myForm3")[0].checkValidity();
      
        // Nastavi gumb za oddajo glede na veljavnost obrazca.
        if (isFormValid) {
          $("#submitBtn3").attr("disabled", false);
          $('#submitBtn3').addClass('btn-primary').removeClass('btn-primary');
        } else {
          $("#submitBtn3").attr("disabled", true);
          $('#submitBtn3').addClass('btn-primary').removeClass('btn-primary');
        }
      });
}