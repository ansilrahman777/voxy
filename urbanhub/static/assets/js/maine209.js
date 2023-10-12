(function ($) {
    ("use strict");
    // Page loading
    $(window).on("load", function () {
        $("#preloader-active").fadeOut("slow");
    });
    /*-----------------
        Menu Stick
    -----------------*/
    var header = $(".sticky-bar");
    var win = $(window);
    win.on("scroll", function () {
        var scroll = win.scrollTop();
        if (scroll < 100) {
            header.removeClass("stick");
            $(".header-style-2 .categories-dropdown-active-large").removeClass("open");
            $(".header-style-2 .categories-button-active").removeClass("open");
        } else {
            header.addClass("stick");
        }
    });

    /*-----------------
        Sidebar Sticky
    -----------------*/
    var sidebar = $(".sidebar-left");
    var win = $(window);
    win.on("scroll", function () {
        var scroll = win.scrollTop();
        if (scroll < 760) {
            sidebar.removeClass("stick");
        } else {
            sidebar.addClass("stick");
        }
    });

    /*------ Wow Active ----*/
    new WOW().init();
    //sidebar sticky
    if ($(".sticky-sidebar").length) {
        $(".sticky-sidebar").theiaStickySidebar();
    }
    /*---------------------
        Select active
    --------------------- */
    if ($(".select-active").length) {
        $(".select-active").select2();
    }
    /*---- CounterUp ----*/
    if ($(".count").length) {
        $(".count").counterUp({
            delay: 10,
            time: 600
        });
    }
    // Isotope active
    if ($(".grid").length) {
        $(".grid").imagesLoaded(function () {
            // init Isotope
            var $grid = $(".grid").isotope({
                itemSelector: ".grid-item",
                percentPosition: true,
                layoutMode: "masonry",
                masonry: {
                    // use outer width of grid-sizer for columnWidth
                    columnWidth: ".grid-item"
                }
            });
        });
    }
    /*====== SidebarSearch ======*/
    function sidebarSearch() {
        var searchTrigger = $(".search-active"),
            endTriggersearch = $(".search-close"),
            container = $(".main-search-active");
        searchTrigger.on("click", function (e) {
            e.preventDefault();
            container.addClass("search-visible");
        });
        endTriggersearch.on("click", function () {
            container.removeClass("search-visible");
        });
    }
    sidebarSearch();
    /*====== Sidebar menu Active ======*/
    function mobileHeaderActive() {
        var navbarTrigger = $(".burger-icon"),
            endTrigger = $(".mobile-menu-close"),
            container = $(".mobile-header-active"),
            wrapper4 = $("body");
        wrapper4.prepend('<div class="body-overlay-1"></div>');
        navbarTrigger.on("click", function (e) {
            navbarTrigger.toggleClass("burger-close");
            e.preventDefault();
            container.toggleClass("sidebar-visible");
            wrapper4.toggleClass("mobile-menu-active");
            window.scrollTo(0, 0);
        });
        endTrigger.on("click", function () {
            container.removeClass("sidebar-visible");
            wrapper4.removeClass("mobile-menu-active");
        });
        $(".close-mobile").on("click", function () {
            container.removeClass("sidebar-visible");
            wrapper4.removeClass("mobile-menu-active");
            navbarTrigger.removeClass("burger-close");
        });
        $(".body-overlay-1").on("click", function () {
            container.removeClass("sidebar-visible");
            wrapper4.removeClass("mobile-menu-active");
            navbarTrigger.removeClass("burger-close");
        });
    }
    mobileHeaderActive();
    /*---------------------
        Mobile menu active
    ------------------------ */
    var $offCanvasNav = $(".mobile-menu"),
        $offCanvasNavSubMenu = $offCanvasNav.find(".sub-menu");
    $offCanvasNavSubMenu.parent().append('<span class="menu-expand"></span>');

    /*Category Sub Menu Toggle*/
    $offCanvasNav.on("click", "li a, li .menu-expand", function (e) {
        var $this = $(this);
        if (
            $this
                .parent()
                .attr("class")
                .match(/\b(menu-item-has-children|has-children|has-sub-menu)\b/) &&
            ($this.attr("href") === "#" || $this.hasClass("menu-expand"))
        ) {
            e.preventDefault();
            if ($this.siblings("ul").hasClass(".menu-show")) {
                console.log(1);
                $(".box-head-1").show();
                $(".box-head-2").hide();
                $this.parent("li").removeClass("active");
                $this.siblings("ul").removeClass("menu-show");
            } else {
                console.log(2);
                $(".box-head-1").hide();
                $(".box-head-2").show();
                $this.parent("li").addClass("active");
                $this.closest("li").siblings("li").removeClass("active").find("li").removeClass("active");
                $this.siblings("ul").addClass("menu-show");
            }
        }
    });
    $(".back-mobile").on("click", function () {
        $(".box-head-1").show();
        $(".box-head-2").hide();
        $(".sub-menu").removeClass("menu-show");
    });
    /* --- SwiperJS --- */
    $(".swiper-banner").each(function () {
        var swiper_banner_items = new Swiper(this, {
            slidesPerView: 1,
            loop: true,
            navigation: {
                nextEl: ".swiper-button-next-banner",
                prevEl: ".swiper-button-prev-banner"
            },
            pagination: {
                el: ".swiper-pagination-banner",
                clickable: true
            },
            autoplay: {
                delay: 10000
            }
        });
    });
    $(".swiper-1-item").each(function () {
        var swiper_1_items = new Swiper(this, {
            slidesPerView: 1,
            loop: true,
            navigation: {
                nextEl: ".swiper-button-next-group-1",
                prevEl: ".swiper-button-prev-group-1"
            },
            pagination: {
                el: ".swiper-pagination-group-1",
                clickable: true
            },
            autoplay: {
                delay: 10000
            }
        });
    });
    $(".swiper-auto").each(function () {
        var swiper_auto_items = new Swiper(this, {
            slidesPerView: "auto",
            spaceBetween: 30,
            slidesPerGroup: 1,
            loop: true,
            navigation: {
                nextEl: ".swiper-button-next-group-auto",
                prevEl: ".swiper-button-prev-group-auto"
            },
            pagination: {
                el: ".swiper-pagination-auto",
                clickable: true
            },
            autoplay: {
                delay: 10000
            },
            on: {
                beforeInit: function () {
                    // set padding left slide fleet
                    var leftTitle = 0;
                    var titleFleet = $(".title-left");
                    if (titleFleet.length > 0) {
                        leftTitle = titleFleet.offset().left;
                    }
                    if ($(".box-slide-padding-left").length > 0) {
                        $(".box-slide-padding-left").css("padding-left", leftTitle + "px");
                    }
                }
            }
        });
    });

    $(".swiper-popular-product").each(function () {
        var swiper_popular_product = new Swiper(this, {
            spaceBetween: 30,
            slidesPerView: 4,
            slidesPerGroup: 1,
            loop: false,
            touchEventsTarget: "cardInfo",
            allowTouchMove: true,
            navigation: {
                nextEl: ".swiper-button-next-popular-product",
                prevEl: ".swiper-button-prev-popular-product"
            },
            pagination: {
                el: ".swiper-pagination-popular-product-page",
                clickable: true
            },
            scrollbar: {
                el: ".swiper-pagination-popular-product",
                draggable: true
            },
            autoplay: false,
            breakpoints: {
                1399: {
                    slidesPerView: 4
                },
                800: {
                    slidesPerView: 3
                },
                500: {
                    slidesPerView: 2
                },
                400: {
                    slidesPerView: 1
                },
                350: {
                    slidesPerView: 1
                },
                150: {
                    slidesPerView: 1
                }
            },
            on: {
                afterInit: function () {
                    initSwiperProduct();
                }
            }
        });
    });

    $(".swiper-scrollbar-4-items").each(function () {
        var swiper_4_product = new Swiper(this, {
            spaceBetween: 30,
            slidesPerView: 4,
            slidesPerGroup: 1,
            loop: false,
            touchEventsTarget: "cardInfo",
            allowTouchMove: true,
            navigation: {
                nextEl: ".swiper-button-next-popular-product",
                prevEl: ".swiper-button-prev-popular-product"
            },
            pagination: {
                el: ".swiper-pagination-popular-product-page",
                clickable: true
            },
            scrollbar: {
                el: ".swiper-pagination-popular-product",
                draggable: true
            },
            autoplay: false,
            breakpoints: {
                1399: {
                    slidesPerView: 4
                },
                1100: {
                    slidesPerView: 4
                },
                800: {
                    slidesPerView: 3
                },
                500: {
                    slidesPerView: 2
                },
                400: {
                    slidesPerView: 1
                },
                350: {
                    slidesPerView: 1
                },
                150: {
                    slidesPerView: 1
                }
            },
            on: {
                beforeInit: function () {
                    // set padding left slide fleet
                    var leftTitle = 0;
                    var titleFleet = $(".container");
                    if (titleFleet.length > 0) {
                        leftTitle = titleFleet.offset().left + 15;
                    }
                    if ($(".container-slider-padding").length > 0) {
                        $(".container-slider-padding").css("padding-left", leftTitle + "px");
                    }
                }
            }
        });
    });

    $(".swiper-scrollbar-4-items-2").each(function () {
        var swiper_4_product_2 = new Swiper(this, {
            spaceBetween: 30,
            slidesPerView: 4,
            slidesPerGroup: 1,
            loop: false,
            touchEventsTarget: "cardInfo",
            allowTouchMove: true,
            navigation: {
                nextEl: ".swiper-button-next-scrollbar-product",
                prevEl: ".swiper-button-prev-scrollbar-product"
            },
            pagination: {
                el: ".swiper-pagination-scrollbar-product-page",
                clickable: true
            },
            scrollbar: {
                el: ".swiper-pagination-scrollbar-product",
                draggable: true
            },
            autoplay: false,
            breakpoints: {
                1399: {
                    slidesPerView: 4
                },
                1100: {
                    slidesPerView: 4
                },
                800: {
                    slidesPerView: 3
                },
                500: {
                    slidesPerView: 2
                },
                400: {
                    slidesPerView: 1
                },
                350: {
                    slidesPerView: 1
                },
                150: {
                    slidesPerView: 1
                }
            },
            on: {
                beforeInit: function () {
                    // set padding left slide fleet
                    var leftTitle = 0;
                    var titleFleet = $(".container");
                    if (titleFleet.length > 0) {
                        leftTitle = titleFleet.offset().left + 15;
                    }
                    if ($(".container-slider-padding").length > 0) {
                        $(".container-slider-padding").css("padding-left", leftTitle + "px");
                    }
                }
            }
        });
    });

    $(".swiper-scrollbar-5-items").each(function () {
        var swiper_scrollbar_5_product = new Swiper(this, {
            spaceBetween: 30,
            slidesPerView: 5,
            slidesPerGroup: 1,
            loop: false,
            touchEventsTarget: "cardInfo",
            allowTouchMove: true,
            navigation: {
                nextEl: ".swiper-button-next-scrollbar-product",
                prevEl: ".swiper-button-prev-scrollbar-product"
            },
            pagination: {
                el: ".swiper-pagination-scrollbar-product-page",
                clickable: true
            },
            scrollbar: {
                el: ".swiper-pagination-scrollbar-product",
                draggable: true
            },
            autoplay: false,
            breakpoints: {
                1399: {
                    slidesPerView: 5
                },
                1100: {
                    slidesPerView: 4
                },
                800: {
                    slidesPerView: 3
                },
                500: {
                    slidesPerView: 2
                },
                400: {
                    slidesPerView: 1
                },
                350: {
                    slidesPerView: 1
                },
                150: {
                    slidesPerView: 1
                }
            },
            on: {
                beforeInit: function () {
                    // set padding left slide fleet
                    var leftTitle = 0;
                    var titleFleet = $(".container");
                    if (titleFleet.length > 0) {
                        leftTitle = titleFleet.offset().left + 15;
                    }
                    if ($(".container-slider-padding").length > 0) {
                        $(".container-slider-padding").css("padding-left", leftTitle + "px");
                    }
                }
            }
        });
    });
    $(".swiper-scrollbar-5-items-2").each(function () {
        var swiper_scrollbar_5_product = new Swiper(this, {
            spaceBetween: 30,
            slidesPerView: 5,
            slidesPerGroup: 1,
            // initialSlide: 1,
            loop: false,
            touchEventsTarget: "cardInfo",
            allowTouchMove: true,
            navigation: {
                nextEl: ".swiper-button-next-scrollbar-product-2",
                prevEl: ".swiper-button-prev-scrollbar-product-2"
            },
            pagination: {
                el: ".swiper-pagination-scrollbar-product-page-2",
                clickable: true
            },
            scrollbar: {
                el: ".swiper-pagination-scrollbar-product-2",
                draggable: true
            },
            autoplay: false,
            breakpoints: {
                1399: {
                    slidesPerView: 5
                },
                1100: {
                    slidesPerView: 4
                },
                800: {
                    slidesPerView: 3
                },
                500: {
                    slidesPerView: 2
                },
                400: {
                    slidesPerView: 1
                },
                350: {
                    slidesPerView: 1
                },
                150: {
                    slidesPerView: 1
                }
            },
            on: {
                beforeInit: function () {
                    // set padding left slide fleet
                    var leftTitle = 0;
                    var titleFleet = $(".container");
                    if (titleFleet.length > 0) {
                        leftTitle = titleFleet.offset().left + 15;
                    }
                    if ($(".container-slider-padding").length > 0) {
                        $(".container-slider-padding").css("padding-left", leftTitle + "px");
                    }
                }
            }
        });
    });

    $(".swiper-group-4").each(function () {
        var swiper_4_fleet = new Swiper(this, {
            spaceBetween: 30,
            slidesPerView: 4,
            slidesPerGroup: 1,
            loop: true,
            navigation: {
                nextEl: ".swiper-button-next-fleet-4",
                prevEl: ".swiper-button-prev-fleet-4"
            },
            pagination: {
                el: ".swiper-pagination-fleet-4",
                clickable: true
            },
            autoplay: {
                delay: 10000
            },
            breakpoints: {
                1399: {
                    slidesPerView: 4
                },
                800: {
                    slidesPerView: 3
                },
                500: {
                    slidesPerView: 2
                },
                400: {
                    slidesPerView: 1
                },
                350: {
                    slidesPerView: 1
                },
                150: {
                    slidesPerView: 1
                }
            }
        });
    });
    $(".swiper-group-5-items").each(function () {
        var swiper_5_items = new Swiper(this, {
            spaceBetween: 30,
            slidesPerView: 5,
            slidesPerGroup: 1,
            loop: true,
            navigation: {
                nextEl: ".swiper-button-next-group-5-items",
                prevEl: ".swiper-button-prev-group-5-items"
            },
            pagination: {
                el: ".swiper-pagination-group-5-items",
                clickable: true
            },
            autoplay: {
                delay: 10000
            },
            breakpoints: {
                1399: {
                    slidesPerView: 5
                },
                1100: {
                    slidesPerView: 4
                },
                800: {
                    slidesPerView: 3
                },
                500: {
                    slidesPerView: 2
                },
                400: {
                    slidesPerView: 1
                },
                350: {
                    slidesPerView: 1
                },
                150: {
                    slidesPerView: 1
                }
            },
            on: {
                beforeInit: function () {
                    // set padding left slide fleet
                    var leftTitle = 0;
                    var titleFleet = $(".container");
                    if (titleFleet.length > 0) {
                        leftTitle = titleFleet.offset().left + 15;
                    }
                    if ($(".container-slider-padding").length > 0) {
                        $(".container-slider-padding").css("padding-left", leftTitle + "px");
                    }
                }
            }
        });
    });
    $(".swiper-group-center-items").each(function () {
        var swiper_center_items = new Swiper(this, {
            spaceBetween: 30,
            slidesPerView: 4,
            centeredSlides: 1,
            centeredSlidesBounds: 1,
            slidesPerGroup: 1,
            loop: true,
            navigation: {
                nextEl: ".swiper-button-next-group-center-items",
                prevEl: ".swiper-button-prev-group-center-items"
            },
            pagination: {
                el: ".swiper-pagination-group-center-items",
                clickable: true
            },
            autoplay: {
                delay: 10000
            },
            breakpoints: {
                1399: {
                    slidesPerView: 4
                },
                1100: {
                    slidesPerView: 3
                },
                800: {
                    slidesPerView: 2
                },
                500: {
                    slidesPerView: 2
                },
                400: {
                    slidesPerView: 1
                },
                350: {
                    slidesPerView: 1
                },
                150: {
                    slidesPerView: 1
                }
            }
        });
    });
    $(".swiper-group-4-category").each(function () {
        var swiper_4_fleet = new Swiper(this, {
            spaceBetween: 5,
            slidesPerView: 4,
            slidesPerGroup: 1,
            loop: true,
            navigation: {
                nextEl: ".swiper-button-next-cat-4",
                prevEl: ".swiper-button-prev-cat-4"
            },
            pagination: {
                el: ".swiper-pagination-cat-4",
                clickable: true
            },
            autoplay: {
                delay: 10000
            },
            breakpoints: {
                1399: {
                    slidesPerView: 4
                },
                800: {
                    slidesPerView: 3
                },
                500: {
                    slidesPerView: 2
                },
                400: {
                    slidesPerView: 1
                },
                350: {
                    slidesPerView: 1
                },
                150: {
                    slidesPerView: 1
                }
            },
            on: {
                beforeInit: function () {
                    // set padding left slide fleet
                    var leftTitle = 0;
                    var titleFleet = $(".container");
                    if (titleFleet.length > 0) {
                        leftTitle = titleFleet.offset().left + 15;
                    }
                    if ($(".container-slider-padding").length > 0) {
                        $(".container-slider-padding").css("padding-left", leftTitle + "px");
                    }
                }
            }
        });
    });
    $(".swiper-3-items").each(function () {
        var swiper_3_items = new Swiper(this, {
            spaceBetween: 30,
            slidesPerView: 3,
            slidesPerGroup: 1,
            loop: true,
            navigation: {
                nextEl: ".swiper-button-next-items-3",
                prevEl: ".swiper-button-prev-items-3"
            },
            pagination: {
                el: ".swiper-pagination-items-3",
                clickable: true
            },
            autoplay: {
                delay: 10000
            },
            breakpoints: {
                1399: {
                    slidesPerView: 3
                },
                800: {
                    slidesPerView: 3
                },
                550: {
                    slidesPerView: 2
                },
                450: {
                    slidesPerView: 1
                },
                350: {
                    slidesPerView: 1
                },
                150: {
                    slidesPerView: 1
                }
            }
        });
    });
    $(".swiper-2-items").each(function () {
        var swiper_2_items = new Swiper(this, {
            spaceBetween: 30,
            slidesPerView: 2,
            slidesPerGroup: 1,
            loop: true,
            navigation: {
                nextEl: ".swiper-button-next-items-2",
                prevEl: ".swiper-button-prev-items-2"
            },
            pagination: {
                el: ".swiper-pagination-items-2",
                clickable: true
            },
            autoplay: {
                delay: 10000
            },
            breakpoints: {
                1399: {
                    slidesPerView: 2
                },
                800: {
                    slidesPerView: 2
                },
                550: {
                    slidesPerView: 1
                },
                450: {
                    slidesPerView: 1
                },
                350: {
                    slidesPerView: 1
                },
                150: {
                    slidesPerView: 1
                }
            }
        });
    });
    $(".swiper-6-items").each(function () {
        var swiper_6_fleet = new Swiper(this, {
            spaceBetween: 30,
            slidesPerView: 6,
            slidesPerGroup: 1,
            loop: true,
            navigation: {
                nextEl: ".swiper-button-next-6",
                prevEl: ".swiper-button-prev-6"
            },
            pagination: {
                el: ".swiper-pagination-6",
                clickable: true
            },
            autoplay: {
                delay: 10000
            },
            breakpoints: {
                1399: {
                    slidesPerView: 6
                },
                800: {
                    slidesPerView: 4
                },
                500: {
                    slidesPerView: 3
                },
                400: {
                    slidesPerView: 2
                },
                350: {
                    slidesPerView: 1
                },
                150: {
                    slidesPerView: 1
                }
            }
        });
    });

    // dropdown location
    $(".dropdown-location").on("click", function (e) {
        $(".box-dropdown-location").fadeOut();
        var _parent = $(this).parents(".search-inputs");
        var _dropdownLocation = _parent.find(".box-dropdown-location");
        if (_dropdownLocation.css("display") == "none") {
            _dropdownLocation.fadeIn();
        }
    });
    $(".item-location").on("click", function () {
        var title = $(this).find(".title-location").html();
        var _parent = $(this).parents(".search-inputs");
        _parent.find(".dropdown-location").val(title);
    });

    //Dropdown selected item
    $(".dropdown-menu > li a").on("click", function (e) {
        e.preventDefault();
        $(this)
            .parents(".dropdown")
            .find(".btn span")
            .html($(this).html() + "");
        $(this).parents(".dropdown").find(".btn").val($(this).data("value"));
    });

    // Video popup
    if ($(".popup-youtube").length) {
        $(".popup-youtube").magnificPopup({
            type: "iframe",
            mainClass: "mfp-fade",
            removalDelay: 160,
            preloader: false,
            fixedContentPos: false
        });
    }

    /*------ Timer Countdown ----*/
    $("[data-countdown]").each(function () {
        var $this = $(this),
            finalDate = $(this).data("countdown");
        $this.countdown(finalDate, function (event) {
            $(this).html(event.strftime("" + '<span class="countdown-section"><span class="countdown-amount font-sm-bold lh-16">%D</span><span class="countdown-period lh-14 font-xs"> days </span></span>' + '<span class="countdown-section"><span class="countdown-amount font-sm-bold lh-16">%H</span><span class="countdown-period font-xs lh-14"> hour </span></span>' + '<span class="countdown-section"><span class="countdown-amount font-sm-bold lh-16">%M</span><span class="countdown-period font-xs lh-14"> min </span></span>' + '<span class="countdown-section"><span class="countdown-amount font-sm-bold lh-16">%S</span><span class="countdown-period font-xs lh-14"> sec </span></span>'));
        });
    });

    //Mobile left sideba
    function mobileLeftSidebar() {
        var width = $(window).width();
        if (width < 992) {
            $(".menu-texts li.has-children > a").removeAttr("href");
            $(".menu-texts li.has-children > a").on("click", function (e) {
                $(this).parent().toggleClass("submenu-open");
                $(this).parent().siblings().removeClass("submenu-open");
            });
        }
    }
    mobileLeftSidebar();

    $(document).on("click", function (event) {
        var $trigger = $(".box-dropdown-cart");
        var $triggerSearch = $(".box-search-top");
        if ($triggerSearch !== event.target && !$triggerSearch.has(event.target).length) {
            $(".form-search-top").slideUp();
        }
        if ($trigger !== event.target && !$trigger.has(event.target).length) {
            $(".dropdown-account").removeClass("dropdown-open");
            $(".dropdown-cart").removeClass("dropdown-open");
        }
        var location = $(".dropdown-location");
        if (!location.is(event.target) && location.has(event.target).length === 0) {
            $(".box-dropdown-location").fadeOut();
        }
    });

    $(".icon-account").on("click", function () {
        $(".dropdown-account").toggleClass("dropdown-open");
    });

    $(".icon-cart").on("click", function () {
        $(".dropdown-cart").toggleClass("dropdown-open");
    });

    // SLick
    $(".product-image-slider-1").slick({
        slidesToShow: 1,
        slidesToScroll: 1,
        arrows: true,
        fade: false,
        asNavFor: ".slider-nav-thumbnails-1",
        prevArrow: '<button type="button" class="slick-prev"></button>',
        nextArrow: '<button type="button" class="slick-next"></button>'
    });

    $(".slider-nav-thumbnails-1").slick({
        slidesToShow: 5,
        slidesToScroll: 1,
        asNavFor: ".product-image-slider-1",
        dots: false,
        focusOnSelect: true,
        vertical: true,
        prevArrow: '<button type="button" class="slick-prev"><svg class="w-6 h-6 icon-16" fill="none" stroke="currentColor" viewbox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg></button>',
        nextArrow: '<button type="button" class="slick-next"><svg class="w-6 h-6 icon-16" fill="none" stroke="currentColor" viewbox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg></button>'
    });

    $(".product-image-slider-2").slick({
        slidesToShow: 1,
        slidesToScroll: 1,
        arrows: true,
        fade: false,
        asNavFor: ".slider-nav-thumbnails-2",
        prevArrow: '<button type="button" class="slick-prev"></button>',
        nextArrow: '<button type="button" class="slick-next"></button>'
    });
    $(".slider-nav-thumbnails-2").slick({
        slidesToShow: 5,
        slidesToScroll: 1,
        asNavFor: ".product-image-slider-2",
        dots: false,
        focusOnSelect: true,
        vertical: false,
        prevArrow: '<button type="button" class="slick-prev"><svg class="w-6 h-6 icon-16" fill="none" stroke="currentColor" viewbox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg></button>',
        nextArrow: '<button type="button" class="slick-next"><svg class="w-6 h-6 icon-16" fill="none" stroke="currentColor" viewbox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg></button>'
    });

    $(".product-image-slider-3").slick({
        slidesToShow: 1,
        slidesToScroll: 1,
        arrows: true,
        fade: false,
        prevArrow: '<button type="button" class="slick-prev"></button>',
        nextArrow: '<button type="button" class="slick-next"></button>'
    });

    $(".product-image-slider-4").slick({
        slidesToShow: 2,
        slidesToScroll: 2,
        arrows: true,
        fade: false,
        prevArrow: '<button type="button" class="slick-prev"></button>',
        nextArrow: '<button type="button" class="slick-next"></button>'
    });

    $(".product-image-slider-5").slick({
        slidesToShow: 1,
        slidesToScroll: 1,
        arrows: true,
        fade: false,
        asNavFor: ".slider-nav-thumbnails-5",
        prevArrow: '<button type="button" class="slick-prev"></button>',
        nextArrow: '<button type="button" class="slick-next"></button>'
    });
    $(".slider-nav-thumbnails-5").slick({
        slidesToShow: 4,
        slidesToScroll: 1,
        asNavFor: ".product-image-slider-5",
        dots: false,
        focusOnSelect: true,
        vertical: false,
        prevArrow: '<button type="button" class="slick-prev"><svg class="w-6 h-6 icon-16" fill="none" stroke="currentColor" viewbox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg></button>',
        nextArrow: '<button type="button" class="slick-next"><svg class="w-6 h-6 icon-16" fill="none" stroke="currentColor" viewbox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg></button>'
    });

    $(".list-terms li a").on("click", function (e) {
        e.preventDefault();
        var id = $(this).attr("href");
        var _top = $(id).offset().top - 90;
        $("html,body").animate({ scrollTop: _top }, 500);
    });
    if ($(".swiper-4-items").length > 0) {
        initSwiper4Items(".swiper-4-items", ".swiper-button-prev-collection", ".swiper-button-next-collection", ".swiper-pagination-collection");
    }
    if ($(".swiper-4-products").length > 0) {
        initSwiper4Items(".swiper-4-products", ".swiper-button-prev-collection", ".swiper-button-next-collection", ".swiper-pagination-collection");
    }
    initSwiper6Items(".swiper-6-items", ".swiper-button-prev-6", ".swiper-button-next-6", ".swiper-pagination-6");
    // init var swiper
    var swiper_1 = null;
    var swiper_2 = null;
    var items_number = $(".nav-tabs li button").attr("data-items");
    if (items_number) initSwiperTab(1, items_number);
    if (items_number) initSwiperTabScrollBar(1, items_number);

    // tab event show
    $('button[data-bs-toggle="tab"]').on("shown.bs.tab", function (e) {
        if (swiper_1) {
            swiper_1.destroy();
        }
        if (swiper_2) {
            swiper_2.destroy();
        }
        var _tab = $(e.target).attr("data-bs-target");
        var idx = $(e.target).data("index");
        var _items = $(e.target).data("items");
        swiper_1 = initSwiperTab(idx, _items);
        swiper_2 = initSwiperTabScrollBar(idx, _items);
    });

    $(".item-collapse").on("click", function () {
        var _parent = $(this).parents(".block-filter");
        if (_parent.find(".box-collapse").css("display") == "none") {
            $(this).removeClass("collapsed-item");
            _parent.find(".box-collapse").slideDown();
        } else {
            $(this).addClass("collapsed-item");
            _parent.find(".box-collapse").slideUp();
        }
    });
    $(".list-colors li").on("click", function () {
        $(".list-colors li").removeClass("active");
        $(".list-colors .box-colors .item-color").removeClass("active");
        $(this).addClass("active");
    });
    $(".box-colors .item-color").on("click", function () {
        $(".box-colors .item-color").removeClass("active");
        $(this).addClass("active");
    });
    $(".list-sizes .item-size").on("click", function () {
        $(".list-sizes .item-size").removeClass("active");
        $(this).addClass("active");
    });
    $(".close-tag").on("click", function (e) {
        e.preventDefault();
        var _btn = $(".block-ele-filter a.btn-tag-filter");
        if (_btn.length == 1) {
            $(".box-your-filter").hide();
        }
        $(this).parent("a").remove();
    });
    $(".clear-filter").on("click", function (e) {
        e.preventDefault();
        $(".block-ele-filter a.btn-tag-filter").remove();
        $(".box-your-filter").hide();
    });
    $(".left-filter .btn-open-filter, .btn-open-filter-click").on("click", function (e) {
        e.preventDefault();
        if ($(".block-filter-canvas").length == 0) {
            if ($(".block-filter-middle").css("display") == "none") {
                $(".block-filter-middle").slideDown();
            } else {
                $(".block-filter-middle").slideUp();
            }
        } else {
            if (!$(".block-filter-canvas").hasClass("active")) {
                $(".wrapper-overlay").show();
                $(".block-filter-canvas").show();
                $(".block-filter-canvas").addClass("active");
            } else {
                $(".wrapper-overlay").hide();
                $(".block-filter-canvas").hide();
                $(".block-filter-canvas").removeClass("active");
            }
        }
    });

    $(".show-sm .btn-open-filter").on("click", function (e) {
        e.preventDefault();
        if ($(".box-filters-sidebar").length > 0) {
            if (!$(".box-filters-sidebar").hasClass("active")) {
                $(".wrapper-overlay").show();
                $(".box-filters-sidebar").addClass("active");
            } else {
                $(".wrapper-overlay").hide();
                $(".box-filters-sidebar").removeClass("active");
            }
        }
        if ($(".block-filter-canvas").length > 0) {
            if (!$(".block-filter-canvas").hasClass("active")) {
                $(".wrapper-overlay").show();
                $(".block-filter-canvas").show();
                $(".block-filter-canvas").addClass("active");
            } else {
                $(".wrapper-overlay").hide();
                $(".block-filter-canvas").hide();
                $(".block-filter-canvas").removeClass("active");
            }
        }
    });

    $(".wrapper-overlay").on("click", function (e) {
        $(".wrapper-overlay").hide();
        $(".wrapper-popup").hide();
        $(".wrapper-popup").removeClass("active");
        $(".box-filters-sidebar").removeClass("active");
    });
    $(".view-type").on("click", function (e) {
        e.preventDefault();
        $(".view-type").removeClass("active");
        $(this).addClass("active");
        var _col = $(this).data("col");
        var _class = "grid-col-" + _col;
        $(".box-list-products").removeClass("grid-col-2");
        $(".box-list-products").removeClass("grid-col-3");
        $(".box-list-products").removeClass("grid-col-4");
        $(".box-list-products").removeClass("grid-col-5");
        $(".box-list-products").addClass(_class);
    });

    $(".arrow-down").on("click", function (e) {
        var _parent = $(this).parent("li");
        if (_parent.find("ul").css("display") == "none") {
            _parent.find("ul").slideDown();
        } else {
            _parent.find("ul").slideUp();
        }
    });

    $(".dropdown-menu-filter").click(function (e) {
        e.stopPropagation();
    });

    //Off canvas Search
    $(".btn-close-popup, .box-search-overlay").on("click", function (e) {
        $(".box-search-wrapper").removeClass("active");
        $(".box-popup-search").css("visibility", "hidden");
    });

    $("a.account-icon.search").on("click", function (e) {
        $(".box-popup-search").css("visibility", "visible");
        $(".box-search-wrapper").addClass("active");
    });

    //Off canvas Cart
    $("a.account-icon.cart").on("click", function (e) {
        $(".box-popup-cart").css("visibility", "visible");
        $(".box-cart-wrapper").addClass("active");
    });

    $(".btn-close-popup, .box-cart-overlay").on("click", function (e) {
        $(".box-cart-wrapper").removeClass("active");
        $(".box-popup-cart").css("visibility", "hidden");
    });

    //Off canvas Wishlist
    $("a.account-icon.wishlist").on("click", function (e) {
        $(".box-popup-wishlist").css("visibility", "visible");
        $(".box-wishlist-wrapper").addClass("active");
    });

    $(".btn-close-popup, .box-wishlist-overlay").on("click", function (e) {
        $(".box-wishlist-wrapper").removeClass("active");
        $(".box-popup-wishlist").css("visibility", "hidden");
    });

     //Popup Account
    $(".btn-close-popup-account, .box-account-overlay").on("click", function (e) {
        $(".box-popup-account").hide();
    });
    $("a.account-icon.account").on("click", function (e) {
        $(".box-popup-account").show();
    });

    $(".button-tab").on("click", function (e) {
        $(".button-tab").removeClass("active");
        $(this).addClass("active");
        if ($(this).hasClass("btn-for-login")) {
            $(".form-login").show();
            $(".form-register").hide();
        }
        if ($(this).hasClass("btn-for-signup")) {
            $(".form-login").hide();
            $(".form-register").show();
        }
    });
    $(".login-now").on("click", function (e) {
        $(".button-tab").removeClass("active");
        $(".btn-for-login").addClass("active");
        $(".form-login").show();
        $(".form-register").hide();
        $(".form-account-info").show();
        $(".form-password-info").hide();
    });
    $(".buttun-forgotpass").on("click", function (e) {
        e.preventDefault();
        $(".form-account-info").hide();
        $(".form-password-info").show();
    });

    // Product gallery
    GLightbox({
        selector: ".glightbox"
    });

    $(".btn-close-popup").on("click", function(e){
        e.preventDefault();
        $(".box-popup-preview").hide();
    });

    $(".preview-product").on("click", function (e) {
        e.preventDefault();
        $(".box-popup-preview").show();
        initSlidePreview();
    });
    var _container = $(".container").offset().left;
    $(".box-padding-left-banner").css('padding-left', ''+_container+'px');

    $(".form-comment input, .form-comment textarea, .form-comment select").focus(function () {
        $(this).parents(".form-group").addClass("focused");
    });

    $(".form-comment input, .form-comment textarea, .form-comment select").blur(function () {
        var inputValue = $(this).val();
        if (inputValue == "") {
            $(this).removeClass("filled");
            $(this).parents(".form-group").removeClass("focused");
        } else {
            $(this).addClass("filled");
        }
    });
    $(".form-comment input, .form-comment textarea, .form-comment select").each(function () {
        if (this.value) {
            $(this).parents(".form-group").addClass("focused");
            $(this).addClass("filled");
        }
    });
    $(".form-label").on("click", function(){
        $(this).next().focus();
    });
    $(".box-payment-method .list-radio .item-radio input").on("click", function(){
        var _parent = $(this).parents(".item-radio");
        $(".extra-info").removeClass("active");
        _parent.find(".extra-info").addClass("active");
    });

    $(".btn-remove-cart").on("click", function(e){
        e.preventDefault();
        $(this).parents(".item-cart").fadeOut(500, function(){
            $(this).remove();
        });
    });
})(jQuery);

