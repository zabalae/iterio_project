$(document).ready(function() {
    $('#id_category').change(function() {
        var url = "/ajax/load-subcategories/";
        var categoryId = $(this).val();

        $.ajax({
            url: url,
            data: {
                'category': categoryId
            },
            success: function (data) {
                $("#id_subcategory").html(data);
            }
        });
    });
});