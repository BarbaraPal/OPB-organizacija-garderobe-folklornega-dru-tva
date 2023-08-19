function KlikSpremembaObrazca(){
    // Ob kliku na gumb "Želim spremeniti mere"
    $("#showFormBtn").click(function() {
      // Skrije prvi obrazec
      $("#card1").hide();
      // Prikaže drugi obrazec
      $("#card2").show();
    });
}

function KlikSpremembaObrazca2(){
  $(document).ready(function() {
    $(".showFormBtn").click(function(event) {
      event.preventDefault();
      var index = $(this).data("index");
      $("#card1_" + index).hide();
      $("#card2_" + index).show();
    });
  });
}

function preveriVnos() {
  $("#vnosi_mer").on("keydown", function (event) {
    // Prebere pritisnjeno tipko
    var pritisnjenaTipka = event.key;

    // Dovoljene so številke in znak '/'
    var dovoljeneTipke = /^[0-9\/]$/;
    // Dovoljeno brisanje
    if (pritisnjenaTipka === "Backspace" || pritisnjenaTipka === "Delete") {
      return;
    }
    // Preveri, ali je pritisnjena tipka dovoljena.
    if (!dovoljeneTipke.test(pritisnjenaTipka)) {
      // Če tipka ni dovoljena, prepreči privzeto obnašanje (vnos neveljavnega znaka).
      event.preventDefault();
    }
  });

}


function showFormSection() {
  const formSelector = document.getElementById("vrsta");
  const selectedOption = formSelector.value;
  // Hide all form sections
  const formSections = document.querySelectorAll("[id^='form']");
  formSections.forEach(section => section.style.display = "none");
  // Show the selected form section if it's one of the clothes options
  if (selectedOption === "zgornji_del" || selectedOption === "spodnji_del" || selectedOption === "enodelni_kos" || selectedOption === "dodatna_oblacila") {
    document.getElementById(`form${selectedOption}`).style.display = "block";
  }
}


function SpreminjanjeOblacilVsiKosi(){
  $(".showFormBtnOmara").click(function() {
    $("#prikazomare").hide();
    $("#formomare").show();
    $("#formomare").on("keydown", function (event) {
    // Preberite pritisnjeno tipko
    var pritisnjenaTipka = event.key;
    
    // Dovoljene so številke in znak '/'
    var dovoljeneTipke = /^[0-9\/]$/;
    // Dovoljeno brisanje
    if (pritisnjenaTipka === "Backspace" || pritisnjenaTipka === "Delete") {
      return;
    }
    // Preverite, ali je pritisnjena tipka dovoljena
    if (!dovoljeneTipke.test(pritisnjenaTipka)) {
      // Če tipka ni dovoljena, preprečimo privzeto obnašanje (vnos neveljavnega znaka)
      event.preventDefault();
    }
    });
  });
  
  $(".showFormBtn").click(function() {
  var index = $(this).data("index");
  $("#card1_" + index).hide();
  $("#card2_" + index).hide();
  $("#card4_" + index).hide();
  $("#card3_" + index).show();
});
var index = $(this).data("index");
$("#card3_" + index).on("keydown", function(event) {
  var pritisnjenaTipka = event.key;

  // Dovoljene so številke in znak '/'
  var dovoljeneTipke = /^[0-9\/]$/;
  // Dovoljeno brisanje
  if (pritisnjenaTipka === "Backspace" || pritisnjenaTipka === "Delete") {
    return;
  }
  // Preverite, ali je pritisnjena tipka dovoljena
  if (!dovoljeneTipke.test(pritisnjenaTipka)) {
    // Če tipka ni dovoljena, preprečimo privzeto obnašanje (vnos neveljavnega znaka)
    event.preventDefault();
  }
});

$("#spremeniopombe").off("keydown"); // Odstrani prejšnji event handler, če obstaja
$("#spremeniopombe").on("keydown", function(event) {
  // Dovolimo vnos vseh tipk
});


$("#spremeniopombe").off("keydown"); // Odstrani prejšnji event handler, če obstaja
$("#spremeniopombe").on("keydown", function(event) {
  // Dovolimo vnos vseh tipk
});

  $(".showFormBtnDodatnaOblacila").click(function() {
    var index = $(this).data("index");
    $("#card9_" + index).hide();
    $("#card7_" + index).show();
    
  });


  $(".showFormBtnSlikaDodatna").click(function() {
    var index = $(this).data("index");
    $("#card9_" + index).hide();
    $("#card8_" + index).show();
    
  });

  $(".showFormBtnSlika").click(function() {
    var index = $(this).data("index");
    $("#card4_" + index).hide();
    $("#card5_" + index).show();
    
  });

}

