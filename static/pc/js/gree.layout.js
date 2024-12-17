$(function() {
    //navbar
    $(document).scroll(function(e) {
        var scrollTop = $(document).scrollTop();

        if (scrollTop > 70) {
            $(".navbar")
                .removeClass("navbar-static-top")
                .addClass("navbar-fixed-top");
        } else {
            $(".navbar")
                .removeClass("navbar-fixed-top")
                .addClass("navbar-static-top");
        }
        if (scrollTop < 70) {
            $("#gree-header-about").addClass("none")

        }

    });

    $(document).scroll(function() {
        var scrollTop = $(this).scrollTop(); //滚动高度
        if (scrollTop > 140) { //
            if ($("#gree-product-subNav").size() > 0) {
                $("#gree-product-subNav").addClass("fixed-top-sub");


            }
        } else {
            if ($("#gree-product-subNav").size() > 0) {
                $("#gree-product-subNav").removeClass("fixed-top-sub");
            }
        }

    });
    $("#showAboutGree").on("click", function(e) {
        $("#gree-header-about").toggleClass("none")
    });

    $(".green-dropdown ,#about-nav").hover(function() {
        $("body").addClass("hd-lock");
    }, function() {});



    // green-dropdown
    $('.green-dropdown').dropdownNav({
        dropdownEl: 'green-dropdown-menu',
        openedClass: 'open'
    });

    $('#about-nav').dropdownNav({
        dropdownEl: 'about-nav-dropBox',
        openedClass: 'open-about'
    });
    $('#about-nav-sub').dropdownNav({
        dropdownEl: 'about-nav-drop',
        openedClass: 'open'
    });
    $('#about-nav-sub2').dropdownNav({
        dropdownEl: 'about-nav-drop2',
        openedClass: 'open'
    });
    // green-search
    $("#navbar-nav-search-result").on("click", function(e) {
        e.stopPropagation();
    });
    $("#navbar-search-close").on("click", function(e) {
        $(this).dropdown('toggle');
        $("body").removeClass("lockScreen")
    });

    $('#navbar-nav-search').on('show.bs.dropdown', function() {
        $("body").addClass("lockScreen");
        if ($.cookie('searchHistroy') != undefined) {
            $('#search-result-histroy').append($.cookie('searchHistroy'));
        }

    });
    $('#navbar-nav-search').on('hide.bs.dropdown', function() {
        $("body").removeClass("lockScreen")
    })
    //search
    $('#navbar-search-key').on('focus', function() {
        $('#navbar-search-suggest').collapse()
    });


});


var decode = function(str) {
    var _str = str.join(',');
    return _str;
}
var encode = function(str) {
    var _arr = str.split(',');
    return _arr;
}


//获取产品列表
var getSearchHistroy = function() {
    var histroyKeyArr = [];
    var searchHistroy = $("#navbar-search-key").val();
    var html = "";
    html += ' <li  class="col-lg-3">';
    html += '     <a href="/searchForm?keyword=' + searchHistroy + '">' + searchHistroy + '</a>';
    html += ' </li>';
    $('#search-result-histroy').append(html);
    var htmlArr = $('#search-result-histroy').html();
    $.cookie('searchHistroy', htmlArr, {
        expires: 1
    });
};