function initSlidePreview() {
    $(".product-image-slider-preview").slick({
        slidesToShow: 1,
        slidesToScroll: 1,
        arrows: true,
        dots: true,
        fade: false,
        prevArrow: '<button type="button" class="slick-prev"></button>',
        nextArrow: '<button type="button" class="slick-next"></button>',
        customPaging: function (slider, i) {
            return '<a class="pager__item"></a>';
        }
    });
}
function initSwiperProduct() {
    $(".swiper-product").each(function () {
        var _lg = $(this).data("lg");
        var _md = $(this).data("md");
        var _sm = $(this).data("sm");
        var _xs = $(this).data("xs");
        var _btn_next = $(this).data("next");
        var _btn_prev = $(this).data("prev");
        var _btn_pagination = $(this).data("pagination");
        new Swiper(this, {
            spaceBetween: 0,
            slidesPerView: _lg,
            slidesPerGroup: 1,
            loop: true,
            navigation: {
                nextEl: _btn_next,
                prevEl: _btn_prev
            },
            pagination: {
                el: _btn_pagination,
                clickable: true
            },
            autoplay: {
                delay: 10000
            },
            breakpoints: {
                1399: {
                    slidesPerView: _lg
                },
                800: {
                    slidesPerView: _md
                },
                500: {
                    slidesPerView: _sm
                },
                400: {
                    slidesPerView: _xs
                },
                350: {
                    slidesPerView: _xs
                },
                150: {
                    slidesPerView: _xs
                }
            }
        });
    });
}
// Guza
var swiper_4_items = null;
function initSwiper4Items(elementor, prevEle, nextEle, pageEle) {
    if (swiper_4_items) {
        swiper_4_items.destroy();
    }
    swiper_4_items = new Swiper(elementor, {
        spaceBetween: 30,
        slidesPerView: 4,
        slidesPerGroup: 1,
        loop: true,
        navigation: {
            nextEl: nextEle,
            prevEl: prevEle
        },
        pagination: {
            el: pageEle,
            clickable: true
        },
        autoplay: {
            delay: 10000
        },
        breakpoints: {
            1399: {
                slidesPerView: 4
            },
            1100: {
                slidesPerView: 3
            },
            670: {
                slidesPerView: 2
            },
            575: {
                slidesPerView: 1
            },
            400: {
                slidesPerView: 1
            },
            350: {
                slidesPerView: 1
            },
            150: {
                slidesPerView: 1
            }
        },
        on: {
            afterInit: function () {
                // set padding left slide fleet
                var leftTitle = 0;
                var titleFleet = $(".container");
                if (titleFleet.length > 0) {
                    leftTitle = titleFleet.offset().left + 15;
                }
                if ($(".container-slider-padding").length > 0) {
                    $(".container-slider-padding").css("padding-left", leftTitle + "px");
                }
            }
        }
    });
}
var swiper_6_items = null;
function initSwiper6Items(elementor, prevEle, nextEle, pageEle) {
    if (swiper_6_items) {
        swiper_6_items.destroy();
    }
    swiper_6_items = new Swiper(elementor, {
        spaceBetween: 30,
        slidesPerView: 6,
        slidesPerGroup: 2,
        loop: true,
        navigation: {
            nextEl: nextEle,
            prevEl: prevEle
        },
        pagination: {
            el: pageEle,
            clickable: true
        },
        autoplay: {
            delay: 10000
        },
        breakpoints: {
            1399: {
                slidesPerView: 6
            },
            800: {
                slidesPerView: 4
            },
            500: {
                slidesPerView: 3
            },
            400: {
                slidesPerView: 2,
                slidesPerGroup: 1
            },
            350: {
                slidesPerView: 1,
                slidesPerGroup: 1
            },
            150: {
                slidesPerView: 1,
                slidesPerGroup: 1
            }
        }
    });
}
// Guza
function initSwiperTab(idx, number) {
    if ($(".swiper-tab-" + idx + "").length == 0) {
        return;
    }
    if (number > 1) {
        return new Swiper(".swiper-tab-" + idx + "", {
            spaceBetween: 30,
            slidesPerView: number,
            slidesPerGroup: 1,
            loop: true,
            navigation: {
                nextEl: ".swiper-button-next-tab-" + idx,
                prevEl: ".swiper-button-prev-tab-" + idx
            },
            pagination: {
                el: ".swiper-pagination-tab-" + idx,
                clickable: true
            },
            autoplay: {
                delay: 10000
            },
            breakpoints: {
                1399: {
                    slidesPerView: number
                },
                1100: {
                    slidesPerView: 3
                },
                670: {
                    slidesPerView: 2
                },
                575: {
                    slidesPerView: 2
                },
                400: {
                    slidesPerView: 1
                },
                350: {
                    slidesPerView: 1
                },
                150: {
                    slidesPerView: 1
                }
            },
            on: {
                afterInit: function () {
                    // set padding left slide fleet
                    var leftTitle = 0;
                    var titleFleet = $(".container");
                    if (titleFleet.length > 0) {
                        leftTitle = titleFleet.offset().left + 15;
                    }
                    if ($(".container-slider-padding-" + idx).length > 0) {
                        $(".container-slider-padding-" + idx).css("padding-left", leftTitle + "px");
                    }
                },
                beforeInit: function () {
                    $(".container-slider-padding-" + idx).css("padding-left", "");
                }
            }
        });
    } else {
        return new Swiper(".swiper-tab-" + idx + "", {
            spaceBetween: 30,
            slidesPerView: number,
            slidesPerGroup: 1,
            loop: true,
            navigation: {
                nextEl: ".swiper-button-next-tab-" + idx,
                prevEl: ".swiper-button-prev-tab-" + idx
            },
            pagination: {
                el: ".swiper-pagination-tab-" + idx,
                clickable: true
            },
            autoplay: {
                delay: 10000
            }
        });
    }
}

