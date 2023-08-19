function preveriUpImeInGeslo(seznam_imen){
// Definira seznam že obstoječih uporabniških imen
var trenutnaUpImena = seznam_imen; // Prilagodite seznam vašim potrebam
  
// Doda dogodek input na polje za uporabniško ime
$("#uporabnisko_ime_uporabnik").on("input", function() {
  // Prebere vrednost vnesenega uporabniškega imena
  var uporabniskoIme = $(this).val();
  if (uporabniskoIme.trim() === "") {
    // Če je uporabniško ime prazno, onemogoči gumb za oddajo obrazca
    $("#rezultat_preverjanja").text("Uporabniško ime ne more biti prazno.");
    $(this).removeClass("is-valid").addClass("is-invalid");
    $("#submitBtn").attr("disabled", true);
    $('#submitBtn').addClass('btn-secondary').removeClass('btn-primary');
    return; // Izstopi iz funkcije, saj ni potrebe po nadaljnjem preverjanju.
  }
  // Preveri, ali vneseno uporabniško ime obstaja v seznamu trenutnih uporabniških imen.
  var exists = trenutnaUpImena.includes(uporabniskoIme);

  // Prikaže ustrezno sporočilo in nastavi barvo ozadja.
  if (exists) {
    $("#rezultat_preverjanja").text("Uporabniško ime že obstaja.");
    $(this).removeClass("is-valid").addClass("is-invalid");
    $("#submitBtn").attr("disabled", true);
    $('#submitBtn').addClass('btn-secondary').removeClass('btn-primary');
  } else {
    $("#rezultat_preverjanja2").text("Uporabniško ime je na voljo.");
    $(this).removeClass("is-invalid").addClass("is-valid");

    // Preveri veljavnost celotnega obrazca.
    var isFormValid = $("#myForm1")[0].checkValidity();

    // Nastavi gumb za pošiljanje glede na veljavnost obrazca.
    if (isFormValid) {
      $("#submitBtn").attr("disabled", false);
      $('#submitBtn').addClass('btn-secondary').removeClass('btn-primary');
    } else {
      $("#submitBtn").attr("disabled", true);
      $('#submitBtn').addClass('btn-secondary').removeClass('btn-primary');
    }
  }
});

$("#geslo_uporabnik").on("input", function() {
  // Prebere vrednost vnesenega gesla.
  var geslo = $(this).val();

  // Preveri, ali je geslo veljavno (npr. dolžina od 8 do 25 znakov, črke, številke, in '_').
  var gesloRegex = /^\w{8,25}$/;
  var isGesloValid = gesloRegex.test(geslo);

  // Prikaže ustrezno sporočilo in nastavi barvo ozadja.
  if (isGesloValid) {
    $("#gesloValidFeedback").text("Geslo je veljavno.");
    $(this).removeClass("is-invalid").addClass("is-valid");
  } else {
    $("#gesloInvalidFeedback").text("Geslo mora biti dolgo od 8 do 25 znakov, ki so lahko črke, številke ali '_'.");
    $(this).removeClass("is-valid").addClass("is-invalid");
  }

  // Preveri veljavnost celotnega obrazca.
  var isFormValid = $("#myForm1")[0].checkValidity();

  // Nastavi gumb za pošiljanje glede na veljavnost obrazca.
  if (isFormValid) {
    $("#submitBtn").attr("disabled", false);
    $('#submitBtn').addClass('btn-secondary').removeClass('btn-primary');
  } else {
    $("#submitBtn").attr("disabled", true);
    $('#submitBtn').addClass('btn-secondary').removeClass('btn-primary');
  }
});



$("#myForm1").submit(function(event) {
    // Preveri, ali sta uporabniško ime in geslo veljavna.
    var isUpImeValid = $("#uporabnisko_ime_uporabnik")[0].checkValidity();
    var isGesloValid = $("#geslo_uporabnik")[0].checkValidity();

    // Če sta oba pogoja izpolnjena, omogoči oddajo obrazca.
    if (isUpImeValid && isGesloValid) {
        $("#submitBtn").attr("disabled", false);
        $('#submitBtn').addClass('btn-secondary').removeClass('btn-primary');
    } else {
      // Sicer prepreči oddajo obrazca in izpiše sporočilo.
      event.preventDefault();
      alert("Prosimo, da vnesete veljavno uporabniško ime in geslo.");
      
    }
  });


}
