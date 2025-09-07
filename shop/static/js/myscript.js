$(document).ready(function () {
    var urlParams = new URLSearchParams(window.location.search);
    if (urlParams == "") {
        localStorage.clear();
        $("#filter_state").css("display", "none");
    } else {
        $("#filter_state").css("display", "inline-block");
    }

    $('input:checkbox').on('click', function () {
        var favs = [];
        $('input:checkbox').each(function () {
            var fav = { id: $(this).attr('id'), value: $(this).prop('checked') };
            favs.push(fav);
        });

        localStorage.setItem("favorites", JSON.stringify(favs));
    });

    var favorites = JSON.parse(localStorage.getItem("favorites"));
    for (var i = 0; i < favorites.length; i++) {
        $('#' + favorites[i].id).prop('checked', favorites[i].value);
    }
});

function showVal(x) {
    // alert(x)
    x = x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    document.getElementById('sel_price').innerText = x;
}

function removeURLParameter(url, parameter) {
    var urlparts = url.split("?");
    if (urlparts.length >= 2) {
        var prefix = encodeURIComponent(parameter) + "=";
        var pars = urlparts[1].split(/[&;]/g);
        for (var i = pars.length; i-- > 0;){
            if (pars[i].lastIndexOf(prefix, 0) !== -1) {
                pars.splice(i, 1);
            }
        }
        return urlparts[0] + (pars.length > 0 ? '?' + pars.join('&'): '');
    }
    return url;
}
function select_sort() {
    var select_sort_value = $("#select_sort").val();
    var url = removeURLParameter(window.location.href, "sort_type");

    // بررسی اینکه آیا قبلاً ? توی URL هست
    var separator = url.includes("?") ? "&" : "?";
    
    window.location = url + separator + "sort_type=" + select_sort_value;
}

// تابع دریافت تعداد جدید پروداکت های نمایشی در هر صفحه بر اساس انتخاب یوزر
function update_product_numbers() {
    var product_numbers_value = $('#product_numbers').val();
    var url = removeURLParameter(window.location.href, "product_numbers");
    
    var separator = url.includes('?') ? '&' : '?';
    window.location.href = url + separator + "product_numbers=" + product_numbers_value;
}
// Shop Cart ............................................

function status_of_shop_cart() {
    $.ajax({
        type: "GET",
        url: "/orders/status_of_shop_cart/",
        success: function (res) {
            $("#indicator__value").text(res);
 
 
        }
    });
}

status_of_shop_cart();

function add_to_shop_cart(product_id, quantity) {
    if (quantity==0) {
        quantity = $("#product-quantity").val();

    }
    $.ajax({
        type: "GET",
        url: "/orders/add_to_shop_cart/",
        data: {
            product_id: product_id,
            quantity: quantity
        },
        success: function (res) {
            alert("کالای مورد نظر به سبد خرید شما اضافه شد");
            status_of_shop_cart();
        }
    });
}

function delete_from_shop_cart(product_id) {
    $.ajax({
        type: "GET",
        url: "/orders/delete_from_shop_cart/",
        data: {
            product_id: product_id,
        },
        success: function (res) {
            alert("کالای مورد نظر از سبد شما حذف شد");
            $("#shop_cart_list").html(res)      //    $("#shop_cart_list").load("/orders/show_shop_cart/"); // معادل هم هستن
            status_of_shop_cart();
   
        }
    });
}


function update_shop_cart() {
    // alert("Test");
    var product_id_list = []
    var qty_list = []

    // اینپوت هایی رو پیدا کن ایدیشون شروع بشه با
    // each is like for
    // push is like append
    // $(this) : عنصری که نوبش شده
    //.attr(id).slice(4) : ویژگی ایدی چهارمی به بعد رو که فقظ عدده که میشه ایدی
    $("input[id^='qty_']").each(function(index) { 
        product_id_list.push($(this).attr('id').slice(4));
        qty_list.push($(this).val());
});
    // console.log(product_id_list);
    // console.log(qty_list);


    $.ajax({
        type:"GET",
        url:"/orders/update_shop_cart/",
        data:{
            product_id_list:product_id_list,
            qty_list:qty_list
        },
        success: function(res) {
            alert("تعداد کالا ها بروز رسانی شد")
            $("#shop_cart_list").html(res); 
            status_of_shop_cart();
            alert("تعداد کالا ها بروز رسانی شد");
            
            
        }
    });

};

