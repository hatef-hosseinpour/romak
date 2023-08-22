// console.log(window.location.pathname);
console.log(encodeURIComponent(document.referrer));
$(document).ready(function () {
  $.ajax({
    url: "/api/users/auth-status/",
    type: "GET",
    success: function (response) {
      if (response.message === false) {
        // User is authenticated, redirect to previous page
        window.location.href = `/login/?next=${encodeURIComponent(
          document.referrer
        )}`;
      } else {
        console.log(response.message);
      }
    },
    error: function () {
      console.log("Failed to check authentication status");
    },
  });
});
