/* Constants */
const bgFadeOut = [
	{opacity:'100%'},
	{opacity:'0%'}
];
const bgFadeIn = [
	{opacity:'0%'},
	{opacity:'100%'}
];
const fadeTiming = {
	duration: 250
};

/* Functions */
function displayTitle(title){
	document.getElementById("title").textContent = title;
}

function displayContent(content){
	document.getElementById("page").src = content;
}
	
function updateHeight(){
	// var heightOffset = 181;
	var heightOffset = 100;
	var nuHeight = window.innerHeight-heightOffset;

	document.getElementById('content').style.height = nuHeight+'px';
}

/* Initial execution */
updateHeight();

/* Events */
window.addEventListener("resize",updateHeight);

document.getElementById("homebtn").addEventListener("click",()=>{
	document.getElementById("pageTitle").animate(bgFadeOut,fadeTiming); 
	document.getElementById("page").animate(bgFadeOut,fadeTiming);
	displayTitle("About");
	displayContent("content/main/home.html")
	document.getElementById("pageTitle").animate(bgFadeIn,fadeTiming); 
	document.getElementById("page").animate(bgFadeIn,fadeTiming);
});
document.getElementById("projectbtn").addEventListener("click",()=>{
	document.getElementById("pageTitle").animate(bgFadeOut,fadeTiming);
	document.getElementById("page").animate(bgFadeOut,fadeTiming);
	displayTitle("Projects");
	displayContent("content/main/projects.html")
	document.getElementById("pageTitle").animate(bgFadeIn,fadeTiming); 
	document.getElementById("page").animate(bgFadeIn,fadeTiming)
});
document.getElementById("contactbtn").addEventListener("click",()=>{
	document.getElementById("pageTitle").animate(bgFadeOut,fadeTiming);
	document.getElementById("page").animate(bgFadeOut,fadeTiming);
	displayTitle("Contact");
	displayContent("content/main/contact.html")
	document.getElementById("pageTitle").animate(bgFadeIn,fadeTiming); 
	document.getElementById("page").animate(bgFadeIn,fadeTiming);

});