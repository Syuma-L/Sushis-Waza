/* =============================================
   SUSHI WASA — Gestion du panier
   ============================================= */

let panier = [];
let panierOuvert = false;

// Charger le panier depuis localStorage au chargement de la page
window.addEventListener("DOMContentLoaded", () => {
  const panierSauvegarde = localStorage.getItem("panier");
  if (panierSauvegarde) {
    panier = JSON.parse(panierSauvegarde);
    afficherPanier();
  }
});

function sauvegarderPanier() {
  localStorage.setItem("panier", JSON.stringify(panier));
}

/* Ouvre / ferme le panneau panier */
function togglePanier() {
  panierOuvert = !panierOuvert;
  document.getElementById('panierPanel').classList.toggle('open', panierOuvert);
  document.getElementById('panierOverlay').classList.toggle('open', panierOuvert);
  document.body.style.overflow = panierOuvert ? 'hidden' : '';
}

/* Ajoute un article et donne un retour visuel sur le bouton */
function ajouterAuPanier(nom, prix, btn) {
  panier.push({ nom, prix, id: Date.now() });
  sauvegarderPanier();
  afficherPanier();

  btn.textContent = '✓ Ajouté !';
  btn.classList.add('added');
  setTimeout(() => {
    btn.textContent = '＋ Ajouter';
    btn.classList.remove('added');
  }, 1200);
}

/* Supprime un article par son identifiant unique */
function supprimerItem(id) {
  panier = panier.filter(item => item.id !== id);
  sauvegarderPanier();
  afficherPanier();
}

/* Met à jour l'affichage du panier (badge, liste, total) */
function afficherPanier() {
  const itemsEl   = document.getElementById('panierItems');
  const footerEl  = document.getElementById('panierFooter');
  const badge     = document.getElementById('badge');
  const totalEl   = document.getElementById('panierTotal');

  badge.textContent = panier.length;

  if (panier.length === 0) {
    itemsEl.innerHTML = `
      <div class="panier-empty">
        <div class="empty-icon">🍱</div>
        <p>Votre panier est vide.<br>Ajoutez des sushis !</p>
      </div>`;
    footerEl.style.display = 'none';
    return;
  }

  let total = 0;
  let html  = '';

  panier.forEach(item => {
    total += item.prix;
    html += `
      <div class="panier-item">
        <div>
          <div class="panier-item-name">${item.nom}</div>
          <div class="panier-item-prix">${item.prix}€</div>
        </div>
        <button class="panier-item-remove" onclick="supprimerItem(${item.id})">✕</button>
      </div>`;
  });

  itemsEl.innerHTML = html;
  totalEl.textContent = total + '€';
  footerEl.style.display = 'block';
}
