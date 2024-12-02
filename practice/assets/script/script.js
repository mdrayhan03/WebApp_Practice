var suboption = document.getElementsByClassName("suboption")
var drop = document.getElementsByClassName("fa-angle-down")
function expandFunction(ind) {
    if (suboption[ind].offsetHeight === 0) {
        suboption[ind].style.maxHeight = "500px" ;
        drop[ind].style.transform = "rotateX(180deg)" ;
    }
    else {
        suboption[ind].style.maxHeight = "0px" ;
        drop[ind].style.transform = "rotateX(0deg)" ;
    }
}