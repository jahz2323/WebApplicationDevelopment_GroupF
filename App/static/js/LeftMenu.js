//Authors Jahziel
/*
    Left Menu code -
    This code is responsible for the left menu of the dashboard.
    It shows the menu when the mouse is on the left side of the screen
    and hides it when the mouse is outside the menu.
   The menu is hidden by default.
 */
$(document).ready(function () {
    console.log("LeftMenu.js loaded");

    const leftMenu = $('#left-menu');
    const mainContent = $('#main-content');

    // Initially the menu is hidden
    let isMenuVisible = false;


    // left menu css - hidden by default at -150px
    // if mouse pos x is > 170px, hide the menu else
    // show the menu
    function showMenu() {
        leftMenu.css('left', '0');
        mainContent.css('margin-left', '150px');
    }
    function hideMenu() {
        leftMenu.css('left', '-150px');
        mainContent.css('margin-left', '0');
    }

    mainContent.hover(function () {
        // console.log("main content hover");
        if (!isMenuVisible) {
            showMenu();
            isMenuVisible = true;
        }
    });

    //hide menu when mouse event is outside x 170, else show the dashboard menu
    //set boolean arg depending on the mouse position
    $(document).on('mousemove', function (e) {
        // Check if mouse is on the left side of the screen
        // console.log("PageX", e.pageX); //For debugging
        if (e.pageX < 170) {
            if (!isMenuVisible) {

                showMenu();
                isMenuVisible = true;
            }
        } else {
            if (isMenuVisible) {
                hideMenu();
                isMenuVisible = false;
            }
        }
    });
});
