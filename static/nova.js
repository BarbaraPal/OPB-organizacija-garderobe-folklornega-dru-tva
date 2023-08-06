function IskanjeImenDelo(seznam_imen_priimkov_in_up_imen){
    // Seznam možnih imen in priimkov
  var imena_priimki_up_imena = seznam_imen_priimkov_in_up_imen;

  $("#imeInput").on("input", function() {
    var vnos = $(this).val();
    var predlogi = [];

    // Filtrirajte imena, ki se ujemajo z vnosom
    for (var i = 0; i < imena_priimki_up_imena.length; i++) {
      if (imena_priimki_up_imena[i].toLowerCase().indexOf(vnos.toLowerCase()) === 0) {
        predlogi.push(imena_priimki_up_imena[i]);
      }
    }

    // Prikazovanje predlogov
    var predlogiElement = $("#predlogi");
    predlogiElement.empty();

    for (var j = 0; j < predlogi.length; j++) {
      var predlogElement = $("<div class='predlog'>" + predlogi[j] + "</div>");
      predlogElement.on("click", function() {
        var fullName = $(this).text();
        var nameParts = fullName.split(" ");
        // Ko uporabnik klikne na predlog, ga vstavimo v input polje
        $("#imeInput").val(fullName);
        // Set the username input to the first letter of name + surname
        var username = nameParts[0][0].toLowerCase() + nameParts[1].toLowerCase();
        $("#uporabniskoImeInput").val(username);
        predlogiElement.empty();
      });
      predlogiElement.append(predlogElement);
    }
  });

  // Skrijte predloge, ko uporabnik klikne drugam na stran
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
      var predlogi = seznam_plesalcev
      
      function preveriVeljavnostPolj(rola) {
        
        var vrstaDela = $("#vrstaDela").val();
        var trajanjeMinut = $("#trajanjeMinut").val().trim();
        var datumIzvajanja = $("#datum_izvajanja").val().trim();
        var vsaPoljaIzpolnjena = true;
        if (rola === "True"){
            var imeInput = $("#imeInput").val().trim();
        }
  
        // Preveri ime, če je rola enaka true in ime pravilno
        if (rola === "True" && (imeInput === "" || predlogi.indexOf(imeInput) === -1)) {
        vsaPoljaIzpolnjena = false;
        }
        
  
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
  
        // Enable/Disable the button based on whether all fields are filled
        var $gumb = $("#gumb");
        if (vsaPoljaIzpolnjena) {
          $gumb.attr("disabled", false);
          $gumb.addClass("btn-primary").removeClass("btn-primary");
        } else {
          $gumb.attr("disabled", true);
          $gumb.addClass("btn-secondary").removeClass("btn-primary");

        }
      }
  
      // Function to check if the date is valid
      function isValidDate(dateString) {
        var regEx = /^\d{4}-\d{2}-\d{2}$/;
        if (!dateString.match(regEx)) return false;  // Invalid format
        var d = new Date(dateString);
        var dNum = d.getTime();
        if (!dNum && dNum !== 0) return false; // NaN value, invalid date
        return d.toISOString().slice(0, 10) === dateString;
      }
  
      // Ob pisanju v poljih obrazca preveri vsako polje, če je vrednost prazna
      $("#imeInput, #vrstaDela, #trajanjeMinut, #datum_izvajanja").on("input change", function () {
        preveriVeljavnostPolj();
      });
  
      // Ob oddaji obrazca preveri, če so vsa polja izpolnjena
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
      var vsaPoljaIzpolnjena = true;

      if (ime === "" || priimek === "") {
        vsaPoljaIzpolnjena = false;
      }
      
      if (spol === "") {
        vsaPoljaIzpolnjena = false;
      }
      if (datumPrikljucitve === "" || !isValidDate2(datumPrikljucitve)) {
        vsaPoljaIzpolnjena = false;
      }

      // Enable/Disable the button based on whether all fields are filled
      var $gumb2 = $("#gumb2");
      if (vsaPoljaIzpolnjena) {
        $gumb2.attr("disabled", false);
        $gumb2.addClass("btn-primary").removeClass("btn-primary");
      } else {
        $gumb2.attr("disabled", true);
        $gumb2.addClass("btn-secondary").removeClass("btn-primary");

      }
    }

    // Function to check if the date is valid
    function isValidDate2(dateString) {
      var regEx = /^\d{4}-\d{2}-\d{2}$/;
      if (!dateString.match(regEx)) return false;  // Invalid format
      var d = new Date(dateString);
      var dNum = d.getTime();
      if (!dNum && dNum !== 0) return false; // NaN value, invalid date
      return d.toISOString().slice(0, 10) === dateString;
    }

    // Ob pisanju v poljih obrazca preveri vsako polje, če je vrednost prazna
    $("#Ime, #Priimek, #Spol, #datetimepicker1").on("input change", function () {
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
      // Preveri vrsto dela
      if (ime === "" || pokrajina === "") {
        vsaPoljaIzpolnjena = false;
      }
      for (let element in seznam_nezazelenih) {
        if (ime == element){
          vsaPoljaIzpolnjena = false;
        }
      }
      
      // Enable/Disable the button based on whether all fields are filled
      var $gumb = $("#" + gumbId);
      if (vsaPoljaIzpolnjena) {
        $gumb.attr("disabled", false);
        $gumb.addClass("btn-primary").removeClass("btn-primary");
      } else {
        $gumb.attr("disabled", true);
        $gumb.addClass("btn-primary").removeClass("btn-primary");
      }
    }

    // Ob pisanju v poljih obrazca preveri vsako polje, če je vrednost prazna
    $("#" + imeId, "#" + pokrajinaId).on("input change", function () {
      preveriVeljavnostPolj(seznam_nezazelenih, imeId, pokrajinaId, gumbId);
    });

    // Ob oddaji obrazca preveri, če so vsa polja izpolnjena
    $("#" + obrazecId).on("submit", function (event) {
      preveriVeljavnostPolj(seznam_nezazelenih, imeId, pokrajinaId, gumbId);
      var $gumb = $("#" + gumbId);
      if (!$gumb.prop("disabled")) {
        return true;
      } else {
        event.preventDefault();
        alert("Prosim izpolnite vsa obvezna polja.");
      }
    });
  });
}










