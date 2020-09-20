$(document).ready(function() {
    // Show sideNav
    $('.button-collapse').sideNav('show');
    // Hide sideNav
    $('.button-collapse').sideNav('hide');
    });


$(document).ready(() => {
    // SideNav Button Initialization
    $(".button-collapse").sideNav();
    // SideNav Scrollbar Initialization
    var sideNavScrollbar = document.querySelector('.custom-scrollbar');
    var ps = new PerfectScrollbar(sideNavScrollbar);
});

$(document).ready(() => {
    // SideNav Initialization
    $(".button-collapse").sideNav();
  
    new WOW().init();
  });