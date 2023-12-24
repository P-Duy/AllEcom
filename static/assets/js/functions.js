console.log("working fine");

$("#commentForm").submit(function (e) {
    e.preventDefault();

    $.ajax({
        data: $(this).serialize(),

        method: $(this).attr("method"),

        url: $(this).attr("action"),

        dataType: "json",

        success: function (res) {
            console.log("Comment Saved");

            if (res.bool == true) {
                $("#review-res").html("review added successfully..");
            }
        },
    })
})