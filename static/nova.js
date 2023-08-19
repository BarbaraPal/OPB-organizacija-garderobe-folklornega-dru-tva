function IskanjeImenDelo(seznam_imen_priimkov_in_up_imen){
    // Seznam možnih imen in priimkov
  var imena_priimki_up_imena = seznam_imen_priimkov_in_up_imen;

  $("#imeInput").on("input", function() {
    var vnos = $(this).val();
    var predlogi = [];

    // Filtrira imena, ki se ujemajo z vnosom
    for (var i = 0; i < imena_priimki_up_imena.length; i++) {
      if (imena_priimki_up_imena[i].toLowerCase().indexOf(vnos.toLowerCase()) === 0) {
        predlogi.push(imena_priimki_up_imena[i]);
      }
    }

    // Prikaže predloge
    var predlogiElement = $("#predlogi");
    predlogiElement.empty();

    for (var j = 0; j < predlogi.length; j++) {
      var predlogElement = $("<div class='predlog'>" + predlogi[j] + "</div>");
      predlogElement.on("click", function() {
        var fullName = $(this).text();
        var nameParts = fullName.split(" ");
        // Ko uporabnik klikne na predlog, ga vstavimo v input polje
        $("#imeInput").val(fullName);
        var username = nameParts[0][0].toLowerCase() + nameParts[1].toLowerCase();
        $("#uporabniskoImeInput").val(username);
        predlogiElement.empty();
      });
      predlogiElement.append(predlogElement);
    }
  });

  // Skrije predloge, ko uporabnik klikne drugam na stran
  $(document).on("click", function(event) {
    var target = $(event.target);
    if (!target.is("#imeInput") && !target.is(".predlog")) {
      $("#predlogi").empty();
    }
  });
}

function IzbiranjeDatuma(){
    $(function() {
        $('#datetimepicker1').datepicker({
            format: 'yyyy-mm-dd',
            autoclose: true,
            endDate: '0d'
        });
    });
}

function DodajanjeDela(seznam_plesalcev, rola){
    $(document).ready(function() {
      var predlogi = seznam_plesalcev;
      var rola = rola;
      function preveriVeljavnostPolj(rola) {
        
        var vrstaDela = $("#vrstaDela").val();
        var trajanjeMinut = $("#trajanjeMinut").val().trim();
        var datumIzvajanja = $("#datum_izvajanja").val().trim();
        var vsaPoljaIzpolnjena = true;
      
        // Preveri vrsto dela
        if (vrstaDela === "") {
          vsaPoljaIzpolnjena = false;
        }
  
        // Preveri trajanje
        if (trajanjeMinut === "") {
          vsaPoljaIzpolnjena = false;
        }
  
        // Preveri datum izvajanja
        if (datumIzvajanja === "" || !isValidDate(datumIzvajanja)) {
          vsaPoljaIzpolnjena = false;
        }
  
        // Gumb za oddajo (omogoči/onemogoči)
        var $gumb = $("#gumb");
        if (vsaPoljaIzpolnjena) {
          $gumb.attr("disabled", false);
          $gumb.addClass("btn-primary").removeClass("btn-primary");
        } else {
          $gumb.attr("disabled", true);
          $gumb.addClass("btn-secondary").removeClass("btn-primary");

        }
      }
  
      // Funkcija, ki preverja če je datum veljaven.
      function isValidDate(dateString) {
        var regEx = /^\d{4}-\d{2}-\d{2}$/;
        if (!dateString.match(regEx)) return false;  
        var d = new Date(dateString);
        var dNum = d.getTime();
        if (!dNum && dNum !== 0) return false; 
        return d.toISOString().slice(0, 10) === dateString;
      }
  
      // Ob pisanju v poljih obrazca preveri vsako polje, če je vrednost prazna.
      $("#imeInput, #vrstaDela, #trajanjeMinut, #datum_izvajanja").on("input change", function () {
        preveriVeljavnostPolj();
      });
  
      // Ob oddaji obrazca preveri, če so vsa polja izpolnjena.
      $("#myForm").on("submit", function (event) {
        preveriVeljavnostPolj();
        if (!$("#gumb").prop("disabled")) {
          return true;
        } else {
          event.preventDefault();
          alert("Prosim izpolnite vsa polja.");
        }
      });

  
    });
}

