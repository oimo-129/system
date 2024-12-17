$(function() {
    if ($("#swiper-index").size() > 0) {
        console.log($(".banner-img").height())
        $("#swiper-index .swiper-slide").css("height", $(".banner-img").height());
        $("#bannervideo").show().css("height", $(".banner-img").height());
        greeSite.initSwiperImg("#swiper-index .banner-img", 2.04);

        console.log($(".banner-img").height())
    }
    //index
    greeSite.bannerShow('#swiper-index', '.swiper-pagination-index', true);

    $("#swiper-index").css("height", $(".banner-img").height());

    //news
    greeSite.bannerNews('#swiper-index-news', '.swiper-pagination-news', true);


    $(".swiper-slide-bg,.swiper-slide-bg-item").css({
        height: $(window).height()
    })
});

(function() {
    let close = document.getElementById("p1");
    let open = document.getElementById("p2");
    let m = document.querySelector("#bannervideo");
    let c = function() {
        m.muted = false;
        close.style.display = "none";
        open.style.display = "block";
    }
    if (close) {
        close.addEventListener("click", c, false);
    }

    let o = function() {
        m.muted = true;
        close.style.display = "block";
        open.style.display = "none";
    }
    if (open) {
        open.addEventListener("click", o, false);
    }
})();




//详情参数组装数据
var getHotProductParams = function(form, modelId) {
    var obj = {};
    var formArray = $(form).serializeArray();
    $.each(formArray, function() {
        if (obj[this.name] !== undefined) {
            if (!obj[this.name].push) {
                obj[this.name] = [obj[this.name]];
            }
            obj[this.name].push(this.value || '');
        } else {
            obj[this.name] = this.value || '';
        }
    });
    obj.modelId = modelId;
    console.log("getDetailsParams-", obj)
    return obj;
};
var getHotProduct = function(o) {
    var id = $(o).attr("data-id");
    greeSite.queryData("/hotProduct/" + id, '', function(res) {
        $(".tab-pane-s").html('<div class="loading" id="loading"></div>');
        $('.nav-tabs-category-item').parent().removeClass("active");
        $(o).parent().addClass("active");
        renderHotProductHtml(res);
    });
};


//详情参数
var renderHotProductHtml = function(res) {
    var html = '<ol class="hotProduct-showlist row">';

    //	 

    //	 <li class="hotProduct-lager col-lg-3 hotProduct-normal-1">
    //		<a href="/cmsProduct/view/3189" class="hotProduct-lager-img view view-first">
    //		<div class="hotProduct-itemImg scale-img-mask">
    //			<img src="/static/pc/img/hotproduct/1.jpg" alt="">
    //		</div>
    //		<h3 class="shows-title">1级文字<br/><span>2级文字</span></h3>
    //		<div class="mask">
    //			<h2 class="mask-title">1级文字<br/><span>2级文字</span></h2>
    //			<span  class="info hotProduct-view-more-s">了解更多</span>
    //		</div>
    //		</a>
    //
    //</li>
    //<li class="hotProduct-normal  col-lg-3 hotProduct-normal-2">
    //	<a href="/cmsProduct/view/3082" class="hotProduct-normal-item view view-first">
    //		<div class="hotProduct-itemImg scale-img-mask" >
    //			<img src="/static/pc/img/hotproduct/2.jpg" alt="">
    //		</div>
    //		<h3 class="shows-title">1级文字<br/><span>2级文字</span></h3>
    //		<div class="mask">
    //			<h2 class="mask-title">1级文字<br/><span>2级文字</span></h2>
    // 		<span class="info hotProduct-view-more-s">了解更多</span>
    //		</div>
    //	 </a>
    //
    //</li>

    $.each(res, function(i, v) {
        if (i == 0) {

            if (v.href !== undefined && v.href != '') {
                html += '<li class="hotProduct-lager col-lg-3 hotProduct-normal-' + Number(i + 1) + '">';
                html += '    <a href="' + v.href + '" target="_blank" class="hotProduct-lager-img view view-first">';
                html += '    	<div class="hotProduct-itemImg scale-img-mask">';
                html += '    	<img src="' + v.image + '" alt="">';
                html += '    	</div>';
                html += ' 		<h3 class="shows-title">' + v.title + '<br/><span>' + v.remarks + '</span></h3>';
                html += ' 		<div class="mask">';
                html += ' 			<h2 class="mask-title">' + v.title + '<br/><span>' + v.remarks + '</span></h2>';
                html += ' 			<span  class="info hotProduct-view-more-s">了解更多</span>';
                html += ' 		</div>';
                html += '    </a>';
                html += '</li>';
            } else {
                html += '<li class="hotProduct-lager col-lg-3 hotProduct-normal-' + Number(i + 1) + '">';
                //html += '    <div class="hotProduct-lager-img view view-first">';

                html += ' <a href="javascript:;" class="hotProduct-normal-item view view-first" style="cursor:default;">';

                html += '    <div class="hotProduct-itemImg scale-img-mask">';
                html += '    	<img src="' + v.image + '" alt="">';
                html += '    </div>';
                html += ' 		<h3 class="shows-title">' + v.title + '<br/><span>' + v.remarks + '</span></h3>';
                html += ' 		<div class="mask">';
                html += ' 			<h2 class="mask-title">' + v.title + '<br/><span>' + v.remarks + '</span></h2>';
                html += ' 		</div>';

                html += '</a>';

                //html += ' 		</div>';
                html += '</li>';

            }

        } else {

            if (v.href !== undefined && v.href != '') {
                html += ' <li class="hotProduct-normal  col-lg-3 hotProduct-normal-' + Number(i + 1) + '">';
                html += '    <a href="' + v.href + '" target="_blank" class="hotProduct-lager-img view view-first">';
                html += '    	<div class="hotProduct-itemImg scale-img-mask">';
                html += '    	<img src="' + v.image + '" alt="">';
                html += '    	</div>';
                html += ' 		<h3 class="shows-title">' + v.title + '<br/><span>' + v.remarks + '</span></h3>';
                html += ' 		<div class="mask">';
                html += ' 			<h2 class="mask-title">' + v.title + '<br/><span>' + v.remarks + '</span></h2>';
                html += ' 			<span  class="info hotProduct-view-more-s">了解更多</span>';
                html += ' 		</div>';
                html += '    </a>';
                html += ' </li>';
            } else {
                html += ' <li class="hotProduct-normal  col-lg-3 hotProduct-normal-' + Number(i + 1) + '">';
                //html += '    <div  class="hotProduct-normal-item view view-first">';

                html += ' <a href="javascript:;" class="hotProduct-normal-item view view-first" style="cursor:default;">';

                html += '    <div class="hotProduct-itemImg scale-img-mask">';
                html += '    	<img src="' + v.image + '" alt="">';
                html += '    </div>';
                html += ' 		<h3 class="shows-title">' + v.title + '<br/><span>' + v.remarks + '</span></h3>';
                html += ' 		<div class="mask">';
                html += ' 			<h2 class="mask-title">' + v.title + '<br/><span>' + v.remarks + '</span></h2>';
                html += ' 		</div>';

                html += '</a>';

                //html += ' 		</div>';
                html += '</li>';
            }


        }
    });
    html += ' </ol>';
    setTimeout(function() {
        $(".tab-pane-s").empty().html(html);
    }, 100);
};