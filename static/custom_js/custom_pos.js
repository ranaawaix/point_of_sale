$(document).ready(function () {
    $('.product').each(function () {
      $(this).on('click', function (e) {
        e.preventDefault();
        let prod_id = $(this).data('pid');
        let user_id = $(this).data('user');
        let register_id = $(this).data('register_id');
        let sale_id = $('#saleId').data('sid');
        let csrf = $("input[name=csrfmiddlewaretoken]").val();
        console.log(sale_id, prod_id, user_id, register_id);
        let my_data = {}
        if (sale_id) {
            my_data = {
                prod_id: prod_id,
                sale_id: sale_id,
                user_id: user_id,
                register_id: register_id,
                csrfmiddlewaretoken: csrf
            }
        } else {
            my_data = {prod_id: prod_id, user_id: user_id, register_id: register_id, csrfmiddlewaretoken: csrf}
        }
        var url = $(this).data('url');
        console.log(my_data, url);
        $.ajax({
            url: url, method: 'POST', data: my_data, success: function (rsp) {
                console.log(rsp)
                $('.billing').html(rsp);
                $('.billing .table-bordered tr').each(function () {
                    $(this).find('#sale_item_quantity').each(function () {
                        $(this).on('blur', function () {
                            let quantity = $(this).val();
                            let sale_id = $('#saleId').data('sid');
                            let price = $(this).closest('tr').find('.saleitem_price').text();
                            let result = quantity * price;
                            $(this).closest('tr').find('.saleitem_subtotal').text(result);
                            let subtotal = result.toFixed();
                            let eurl = $('#sale_item_quantity').data('eurl');
                            let my_data = {
                                prod_id: prod_id,
                                sale_id: sale_id,
                                user_id: user_id,
                                register_id: register_id,
                                quantity: quantity,
                                price: price,
                                subtotal: subtotal,
                                csrfmiddlewaretoken: csrf
                            }
                            console.log(my_data);
                            $.ajax({
                                url: eurl, method: 'POST', data: my_data, success: function (rsp) {
                                    console.log(rsp);
                                    $('.billing').html(rsp);
                                },
                                error: function (xhr, status, error) {
                                    console.error(error);
                                }
                            });
                        });
                    })
                })
            }
        })
    })
    })
});