function KlikSpremembaObrazcaZaKostumskePodobe(){
  $("#gumb_dodaj_obvezni_del, #gumb_dodaj_obvezni_del2").click(function() {
    $("#div_posebnosti").hide();
    $("#form_posebnosti").hide();
    $("#form_cevlji_dodaj").hide();
    $("#div_cevlji_posebnosti").hide();
    $("#form_cevlji").hide();
    $("#div_dodaj_k_obstojeci_moznosti").hide();
    $("#form_dodaj_k_obstojeci_moznosti").hide();
    $("#div_dodaj_moznost").hide();
    $("#form_dodaj_del_moznost").hide();
    $("#div_dodaj").show();
    $("#form_dodaj_del").show();
  });

  $("#gumb_dodaj_moznost, #gumb_dodaj_moznost2").click(function() {
    $("#div_posebnosti").hide();
    $("#form_posebnosti").hide();
    $("#form_cevlji_dodaj").hide();
    $("#div_cevlji_posebnosti").hide();
    $("#form_cevlji").hide();
    $("#div_dodaj").hide();
    $("#form_dodaj_del").hide();
    $("#div_dodaj_k_obstojeci_moznosti").hide();
    $("#form_dodaj_k_obstojeci_moznosti").hide();
    $("#div_dodaj_moznost").show();
    $("#form_dodaj_del_moznost").show();
  });

  $("#gumb_dodaj_k_eni_izmed_moznosti").click(function() {
    $("#div_posebnosti").hide();
    $("#form_posebnosti").hide();
    $("#form_cevlji_dodaj").hide();
    $("#div_cevlji_posebnosti").hide();
    $("#form_cevlji").hide();
    $("#div_dodaj").hide();
    $("#form_dodaj_del").hide();
    $("#div_dodaj_moznost").hide();
    $("#form_dodaj_del_moznost").hide();
    $("#div_dodaj_k_obstojeci_moznosti").show();
    $("#form_dodaj_k_obstojeci_moznosti").show();
  });

  $("#gumb_form_za_cevlje").click(function(){
    $("#div_posebnosti").hide();
    $("#form_posebnosti").hide();
    $("#div_dodaj").hide();
    $("#form_dodaj_del").hide();
    $("#div_dodaj_moznost").hide();
    $("#form_dodaj_del_moznost").hide();
    $("#div_dodaj_k_obstojeci_moznosti").hide();
    $("#form_dodaj_k_obstojeci_moznosti").hide();
    $("#form_cevlji_dodaj").hide();
    $("#div_cevlji_posebnosti").show();
    $("#form_cevlji").show();
  });

  $("#gumb_form_za_cevlje_dodaj").click(function(){
    $("#div_posebnosti").hide();
    $("#form_posebnosti").hide();
    $("#div_dodaj").hide();
    $("#form_dodaj_del").hide();
    $("#div_dodaj_moznost").hide();
    $("#form_dodaj_del_moznost").hide();
    $("#div_dodaj_k_obstojeci_moznosti").hide();
    $("#form_dodaj_k_obstojeci_moznosti").hide();
    $("#form_cevlji").hide();
    $("#div_cevlji_posebnosti").show();
    $("#form_cevlji_dodaj").show();
    
 
  });

  $("#posebnosti_dodaj_gumb").click(function(){
    $("#div_dodaj").hide();
    $("#form_dodaj_del").hide();
    $("#div_dodaj_moznost").hide();
    $("#form_dodaj_del_moznost").hide();
    $("#div_dodaj_k_obstojeci_moznosti").hide();
    $("#form_dodaj_k_obstojeci_moznosti").hide();
    $("#form_cevlji_dodaj").hide();
    $("#div_cevlji_posebnosti").hide();
    $("#form_cevlji").hide();
    $("#div_posebnosti").show();
    $("#form_posebnosti").show();
  });
}


