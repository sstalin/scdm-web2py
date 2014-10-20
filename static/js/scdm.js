"use strict";


$(document).ready(function () {
    var overlay = $(".overlay"),
        menuBtn = $("#menu-btn"),
        menuTray = $('.menu-tray');

    function toggleMenu() {
        if (overlay.hasClass('on')) {
            overlay.removeClass('on');
        } else {
            overlay.addClass('on');
        }
        if(menuTray.hasClass('on')){
            menuTray.removeClass('on');
        }else{
            menuTray.addClass('on');
        }

    }


    menuBtn.click(toggleMenu);
    overlay.click(toggleMenu);

});

