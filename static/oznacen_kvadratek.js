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

function FiltriranjeGledeNaSpol(){
  var izberiSpolSelect = document.getElementById("izberi_spol");
    var plesalciCheckbox = document.querySelectorAll(".plesalec-checkbox");

    izberiSpolSelect.addEventListener("change", function() {
        var izbranaVrednost = izberiSpolSelect.value;

        plesalciCheckbox.forEach(function(checkbox) {
            var spolPlesalca = checkbox.querySelector(".form-check-label").textContent.split("(")[1].split(")")[0];

            if (izbranaVrednost === "Vsi" || izbranaVrednost === spolPlesalca) {
                checkbox.style.display = "block";
            } else {
                checkbox.style.display = "none";
            }
        });
    });
}
function IzbraniVsiPodatki(){
  var izberiSpolSelect = document.getElementById("izberi_spol");
  var izberiTipSelect = document.getElementById("izberi_tip");
  var plesalciCheckboxes = document.querySelectorAll(".plesalec-checkbox");
  var potrdiGumb = document.getElementById("gumb");

  // Funkcija za preverjanje, ali je gumb lahko kliknjen
  function preveriGumb() {
      var izbranSpol = izberiSpolSelect.value;
      var izbranTip = izberiTipSelect.value;
      var vsajEnPlesalecIzbran = [...plesalciCheckboxes].some(function(checkbox) {
          return checkbox.querySelector("input").checked;
      });

      if (izbranSpol !== "Izberi..." && izbranTip !== "Izberi..." && vsajEnPlesalecIzbran) {
          potrdiGumb.disabled = false;
      } else {
          potrdiGumb.disabled = true;
      }
  }

  // Poslušaj spremembe v izbirnih poljih in checkboxih
  izberiSpolSelect.addEventListener("change", preveriGumb);
  izberiTipSelect.addEventListener("change", preveriGumb);
  plesalciCheckboxes.forEach(function(checkbox) {
      checkbox.querySelector("input").addEventListener("change", preveriGumb);
  });
}

function OznacenVsajEnKvadratek(){
  var checkboxi = document.querySelectorAll(".custom-control-input");
  var potrdiGumb = document.getElementById("gumb");
  
  checkboxi.forEach(function(checkbox) {
      checkbox.addEventListener("change", function() {
          var vsajEnOznačen = false;
          checkboxi.forEach(function(checkbox) {
              if (checkbox.checked) {
                  vsajEnOznačen = true;
              }
          });
          if (vsajEnOznačen) {
              potrdiGumb.removeAttribute("disabled");
          } else {
              potrdiGumb.setAttribute("disabled", "disabled");
          }
      });
  });
}