//--------------------------------------------------comment---------------------------

function showCreateCommentForm(productId, commentId, slug) {
    $.ajax({
        type: "GET",
        url: "/csf/create_comment/" + slug,
        data: {
            productId: productId,
            commentId: commentId,
        },
        success: function(res) {
            $("#btn_" + commentId).hide(); // دکمه پاسخ مخفی بشه

            // نمایش فرم همراه با ضربدر
            $("#comment_form_" + commentId).html(`
                <div style="position: relative;">
                    <button onclick="hideCommentForm(${commentId})" class="close-button">×</button>
                    ${res}
                </div>
            `);
            

            console.log("FORM LOADED:", res);
        }
    });
}

// ----------------------------------------------------------------------------------------------
// ستاره های امتیاز دهی - ثبت امتیاز در پروداکت دیتیل

function addScore(score,productId){
    var starRatings = document.querySelectorAll(".fa-star");
    
    
    // همه ستاره ها رو مشکی کن - چکدهاشون رو پاک کن
    starRatings.forEach(element =>{
        element.classList.remove("checked");
    });



    
    // به تعداد اسکور بهشون چکد اضافه میکنم
    for (let i = 1; i<= score; i++) {
        const element = document.getElementById("star_" + i);
        element.classList.add("checked");
    }

    $.ajax({
        type : "GET",
        url : "/csf/add_score/",
        data : {
            productId : productId,
            score : score,
        },
        success : function(res) {
            alert(res.message); // پیام موفقیت
            $("#avg_score").text(res.avg_score); // میانگین جدید رو بذار
        }
        
    });

    starRatings.forEach(element =>{
        element.classList.add("disable");
    });

}


// -------------------------------------------------


function star_score_percent(productId, avgScore) {
    const percent = (avgScore / 5) * 100;
    const star = document.getElementById("star_fill_" + productId);
    if (star) {
        star.style.width = percent + "%";
    }
}

//-------------------------------------------------------------

function addTofavorites(productId) {
    $.ajax({
        type: "GET",
        url: "/csf/add_to_favorites/",
        data: {productId: productId},
        success: function (res) {
            alert(res.message)
            // Update icon
            const button = $(`#favorite-btn-${productId}`);
            const icon = button.find('i');
            icon.removeClass('fa-heart fa-heart-broken').addClass(res.icon_class);
            
            // Show notification
            showNotification(res.message, 'success');
        },
        error: function(xhr) {
            const error = xhr.responseJSON?.error || 'خطایی رخ داد';
            showNotification(error, 'error');
        }
    });
}

function showNotification(message, type) {
    const alertClass = type === 'success' ? 'alert-success' : 'alert-danger';
    const notification = $(`
        <div class="alert ${alertClass} notification-alert">
            ${message}
        </div>
    `).appendTo('body');
    
    setTimeout(() => notification.remove(), 3000);
}


function status_of_favorite() {
    $.ajax({
        type: "GET",
        url: "/csf/status_of_favorite/",
        success: function (res) {
            $("#indicator__value_favorite").text(res.count);
 
 
        }
    });
}
status_of_favorite();
    

// -------------------------------------------------





function status_of_compare_list() {
    $.ajax({
        type: "GET",
        url: "/products/status_of_compare_list/",
        success: function(res) {
            if(Number(res) === 0) {
                $("#compare_count_icon").hide();    
            } else {
                $("#compare_count_icon").show();
                $("#compare_count").text(res);
            }
            
        }
    });
}




function addToCompareList(productId, productGroupId) {
    $.ajax({
        type: "GET",
        url: "/products/add_to_compare_list/",
        data: {
            productId: productId,
            productGroupId: productGroupId,
        },
        success: function(res) {
            alert(res);
            status_of_compare_list();
        }
    });
}



function deleteFromCompareList(productId) {
    $.ajax({
        type: "GET",
        url: "/products/delete_from_compare_list/",
        data: {
            productId: productId,
        },
        success: function(res) {
            alert('حذف با موفقیت انجام شد');

            // این کد دیوی که این ایدی رو داره رو بدون رفرش کردن اون بروز رسانی میکنه
            $("#compare_list").html(res); 
            status_of_compare_list();
        }
    });
}




status_of_compare_list();