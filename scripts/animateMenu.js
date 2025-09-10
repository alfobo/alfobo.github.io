/* */
function getMousePosition(e){
    var bound = document.getElementById("aniMenu").getBoundingClientRect();
    var pos = [e.clientX - (bound.width*.5),(e.clientY-(bound.height*.5))*-1];
    return pos;
}

/* 
Get the degree of a circle based of the mouse's position. An offset of -130 
degree in order to better align with the mouse.
*/
function getDegree(pos){
    var rad = Math.atan2(pos[0],pos[1]);
    var deg = rad*(180/Math.PI)-130;
    return deg;
}

function rotateEye(e){
    var deg = getDegree(getMousePosition(e));
    document.getElementById("logoIMG").style.transform = 'rotate('+deg+'deg)';
}
