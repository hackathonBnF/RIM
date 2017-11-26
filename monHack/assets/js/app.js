
  $(document).ready(function(){
    // the "href" attribute of the modal trigger must specify the modal ID that wants to be triggered
    $('.modal').modal();
    parser();
  });



(function($){
    $(function(){

        $('.button-collapse').sideNav();



    }); // end of document ready
})(jQuery); // end of jQuery name space

document.addEventListener('DOMContentLoaded', function(){
    let wrapper = document.getElementById('wrapper');
    let topLayer = wrapper.querySelector('.top');
    let handle = wrapper.querySelector('.handle');
    let skew = 0;
    let delta = 0;

    if(wrapper.className.indexOf('skewed') != -1){
        skew = 1000;
    }

    wrapper.addEventListener('mousemove', function(e){
        delta = (e.clientX - window.innerWidth / 2) * 0.5;

        handle.style.left = e.clientX + delta + 'px';

        topLayer.style.width= e.clientX + skew + delta + 'px';
    });
});

(function(d, s, id) {
var js, djs = d.getElementsByTagName(s)[0];
if (d.getElementById(id)) return;
js = d.createElement(s); js.id = id;
js.src = "https://e-cdns-files.dzcdn.net/js/widget/loader.js";
 djs.parentNode.insertBefore(js, djs);
}(document, "script", "deezer-widget-loader"));


const makeRequest = (function () {
    let httpRequest;
    if (window.XMLHttpRequest) {
        httpRequest = new XMLHttpRequest();
    }
    httpRequest.onreadystatechange = function () {
        console.log("say");
        if (httpRequest.readyState === XMLHttpRequest.DONE) {
                console.log("yipii");
            if (httpRequest.status === 200) {
                    console.log("yay");
            } else {
                console.log(httpRequest.status);
            }
        }
    };
    console.log("Now");
    let url = "data.bnf.fr";
    httpRequest.open("GET", url, true);
    httpRequest.send();
}());
const parser = (function (obj) {
    "use strict";
    let nomCompositeur;
    let dateOeuvre;
    let titreOeuvre;
    let sujetOeuvre;

    let pNom = document.createElement("p");
    pNom.textContent = nomCompositeur;

    let pDate = document.createElement("p");
    pDate.textContent = dateOeuvre;

    let pTitre = document.createElement("p");
    pTitre.textContent = titreOeuvre;

    let pSujet = document.createElement("p");
    pSujet.textContent = sujetOeuvre;

    let lecteur1 = document.createElement("audio");
    lecteur1.controls = true;
    lecteur1.src = "assets/musique/native10.flac";

    let lecteur2 = document.createElement("audio");
    lecteur2.controls = true;
    lecteur2.src = "assets/musique/native12.flac";

    document.getElementById("resultat").appendChild(pNom);
    document.getElementById("resultat").appendChild(pDate);
    document.getElementById("resultat").appendChild(pTitre);
    document.getElementById("resultat").appendChild(pSujet);

    document.getElementById("resultat").appendChild(lecteur1);
    document.getElementById("resultat").appendChild(lecteur2);

}());