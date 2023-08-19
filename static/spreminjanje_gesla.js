function preveriGesla(){
    // ------------ Preveri ali se gesli ujemata --------------
    $('#pwdId, #cPwdId').on('keyup', function () {
      if ($('#pwdId').val() != '' && $('#cPwdId').val() != '' && $('#pwdId').val() == $('#cPwdId').val() ) {
        $('#cPwdValid').show();
        $('#cPwdInvalid').hide();
        $('#cPwdInvalid').html('Gesli se ujemata.').css('color', 'green');
        $('.myCpwdClass').addClass('is-valid');
        $('.myCpwdClass').removeClass('is-invalid');
        $("#submitBtn").attr("disabled",false);
        $('#submitBtn').addClass('btn-primary').removeClass('btn-primary');
        for (i = 0; i < myInputElements.length; i++) {
          var myElement = document.getElementById(myInputElements[i].id);
          if (myElement.classList.contains('is-invalid')) {
            $("#submitBtn").attr("disabled",true);
            $('#submitBtn').addClass('btn-primary').removeClass('btn-primary');
            break;
          }
        }
      } else {
        $('#cPwdValid').hide();
        $('#cPwdInvalid').show();
        $('#cPwdInvalid').html('Gesli se ne ujemata!').css('color', 'red');
        $('.myCpwdClass').removeClass('is-valid');
        $('.myCpwdClass').addClass('is-invalid');
        $("#submitBtn").attr("disabled",true);
        $('#submitBtn').addClass('btn-primary').removeClass('btn-primary');
      }
    });
    // ----------------- Gumb -----------------
    let currForm1 = document.getElementById('myForm1');
    currForm1.addEventListener('submit', function(event) {
      if (currForm1.checkValidity() === false) {
        event.preventDefault();
        event.stopPropagation();
      }
      else {
        $("#submitBtn").attr("disabled",false);
        $('#submitBtn').addClass('btn-primary').removeClass('btn-primary');
        currForm1.classList.add('was-validated');

      }
    }, false);
    currForm1.querySelectorAll('.form-control').forEach(input => {
      input.addEventListener(('input'), () => {
        if (input.checkValidity()) {
          input.classList.remove('is-invalid');
          input.classList.add('is-valid');
        } else {
          input.classList.remove('is-valid');
          input.classList.add('is-invalid');
        }
        var is_valid = $('.form-control').length === $('.form-control.is-valid').length;
        if (is_valid) {
          $("#submitBtn").attr("disabled",false);
          $('#submitBtn').addClass('btn-primary').removeClass('btn-primary');
        } else {
          $("#submitBtn").attr("disabled",true);
          $('#submitBtn').addClass('btn-primary').removeClass('btn-primary');
        }
      });
    });
  }