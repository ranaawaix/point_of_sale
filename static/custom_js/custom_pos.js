$(document).ready(function () {
    $('.product').on('click', function (e) {
        e.preventDefault();
        var prod_id = $(this).data('pid');
        var sale_id = $('#saleId').data('sid');
        let csrf = $("input[name=csrfmiddlewaretoken]").val();
        console.log(sale_id, prod_id);
        let my_data = {}
        if (sale_id) {
            my_data = {prod_id: prod_id, sale_id: sale_id, csrfmiddlewaretoken: csrf}
        } else {
            my_data = {prod_id: prod_id, csrfmiddlewaretoken: csrf}
        }
        var url = $(this).data('url');
        console.log(my_data, url);
        $.ajax({
            url: url, method: 'POST', data: my_data, success: function (rsp) {
                console.log(rsp)
                $('.billing').html(rsp);
            }
        })
    })
});
