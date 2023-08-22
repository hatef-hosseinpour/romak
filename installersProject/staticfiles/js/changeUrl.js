// $.ajax({
//   url: "/api/users/auth-status/",
//   method: "GET",
//   success: function (response) {
//     if (response.is_authenticated) {
//       window.location.replace(window.location.href);
//     } else {
//       console.log("You are not Authenticate!!!!");
//     }
//   },
//   error: function () {
//     console.log("ERROR");
//   },
// });
// auth-check.js

$(document).ready(function () {
  $.ajax({
    url: "api/users/auth-status/",
    type: "GET",
    success: function (response) {
      if (response.message === true) {
        // User is authenticated, redirect to previous page
        window.history.back();
      } else {
        // window.location.href = "/login/";
        console.log(response.message);
      }
    },
    error: function () {
      console.log("Failed to check authentication status");
    },
  });
});
