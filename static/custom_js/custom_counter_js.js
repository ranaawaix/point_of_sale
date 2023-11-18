$(document).ready(function () {
    $('.holdForm').on('submit', function (e) {
        e.preventDefault();
        var sale_id = $('#SaleID').data('slid');
        var note = $(this).find('#id_reference_note').val();
        let csrf = $("input[name=csrfmiddlewaretoken]").val();
        let url = $('#SaleID').data('url');
        console.log(sale_id, note);
        my_data = {sale_id: sale_id, note: note, csrfmiddlewaretoken: csrf}
        $.ajax({
            url: url, method: 'POST', data: my_data, success: function (data) {
                if (data.status === 'Saved') {
                    $('#modalHold').modal('show');
                    $("#msg strong").text("Order Held successfully");
                    $("#msg").show();
                    setTimeout(function () {
                        $('#modalHold').modal('hide');
                    }, 5000);
                    $('.modal-backdrop').removeClass('modal-backdrop fade');
                } else if (data.status === 0) {
                    $('#modalHold').modal('show');
                    $("#msgfail strong").text("Unable to Hold order");
                    $('#msgfail').show();
                    setTimeout(function () {
                        $('#modalHold').modal('hide');
                    }, 5000);
                    $('.modal-backdrop').removeClass('modal-backdrop fade');
                }
            }
        });
    });
    $('.customerForm').on('submit', function (e) {
        e.preventDefault();
        var name = $(this).find('#id_name').val();
        var email = $(this).find('#id_email').val();
        var phone = $(this).find('#id_phone').val();
        var custom_1 = $(this).find('#id_customer_custom_field_1').val();
        var custom_2 = $(this).find('#id_customer_custom_field_2').val();
        let csrf = $("input[name=csrfmiddlewaretoken]").val();
        var sale_id = $('#SaleId').data('saleid');
        let url = $('#SaleId').data('url');
        console.log(name, email, phone, custom_1, custom_2, sale_id);
        my_data = {
            sale_id: sale_id,
            name: name,
            email: email,
            phone: phone,
            custom_1: custom_1,
            custom_2: custom_2,
            csrfmiddlewaretoken: csrf
        }
        $.ajax({
            url: url, method: 'POST', data: my_data, success: function (rsp) {
                let customer_id = rsp.cust_id;
                if (rsp.status === 'Saved') {
                    $('#modalCustomer').modal('show');
                    $("#msgc strong").text("Added the customer successfully");
                    $("#msgc").show();
                    setTimeout(function () {
                        $('#modalCustomer').modal('hide');
                    }, 5000);
                    $('.modal-backdrop').removeClass('modal-backdrop fade');
                    if (customer_id) {
                        console.log(customer_id);
                        $('#id_customer').val(customer_id);
                    }
                } else if (rsp.status === 0) {
                    $('#modalCustomer').modal('show');
                    $("#msgcfail strong").text("Unable to add customer");
                    $('#msgcfail').show();
                    setTimeout(function () {
                        $('#modalCustomer').modal('hide');
                    }, 5000);
                    $('.modal-backdrop').removeClass('modal-backdrop fade');
                }
            }
        });
    });
    $('.paymentForm').on('submit', function (e) {
        e.preventDefault();
        var sale_id = $('#saleId').data('sid');
        let url = $('#Saleid').data('url');
        var note = $(this).find('#id_note').val();
        var amount = $(this).find('#id_amount').val();
        var payment_by = $(this).find('#id_payment_by').val();
        var payment_note = $(this).find('#id_payment_note').val();
        let csrf = $("input[name=csrfmiddlewaretoken]").val();
        console.log(note, amount, payment_by, payment_note, sale_id);
        my_data = {
            sale_id: sale_id,
            note: note,
            amount: amount,
            payment_by: payment_by,
            payment_note: payment_note,
            csrfmiddlewaretoken: csrf
        }
        $.ajax({
            url: url, method: 'POST', data: my_data, success: function (rsp) {
                if (rsp.status === 'Saved') {
                    $('#modalPayment').modal('show');
                    $("#msgp strong").text("Payment submitted successfully");
                    $("#msgp").show();
                    setTimeout(function () {
                        $('#modalPayment').modal('hide');
                    }, 5000);
                    $('.modal-backdrop').removeClass('modal-backdrop fade');
                } else if (rsp.status === 0) {
                    $('#modalPayment').modal('show');
                    $("#msgpfail strong").text("Unable to submit payment");
                    $('#msgpfail').show();
                    setTimeout(function () {
                        $('#modalPayment').modal('hide');
                    }, 5000);
                    $('.modal-backdrop').removeClass('modal-backdrop fade');
                }
            }
        });
    });
    $(".btn-group-vertical button").on("click", function () {
        var buttonText = $(this).text();
        var total_paying = $(this).val();
        var total_payable = $('#totalPayable').data('tp');
        var balance = total_paying - total_payable
        console.log(total_paying, total_payable, balance);
        $('#totalPaying').html(buttonText);
        $('#id_amount').val(total_payable);
        $('#balance').html(balance);
    });
    $("#clear").on("click", function () {
        $('#totalPaying').html(0);
        $('#id_amount').val(0);
    });
    $(document).ready(function () {
        $('#delete_saleitem a').on('click', function (e) {
            e.preventDefault();
            console.log('Open Prevented');
            var sale_id = $('#saleId').data('sid');
            var saleitem_id = $(this).data('sp');
            let url = $(this).data('url');
            let csrf = $("input[name=csrfmiddlewaretoken]").val();
            console.log(sale_id, saleitem_id);
            var my_data = {sale_id: sale_id, saleitem_id: saleitem_id, csrfmiddlewaretoken: csrf}
            $.ajax({
                url: url, method: 'POST', data: my_data, success: function (rsp) {
                    console.log(rsp)
                    $('.billing').html(rsp);
                }
            })
        })
    })
});