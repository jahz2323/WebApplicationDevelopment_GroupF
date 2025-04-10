$(document).ready(function () {
    console.log("LeftMenu.js loaded");

    const leftMenu = $('#left-menu');
    const mainContent = $('#main-content');

    // Initially the menu is hidden
    let isMenuVisible = false;

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

    //hide menu when mouse is outside x 170, else show the dashboard menu
    $(document).on('mousemove', function (e) {
        // Check if mouse is on the left side of the screen
        // console.log("PageX", e.pageX);
        if (e.pageX < 20) {
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
