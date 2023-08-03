function KlikSpremembaObrazca(){
    // Ob kliku na gumb "Želim spremeniti mere"
    $("#showFormBtn").click(function() {
      // Skrijemo prvi obrazec
      $("#card1").hide();
      // Prikažemo drugi obrazec
      $("#card2").show();
    });
}

function preveriVnos() {
  $("#vnosi_mer").on("keydown", function (event) {
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

}


