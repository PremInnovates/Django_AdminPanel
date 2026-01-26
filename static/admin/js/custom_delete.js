$(document).on("click", ".delete-btn", function (e) {
    e.preventDefault();

    if (!confirm("Delete this record?")) return;

    let btn = $(this);

    $.post("/admin/api/delete/", {
        model: btn.data("model"),
        id: btn.data("id"),
        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
    }, function () {
        btn.closest("tr").fadeOut();
    });
});
