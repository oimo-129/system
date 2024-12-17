/* 系统公用方法 */
(function(win, doc) {
    var greeSite = {
        host: "",
        wxhost: "",
        screen: function() {
            var w = $(window).width();
            return w >= 1200 ? 3 : w >= 992 ? 2 : w >= 768 ? 1 : 0;
        },
        //截取长度
        cutstr: function(str, len) {
            var str_length = 0;
            var str_len = 0;
            var str_cut = new String();
            var str_len = str.length;
            for (var i = 0; i < str_len; i++) {
                var a = str.charAt(i);
                str_length++;
                if (escape(a).length > 4) {
                    str_length++;
                }
                str_cut = str_cut.concat(a);
                if (str_length >= len) {
                    str_cut = str_cut.concat("...");
                    return str_cut;
                }
            }
            if (str_length < len) {
                return str;
            }
        },
        //获取URL参数 key 参数名称 url URL链接，默认为当前URL
        getUrlKey: function(key, url) {
            var url = url ? url : location.href;
            var v = '';
            var o = url.indexOf(key + "=");
            if (o != -1) {
                o += key.length + 1;
                e = url.indexOf("&", o);
                if (e == -1) {
                    e = url.length;
                }
                //v = decodeURIComponent(url.substring(o, e));
                v = url.substring(o, e);
            }
            return v;
        },
        copyrightYear: function(id) {
            var year = new Date().getFullYear();
            $(id).html("2014-" + year);
        },
        queryData: function(url, params, callback) {
            $.ajax({
                type: "post",
                url: url,
                data: JSON.stringify(params),
                dataType: 'json',
                contentType: "application/json",
                success: function(res) {
                    callback(res);
                },
                error: function(res) {
                    console.log(res, '请求失败')
                }
            });
        },
        initSwiperImg: function(o, ratio) {
            $(o).width($(window).width()).height(($(window).width() / ratio));
        },
        play_v: function(v) {
            $(v).play()
        },
        stop_v: function(v) {
            $(v).pause();
        },
        //banner
        bannerShow: function(obj, pagination, autoplay) {
            var delayTime = "";
            if ($(obj).size() > 0) {
                var delayTimeV = $("#bannervideo").attr("data-durationTime");
                if ($("#bannervideo").size() > 0) {
                    console.log(delayTimeV);
                    delayTime = delayTimeV
                } else {
                    delayTime = 3000;
                }
                //console.log("delayTime--",delayTime)
                var swiperNew = new Swiper(obj, {
                    autoplay: autoplay,
                    loop: false,
                    effect: 'fade',
                    speed: 300,
                    //observer:true,
                    //observeParents:true,
                    autoplay: {
                        delay: delayTime
                    },
                    pagination: {
                        clickable: true,
                        el: pagination
                    },

                    on: {
                        init: function() {
                            if ($("#bannervideo").size() > 0) {
                                var videoIndex = $("#bannerVdeo_index").val();
                                $("#swiper-index .swiper-slide").css("height", $(".banner-img").height());
                                $("#bannervideo").show().css("height", $(".banner-img").height());
                                if (this.activeIndex == videoIndex) {
                                    $('#bannervideo').trigger('play');
                                    $(".bannervideo-view").addClass("bannervideo-view-show");
                                    $(".bannervideo-info").addClass("bannervideo-info-show");

                                } else {
                                    //$('#bannervideo').trigger('pause');
                                }
                                //监听播放情况 
                                var v = document.getElementById("bannervideo");
                                v.addEventListener('play', function() {
                                    if (v.ended) {
                                        swiperNew.slideNext(300, false);

                                        return false;
                                    } else {

                                        //$('#p1').trigger('click');
                                    }
                                }, false);
                            }
                            var len = this.slides.length;


                            if (len <= 1) {
                                $(pagination).hide();
                                this.destroy(false);
                                this.autoplay.stop();
                            }
                            if (this.slides[this.activeIndex].dataset != undefined) {
                                var theme = this.slides[this.activeIndex].dataset.theme;
                                if (theme) {
                                    greeSite.bannerTheme(theme)
                                }
                            }
                        },
                        click: function(swiper) {
                            if ($("#bannervideo").size() > 0) {
                                var videoIndex = $("#bannerVdeo_index").val();
                                if (this.activeIndex == videoIndex) {
                                    $('#bannervideo').trigger('play');
                                    //$('#p1').trigger('click');
                                    document.getElementById("bannervideo").currentTime = 0;
                                    $(".bannervideo-view").addClass("bannervideo-view-show");
                                    $(".bannervideo-info").addClass("bannervideo-info-show");
                                } else {
                                    $('#bannervideo').trigger('pause');
                                }
                            }
                        },
                        slideChangeTransitionStart: function() {
                            if ($("#bannervideo").size() > 0) {
                                var videoIndex = $("#bannerVdeo_index").val();
                                if (this.activeIndex == videoIndex) {
                                    $('#bannervideo').trigger('play');
                                    document.getElementById("bannervideo").currentTime = 0;
                                    //$('#p1').trigger('click');
                                    $(".bannervideo-view").addClass("bannervideo-view-show");
                                    $(".bannervideo-info").addClass("bannervideo-info-show");
                                } else {
                                    //$('#bannervideo').trigger('pause');
                                }
                            }
                            //theme
                            if (this.slides[this.activeIndex].dataset != undefined) {
                                var theme = this.slides[this.activeIndex].dataset.theme;
                                if (theme) {
                                    greeSite.bannerTheme(theme)
                                }
                            }
                        }
                    },
                });
                $(".swiper-container").hover(function() {
                    $("body").removeClass("hd-lock");
                    swiperNew.autoplay.stop();
                }, function() {

                    swiperNew.autoplay.start();
                });
            }
        },
        //banner
        bannerNews: function(obj, pagination, autoplay) {
            if ($(obj).size() > 0) {
                var swiper = new Swiper(obj, {
                    autoplay: autoplay,
                    loop: true,
                    pagination: {
                        clickable: true,
                        el: pagination
                    },

                    on: {
                        init: function() {
                            //                            var len = this.slides.length;
                            //                            if (len<=1) {
                            //                                $(pagination).hide();
                            //                                this.destroy(false);
                            //                                this.autoplay.stop();
                            //                            }

                        }
                    }
                });
            }
        },
        bannerTheme: function(theme) {

            if (theme == "lighten") {
                if ($("body").hasClass("hd-lock") && $('.green-dropdown-menu-lock').is(':visible')) {
                    $("body").addClass("hd-lock")
                } else {
                    $("body").removeClass("hd-lock")
                }
                $("#gree-header").addClass("lighten").removeClass("dark");
            } else if (theme == "dark") {
                if ($("body").hasClass("hd-lock") && $('.green-dropdown-menu-lock').is(':visible')) {
                    $("body").addClass("hd-lock")
                } else {
                    $("body").removeClass("hd-lock")
                }
                $("#gree-header").addClass("dark").removeClass("lighten");
            } else {

                $("#gree-header").removeClass("lighten").removeClass("dark");
            }
        },
        bannerCategoryLev: function(obj) {
            var swiper = new Swiper(obj, {
                slidesPerView: 3,
                spaceBetween: 0,
                slidesPerGroup: 3,
                pagination: {
                    el: 'swiper-pagination',
                    clickable: false
                }
            });
        },
        bannerCategory: function(obj) {
            var swiper = new Swiper(obj, {
                slidesPerView: 7,
                spaceBetween: 0,
                slidesPerGroup: 7,
                loopFillGroupWithBlank: true,

                pagination: {
                    el: 'swiper-pagination',
                    clickable: false
                },
                navigation: {
                    nextEl: '.swiper-gree-next',
                    prevEl: '.swiper-gree-prev',
                },
                on: {
                    init: function() {
                        var len = this.slides.length;
                        if (len <= 7) {
                            $(".swiper-button-item").remove();
                            var w = $(obj + " .swiper-slide").outerWidth(true);
                            $(obj + " .swiper-wrapper").css({
                                width: w * len
                            })
                        }

                    }
                }
            });
        },
        yearCategory: function(obj) {
            var swiper = new Swiper(obj, {
                slidesPerView: 10,
                spaceBetween: 0,
                slidesPerGroup: 1,
                loopFillGroupWithBlank: true,
                pagination: {
                    el: '.swiper-pagination',
                    clickable: true,
                },
                navigation: {
                    nextEl: '.swiper-year-next',
                    prevEl: '.swiper-year-prev',
                },
                on: {
                    init: function() {
                        var len = this.slides.length;
                        if (len <= 7) {
                            $(".swiper-button-item").remove();
                            var w = $(obj + " .swiper-slide").outerWidth(true);
                            $(obj + " .swiper-wrapper").css({
                                width: w * len
                            })
                        }

                    }
                }
            });
        },
    };
    win.greeSite = greeSite;
}(window, document));




//var mySwiper = new Swiper('.swiper-container',{
//    preventClicks : true,
//    pagination: '.swiper-pagination',
//    paginationClickable: '.swiper-pagination',
//    preventLinksPropagation : true,
//    spaceBetween: 30,
//    effect: 'fade',
//    
//
//});


function popup(title, time) {
    var html = '<div id="gree-popup"><div class="gree-layer"></div><div class="gree-open">' + title + '</div></div>';
    $(document.body).append(html);
    window.setTimeout(function() {
        $("#gree-popup").remove();
    }, time);
};