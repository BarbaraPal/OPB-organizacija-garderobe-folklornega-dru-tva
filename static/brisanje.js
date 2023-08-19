function IzbrisiUpRacun(){
    $(document).ready(function() {
        // Dodajte dogodek na klik gumba
        $("#submitBtn5").on("click", function(e) {
          // Preprečite privzeto dejanje gumba (torej pošiljanje obrazca)
          e.preventDefault();

          // Uporabniku pokažite potrditveno okno
          var confirmed = confirm("Ali ste prepričani, da želite odstraniti uporabniški račun?");
          if (confirmed) {
            // Če uporabnik potrdi, da želi odstraniti račun, nadaljujte s pošiljanjem obrazca
            $("#myForm5").submit();
          }
        });
      });
}