function DodajanjePlesalca(){
  $(document).ready(function() {    
    function preveriVeljavnostPolj2() {
      var ime = $("#Ime").val().trim();
      var priimek = $("#Priimek").val().trim();
      var spol = $("#Spol").val();
      var datumPrikljucitve = $("#datetimepicker1").val().trim();
      var emso = $("#emsonovega").val().trim();
      var vsaPoljaIzpolnjena = true;

      if (ime === "" || priimek === "") {
        vsaPoljaIzpolnjena = false;
      }
      if (!(/^[a-zA-Z]+$/.test(ime))) {
        vsaPoljaIzpolnjena = false;
      } 
      if (!(/^[a-zA-Z]+$/.test(priimek))) {
        vsaPoljaIzpolnjena = false;
      } 
      if (spol === "") {
        vsaPoljaIzpolnjena = false;
      }
      if (datumPrikljucitve === "" || !isValidDate2(datumPrikljucitve)) {
        vsaPoljaIzpolnjena = false;
      }
      if (!/^[0-9]{13}$/.test(emso)) {
        vsaPoljaIzpolnjena = false;
      }
      
      var $gumb2 = $("#gumb2");
      if (vsaPoljaIzpolnjena) {
        $gumb2.attr("disabled", false);
        $gumb2.addClass("btn-primary").removeClass("btn-primary");
      } else {
        $gumb2.attr("disabled", true);
        $gumb2.addClass("btn-secondary").removeClass("btn-primary");

      }
    }

    function isValidDate2(dateString) {
      var regEx = /^\d{4}-\d{2}-\d{2}$/;
      if (!dateString.match(regEx)) return false;  // Invalid format
      var d = new Date(dateString);
      var dNum = d.getTime();
      if (!dNum && dNum !== 0) return false; // NaN value, invalid date
      return d.toISOString().slice(0, 10) === dateString;
    }

    // Ob pisanju v poljih obrazca preveri vsako polje, če je vrednost prazna
    $("#Ime, #Priimek, #Spol, #datetimepicker1, #emsonovega").on("input change", function () {
      preveriVeljavnostPolj2();
    });

    // Ob oddaji obrazca preveri, če so vsa polja izpolnjena
    $("#obrazecdodajplesalca").on("submit", function (event) {
      preveriVeljavnostPolj2();
      if (!$("#gumb2").prop("disabled")) {
        return true;
      } else {
        event.preventDefault();
        alert("Prosim izpolnite vsa polja.");
      }
    });
    

  });
}

function DodajanjeKosaOblacila(seznam, imeId, pokrajinaId, obrazecId, gumbId) {
  $(document).ready(function() {
    var seznam_nezazelenih = seznam;    
    function preveriVeljavnostPolj(seznam_nezazelenih, imeId, pokrajinaId, gumbId) {
      var ime = $("#" + imeId).val().trim();
      var pokrajina = $("#" + pokrajinaId).val().trim();
      var vsaPoljaIzpolnjena = true;
      if (ime === "" || pokrajina === "") {
        vsaPoljaIzpolnjena = false;
      }
      for (let element in seznam_nezazelenih) {
        if (ime == seznam_nezazelenih[element]){
          vsaPoljaIzpolnjena = false;
        }
      }
      // Gumb za oddajo (omogoči/onemogoči).
      var $gumb = $("#" + gumbId);
      
      if (vsaPoljaIzpolnjena) {
        $gumb.attr("disabled", false);
        $gumb.addClass("btn-primary").removeClass("btn-primary");
      } else {
        $gumb.attr("disabled", true);
        $gumb.addClass("btn-primary").removeClass("btn-primary");
      }
    }

    // Ob pisanju v poljih obrazca preveri vsako polje, če je vrednost prazna.
    $("#" + imeId + ", #" + pokrajinaId).on("input change", function () {
      preveriVeljavnostPolj(seznam_nezazelenih, imeId, pokrajinaId, gumbId);
    });
    

    // Ob oddaji obrazca preveri, če so vsa polja izpolnjena.
    $("#" + obrazecId).on("submit", function (event) {
      preveriVeljavnostPolj(seznam_nezazelenih, imeId, pokrajinaId, gumbId);
      var $gumb = $("#" + gumbId);
      if (!$gumb.prop("disabled")) {
        return true
        
      } else {
        event.preventDefault();
        alert("Prosim izpolnite vsa obvezna polja.");
      }
    });
  });
}