function initSwiperTabScrollBar(idx, number) {
    if ($(".swiper-tab-scrollbar-" + idx + "").length == 0) {
        return;
    }
    return new Swiper(".swiper-tab-scrollbar-" + idx + "", {
        spaceBetween: 30,
        slidesPerView: number,
        slidesPerGroup: 1,
        loop: false,
        allowTouchMove: true,
        navigation: {
            nextEl: ".swiper-button-next-tab-scrollbar-" + idx,
            prevEl: ".swiper-button-prev-tab-scrollbar-" + idx
        },
        pagination: {
            el: ".swiper-pagination-tab-scrollbar-" + idx,
            clickable: true
        },
        scrollbar: {
            el: ".swiper-pagination-scrollbar-" + idx,
            draggable: true
        },
        autoplay: false,
        breakpoints: {
            1399: {
                slidesPerView: number
            },
            1100: {
                slidesPerView: 4
            },
            870: {
                slidesPerView: 3
            },
            575: {
                slidesPerView: 2
            },
            400: {
                slidesPerView: 1
            },
            350: {
                slidesPerView: 1
            },
            150: {
                slidesPerView: 1
            }
        },
        on: {
            beforeInit: function () {
                // set padding left slide fleet
                var leftTitle = 0;
                var titleFleet = $(".container");
                if (titleFleet.length > 0) {
                    leftTitle = titleFleet.offset().left + 15;
                }
                if ($(".container-slider-padding").length > 0) {
                    $(".container-slider-padding").css("padding-left", leftTitle + "px");
                }
            }
        }
    });
}
//Perfect Scrollbar
if ($(".mobile-header-wrapper-inner").length) {
    const ps = new PerfectScrollbar(".mobile-header-wrapper-inner");
}
if ($(".scrollFilter").length > 0) {
    $(".scrollFilter").each(function(){
        new PerfectScrollbar(this);
    });
}

//Qty Up-Down
$('.detail-qty').each(function () {
    var qtyval = parseInt($(this).find(".qty-val").val(), 10);
    var $qtyInput = $(this).find(".qty-val");

    $(this).find('.plus').on('click', function (event) {
        event.preventDefault();
        qtyval = qtyval + 1;
        $qtyInput.val(qtyval);
    });

    $(this).find(".minus").on("click", function (event) {
        event.preventDefault();/*  */
        qtyval = Math.max(1, qtyval - 1);
        $qtyInput.val(qtyval);
    });
});
