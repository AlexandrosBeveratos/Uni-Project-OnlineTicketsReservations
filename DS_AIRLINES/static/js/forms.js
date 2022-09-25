$("form[name=signup_form").submit(function(e) {
    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
      url: "/user/register",
      type: "POST",
      data: data,
      dataType: "json",
      success: function(resp) {
        window.location.href = "/dash/";
      },
      error: function(resp) {
        console.log(resp);
        $error.text(resp.responseJSON.error).removeClass("error--hidden");
        setTimeout(() => {
          $error.addClass("error--hidden");
        }, 3000);
      }
    });
    e.preventDefault();
  });

  $("form[name=login_form").submit(function(e) {
  var $form = $(this);
  var $error = $form.find(".error");
  var $info = $form.find(".info");
  var data = $form.serialize();

  $.ajax({
    url: "/user/signin",
    type: "POST",
    data: data,
    dataType: "json",
    success: function(resp) {
      window.location.href = "/dash/";
    },
    error: function(resp) {
      $error.text(resp.responseJSON.error).removeClass("error--hidden");
      if(resp.responseJSON.error == "Account Disabled"){
        $info.removeClass("info--hidden")
      }
      setTimeout(() => {
        $error.addClass("error--hidden");
      }, 3000);
    }
  });
  e.preventDefault();
});

$("form[name=add_flight_form").submit(function(e) {
  var $form = $(this);
  var $error = $form.find(".error");
  var data = $form.serialize();

  $.ajax({
    url: "/admin/createflight",
    type: "POST",
    data: data,
    dataType: "json",
    success: function(resp) {
      window.location.href = "/flights/";
    },
    error: function(resp) {
      $error.text(resp.responseJSON.error).removeClass("error--hidden");
      setTimeout(() => {
        $error.addClass("error--hidden");
      }, 3000);
    }
  });
  e.preventDefault();
});

$("form[name=add_admin_form").submit(function(e) {
  var $form = $(this);
  var $error = $form.find(".error");
  var data = $form.serialize();

  $.ajax({
    url: "/admin/makeadmin/",
    type: "POST",
    data: data,
    dataType: "json",
    success: function(resp) {
      window.location.href = "/admin/";
    },
    error: function(resp) {
      $error.text(resp.responseJSON.error).removeClass("error--hidden");
      setTimeout(() => {
        $error.addClass("error--hidden");
      }, 3000);
    }
  });
  e.preventDefault();
});

$("form[name=remove_admin_form").submit(function(e) {
  var $form = $(this);
  var $error = $form.find(".error");
  var data = $form.serialize();

  $.ajax({
    url: "/admin/removeadmin/",
    type: "POST",
    data: data,
    dataType: "json",
    success: function(resp) {
      window.location.href = "/admin/";
    },
    error: function(resp) {
      $error.text(resp.responseJSON.error).removeClass("error--hidden");
      setTimeout(() => {
        $error.addClass("error--hidden");
      }, 3000);
    }
  });
  e.preventDefault();
});

$("form[name=reserve_flight_form").submit(function(e) {
  var $form = $(this);
  var $error = $form.find(".error");
  var data = $form.serialize();

  $.ajax({
    url: "/flights/reserve/",
    type: "POST",
    data: data,
    dataType: "json",
    success: function(resp) {
      window.location.href = "/flights/";
    },
    error: function(resp) {
      $error.text(resp.responseJSON.error).removeClass("error--hidden");
      setTimeout(() => {
        $error.addClass("error--hidden");
      }, 3000);
    }
  });
  e.preventDefault();
});

$("form[name=edit_flight_form").submit(function(e) {
  var $form = $(this);
  var $error = $form.find(".error");
  var data = $form.serialize();

  $.ajax({
    url: "/admin/editcost/",
    type: "POST",
    data: data,
    dataType: "json",
    success: function(resp) {
      window.location.href = "/admin/";
    },
    error: function(resp) {
      $error.text(resp.responseJSON.error).removeClass("error--hidden");
      setTimeout(() => {
        $error.addClass("error--hidden");
      }, 3000);
    }
  });
  e.preventDefault();
});

$("form[name=delete_flight_form").submit(function(e) {
  var $form = $(this);
  var $error = $form.find(".error");
  var data = $form.serialize();

  $.ajax({
    url: "/admin/deleteflight/",
    type: "POST",
    data: data,
    dataType: "json",
    success: function(resp) {
      window.location.href = "/admin/";
    },
    error: function(resp) {
      $error.text(resp.responseJSON.error).removeClass("error--hidden");
      setTimeout(() => {
        $error.addClass("error--hidden");
      }, 3000);
    }
  });
  e.preventDefault();
});

$("form[name=cancel_reservation_form").submit(function(e) {
  var $form = $(this);
  var $error = $form.find(".error");
  var data = $form.serialize();

  $.ajax({
    url: "/user/reservations/cancel/",
    type: "POST",
    data: data,
    dataType: "json",
    success: function(resp) {
      window.location.href = "/user/reservations/";
    },
    error: function(resp) {
      $error.text(resp.responseJSON.error).removeClass("error--hidden");
      setTimeout(() => {
        $error.addClass("error--hidden");
      }, 3000);
    }
  });
  e.preventDefault();
});