function PrikazovanjeImenaSlike(slikaid, slikalabel){
  $(document).ready(function() {
    $("#" + slikaid).on("change", function() {
        var fileInput = $(this)[0];
        if (fileInput.files && fileInput.files[0]) {
            var selectedFile = fileInput.files[0];
            console.log("Izbrana datoteka:", selectedFile.name);

            // Prikaz imena izbrane datoteke v obrazcu
            $("#" + slikalabel).text("Izbrana datoteka: " + selectedFile.name);
        } else {
            // Če ni izbrana nobena datoteka, ponastavimo prikaz
            $("#" + slikalabel).text("");
        }
    });
});
}

function DodajanjeOpraveKostumskePodobe(){
  $(document).ready(function() {    
    function preveriVeljavnostPolj() {
      var ime = $("#kostumska_podoba").val().trim();
      var oprava = $("#oprava").val().trim();
      var vsaPoljaIzpolnjena = true;

      if (ime === "" || oprava === "") {
        vsaPoljaIzpolnjena = false;
      }
      
      var $gumb = $("#gumb");
      if (vsaPoljaIzpolnjena) {
        $gumb.attr("disabled", false);
        $gumb.addClass("btn-primary").removeClass("btn-primary");
      } else {
        $gumb.attr("disabled", true);
        $gumb.addClass("btn-secondary").removeClass("btn-primary");

      }
    }

    // Ob pisanju v poljih obrazca preveri vsako polje, če je vrednost prazna
    $("#kostumska_podoba, #oprava").on("input change", function () {
      preveriVeljavnostPolj();
    });

    // Ob oddaji obrazca preveri, če so vsa polja izpolnjena
    $("#obrazec_oprava_kostumske_podobe").on("submit", function (event) {
      preveriVeljavnostPolj();
      if (!$("#gumb").prop("disabled")) {
        return true;
      } else {
        event.preventDefault();
        alert("Prosim izpolnite vsa polja.");
      }
    });
  });
}

function DodajanjeObveznegaDela(){
  $(document).ready(function() {    
    function preveriVeljavnostPolj() {
      var ime = $("#form_dodaj_obvezni_del_ime_kosa").val().trim();
      var oprava = $("#form_dodaj_obvezni_del_pokrajina").val().trim();
      var vsaPoljaIzpolnjena = true;

      if (ime === "" || oprava === "") {
        vsaPoljaIzpolnjena = false;
      }
      
      var $gumb = $("#form_dodaj_obvezni_del_gumb_dodaj");
      if (vsaPoljaIzpolnjena) {
        $gumb.attr("disabled", false);
        $gumb.addClass("btn-primary").removeClass("btn-primary");
      } else {
        $gumb.attr("disabled", true);
        $gumb.addClass("btn-secondary").removeClass("btn-primary");

      }
    }

    // Ob pisanju v poljih obrazca preveri vsako polje, če je vrednost prazna
    $("#form_dodaj_obvezni_del_ime_kosa, #form_dodaj_obvezni_del_pokrajina").on("input change", function () {
      preveriVeljavnostPolj();
    });

    // Ob oddaji obrazca preveri, če so vsa polja izpolnjena
    $("#form_dodaj_obvezni_del").on("submit", function (event) {
      preveriVeljavnostPolj();
      if (!$("#form_dodaj_obvezni_del_gumb_dodaj").prop("disabled")) {
        return true;
      } else {
        event.preventDefault();
        alert("Prosim izpolnite vsa polja.");
      }
    });
    

  });
}

function DodajanjeMoznosti(){
  $(document).ready(function() {    
    function preveriVeljavnostPolj() {
      var ime = $("#form_dodaj_ime_kosa_moznost").val().trim();
      var oprava = $("#form_dodaj_pokrajina_moznost").val().trim();
      var vsaPoljaIzpolnjena = true;

      if (ime === "" || oprava === "") {
        vsaPoljaIzpolnjena = false;
      }
      
      var $gumb = $("#gumb_dodaj_del_moznost");
      if (vsaPoljaIzpolnjena) {
        $gumb.attr("disabled", false);
        $gumb.addClass("btn-primary").removeClass("btn-primary");
      } else {
        $gumb.attr("disabled", true);
        $gumb.addClass("btn-secondary").removeClass("btn-primary");

      }
    }

    // Ob pisanju v poljih obrazca preveri vsako polje, če je vrednost prazna
    $("#form_dodaj_ime_kosa_moznost, #form_dodaj_pokrajina_moznost").on("input change", function () {
      preveriVeljavnostPolj();
    });

    // Ob oddaji obrazca preveri, če so vsa polja izpolnjena
    $("#form_dodaj_del_moznost").on("submit", function (event) {
      preveriVeljavnostPolj();
      if (!$("#gumb_dodaj_del_moznost").prop("disabled")) {
        return true;
      } else {
        event.preventDefault();
        alert("Prosim izpolnite vsa polja.");
      }
    });
    

  });
}

