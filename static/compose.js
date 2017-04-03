
$(document).ready(function() {

  $("#archive-button")
    .click(function() {
      var noteId = $(this).data("note-id");
      var referer = $(this).data("referer");
      $.post("/notes/" + noteId + "/archive", function() {
        window.location.href = referer;
      });
    })
    .attr("href", "#")
    .html("Archive");

  $("#unarchive-button")
    .click(function() {
      var noteId = $(this).data("note-id");
      var referer = $(this).data("referer");
      $.post("/notes/" + noteId + "/unarchive", function() {
        window.location.href = referer;
      });
    })
    .attr("href", "#")
    .html("Unarchive");

});

function submit() {
  document.form.submit();
}
