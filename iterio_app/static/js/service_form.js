$(document).ready(function() {
    $('.select2').select2();

    $('#id_category').change(function() {
        var categoryId = $(this).val();
        $.ajax({
            url: '/get_subcategories/' + categoryId,
            method: 'GET',
            success: function(data) {
                var subcategorySelect = $('#id_subcategory');
                subcategorySelect.empty();
                $.each(data, function(index, subcategory) {
                    subcategorySelect.append(new Option(subcategory.name, subcategory.id));
                });
            }
        });
    });
});