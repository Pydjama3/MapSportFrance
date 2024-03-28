var configList, count;


// on initie tout
$(function() {
    // récupération du <div> contenant l'ensemble des configurations
    configList = document.getElementById('config-list');

    // intialisation à 1, même s'il n'y a aucun élémet 
    // dans la liste car le compteur s'incrémente après
    // un ajout
    count = 1;
    console.log("Ready and running config manager!")

    // instance du Sortable module de la librairie Sortable.js 
    // (importée depuis homepage.html)
    // responnsable de la gestion des éléments de la liste
    // (ajout, suppression, etc...)
    Sortable.create(configList, {
        filter: '.locked',
        removeOnSpill: true,
        animation: 150,
        ghostClass: 'blue-background-class',
        onMove: function (evt) {
            if(evt.related.classList.contains("locked")){ 
                return false;
            }
        },
        onEnd: function (evt) {

        }
    });
});

function addItem(plotType){
    /**
     * Ajoute un élément à la liste des configurations
     * @param {string} plotType - type de graphique à ajouter: "file" ou "formula"
     */
    var newItem = document.createElement('div');
    newItem.className = 'list-group-item';

    if(plotType == "file"){
        newItem.innerHTML = `
        <div class="num">
            <p>
                №${count}<br>
                &nbsp;&nbsp;&nbsp;↳
            </p>
            <div class="form-group" class="display">
                <input type="checkbox" class="form-control" id="plots[${count}][display]" name="plots[${count}][display]" checked>
                <label for="plots[${count}][display]">Affichage sur la carte</label>
            </div>
            <input type="hidden" name="plots[${count}][id]" value="${count}">
            <input type="hidden" name="plots[${count}][type]" value="file">
        </div>
        <div class="config-container">
            <div class="form-group">
                <label for="plots[${count}][title]">Légende: </label>
                <input type="text" class="form-control" id="plots[${count}][title]" name="plots[${count}][title]" placeholder="Données sans titre (${count})" required>
            </div>
            <br>
            <div class="form-group">
                <label for="plots[${count}][file]">Fichier source (.csv): </label>
                <input type="text" class="form-control" id="plots[${count}][file]" name="plots[${count}][file]" required>
            </div>
            <br>
            <div class="form-group">
                <label for="plots[${count}][departments]">En-tête des départements:</label>
                <input type="text" class="form-control" placeholder="Département" id="plots[${count}][departments]" name="plots[${count}][departments]" required>
            </div>
            <br>
            <div class="form-group">
                <label for="plots[${count}][values]">En tête des valeurs: </label>
                <input type="text" class="form-control" placeholder="Valeurs" id="plots[${count}][values]" name="plots[${count}][values]" required>
            </div>
            <br>
            <div class="form-group">
                <label for="plots[${count}][color]">Couleur: </label>
                <input type="color" class="form-control" onchange="changeColor(this)" id="plots[${count}][color]" name="plots[${count}][color]" value="#ffffff" required>
            </div>    
        </div>`;
    } else {
        newItem.innerHTML = `
        <div class="num">
            <p>
                №${count}<br>
                &nbsp;&nbsp;&nbsp;↳
            </p>
            <div class="form-group" class="display">
                <input type="checkbox" class="form-control" id="plots[${count}][display]" name="plots[${count}][display]" checked>
                <label for="plots[${count}][display]">Affichage sur la carte</label>
            </div>
            <input type="hidden" name="plots[${count}][id]" value="${count}">
            <input type="hidden" name="plots[${count}][type]" value="formula">
        </div>
        <div class="config-container">
            <div class="form-group">
                <label for="plots[${count}][title]">Légende: </label>
                <input type="text" class="form-control" id="plots[${count}][title]" name="plots[${count}][title]" placeholder="Données sans titre (${count})" required>
            </div>
            <br>
            <div class="form-group">
                <label for="plots[${count}][formula]">Formule en Python (l'index correspond au numéro):</label>
                <input type="text" class="form-control" placeholder="Ex: V[${count}]*V[${count+1}], V[${count}]/100,..." id="plots[${count}][formula]" name="plots[${count}][formula]" required>
            </div>
            <br>
            <div class="form-group">
                <label for="plots[${count}][color]">Couleur: </label>
                <input type="color" class="form-control" onchange="changeColor(this)" id="plots[${count}][color]" name="plots[${count}][color]" value="#ffffff" required>
            </div>
        </div>`;
    }
    
    
    $("#adder").before(newItem);
    count += 1;
}


function changeColor(element){
    /**
     * Change la couleur de la police d'un élément de la configuration
     * pour que l'écriture ressorte toujours
     * @param {object} element - élément initiateur de l'évènement
     */
    color = element.value;
    element.parentElement.parentElement.parentElement.style.backgroundColor = color;
    
    const r = parseInt(color.substr(1,2), 16)
    const g = parseInt(color.substr(3,2), 16)
    const b = parseInt(color.substr(5,2), 16)
    let a = (r + g + b) / 3; // passage en niveau de gris
    
    element.parentElement.parentElement.parentElement.
        style.color = `rgb(${255-a}, ${255-a}, ${255-a})`; // inversion colorimétrique
}