function DodajanjeKEniIzmedMoznosti(){
  $(document).ready(function() {    
    function preveriVeljavnostPolj() {
      var ime = $("#form_dodaj_k_obstojeci_moznosti_ime_kosa").val().trim();
      var oprava = $("#form_dodaj_k_obstojeci_moznosti_pokrajina").val().trim();
      var vsaPoljaIzpolnjena = true;

      if (ime === "" || oprava === "") {
        vsaPoljaIzpolnjena = false;
      }
      
      var $gumb = $("#form_dodaj_k_obstojeci_moznosti_gumb_dodaj");
      if (vsaPoljaIzpolnjena) {
        $gumb.attr("disabled", false);
        $gumb.addClass("btn-primary").removeClass("btn-primary");
      } else {
        $gumb.attr("disabled", true);
        $gumb.addClass("btn-secondary").removeClass("btn-primary");

      }
    }

    // Ob pisanju v poljih obrazca preveri vsako polje, če je vrednost prazna
    $("#form_dodaj_k_obstojeci_moznosti_ime_kosa, #form_dodaj_k_obstojeci_moznosti_pokrajina").on("input change", function () {
      preveriVeljavnostPolj();
    });

    // Ob oddaji obrazca preveri, če so vsa polja izpolnjena
    $("#form_dodaj_k_obstojeci_moznosti").on("submit", function (event) {
      preveriVeljavnostPolj();
      if (!$("#form_dodaj_k_obstojeci_moznosti_gumb_dodaj").prop("disabled")) {
        return true;
      } else {
        event.preventDefault();
        alert("Prosim izpolnite vsa polja.");
      }
    });
    

  });
}

function DodajanjeTipaCevljev(){
  $(document).ready(function() {    
    function preveriVeljavnostPolj() {
      var ime = $("#tip_cevljev_dodaj").val().trim();
      var vsaPoljaIzpolnjena = true;

      if (ime === "") {
        vsaPoljaIzpolnjena = false;
      }
      
      var $gumb = $("#tip_cevljev_dodaj_gumb");
      if (vsaPoljaIzpolnjena) {
        $gumb.attr("disabled", false);
        $gumb.addClass("btn-primary").removeClass("btn-primary");
      } else {
        $gumb.attr("disabled", true);
        $gumb.addClass("btn-secondary").removeClass("btn-primary");

      }
    }

    // Ob pisanju v poljih obrazca preveri vsako polje, če je vrednost prazna
    $("#tip_cevljev_dodaj").on("input change", function () {
      preveriVeljavnostPolj();
    });

    // Ob oddaji obrazca preveri, če so vsa polja izpolnjena
    $("#form_cevlji_dodaj").on("submit", function (event) {
      preveriVeljavnostPolj();
      if (!$("#tip_cevljev_dodaj_gumb").prop("disabled")) {
        return true;
      } else {
        event.preventDefault();
        alert("Prosim izpolnite vsa polja.");
      }
    });
    

  });
}

function DodajanjePosebnosti(){
  $(document).ready(function() {    
    function preveriVeljavnostPolj() {
      var ime = $("#exampleFormControlTextarea1").val().trim();
      var vsaPoljaIzpolnjena = true;

      if (ime === "") {
        vsaPoljaIzpolnjena = false;
      }
      
      var $gumb = $("#gumb_posebnost_dodaj");
      if (vsaPoljaIzpolnjena) {
        $gumb.attr("disabled", false);
        $gumb.addClass("btn-primary").removeClass("btn-primary");
      } else {
        $gumb.attr("disabled", true);
        $gumb.addClass("btn-secondary").removeClass("btn-primary");

      }
    }

    // Ob pisanju v poljih obrazca preveri vsako polje, če je vrednost prazna
    $("#exampleFormControlTextarea1").on("input change", function () {
      preveriVeljavnostPolj();
    });
    

  });
}
