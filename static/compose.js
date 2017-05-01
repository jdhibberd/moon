
$(document).ready(function() {

  $("#save-button")
    .click(function() {
      document.form.submit();
    });

  $("#archive-button")
    .click(function() {
      var noteId = $(this).data("note-id");
      var referer = $(this).data("referer");
      $.post("/notes/" + noteId + "/archive", function() {
        window.location.href = referer;
      });
    })
    .attr("value", "Archive");

  $("#unarchive-button")
    .click(function() {
      var noteId = $(this).data("note-id");
      var referer = $(this).data("referer");
      $.post("/notes/" + noteId + "/unarchive", function() {
        window.location.href = referer;
      });
    })
    .attr("value", "Unarchive");

    $("#cancel-button")
      .click(function() {
        var referer = $(this).data("referer");
        window.location.href = referer;
      });

});
