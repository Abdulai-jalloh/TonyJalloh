
document.addEventListener('DOMContentLoaded', () => {
  const isIndex = document.body.classList.contains('home-page');
  // const isDetails = document.body.classList.contains('details-page');
  const alllands = document.body.classList.contains('AllLands');

  //the if statment on the index(home) page.html

  if (isIndex) {
    const container = document.querySelector('.lands-container');
    const searchInput = document.getElementById('search-location');
    const searchIcon = document.getElementById('search-Icon');
    const noResult = document.querySelector('.No-result')
    //store all lands for filtering later
    let allLands = [];
    // fetch and display lands 
    fetch('/static/land.json')
    .then(res => res.json())
    .then(lands => {
      allLands = lands;
      console.log(allLands);
      
      displayLands(lands.slice(0, 20));
    });

    //function to display land cards
    function displayLands (landsToDisplay) {
      // clear current list/lands
      if (landsToDisplay.length === 0) {
        noResult.style.display = 'block';
        return;
      }else{
        noResult.style.display = 'none';
    
      container.innerHTML = ''; 
      landsToDisplay.forEach(land => {
        container.innerHTML += `<div class="land-card"> 
                        
                                <img src="${land.mainimage}" alt="${land.title}">
                                <h4>Titre: ${land.title}</h4>
                                <p>Emplacement: ${land.location}</p>
                                <p>Prix: ${land.price}</p>
                                <a href="/land/${land.id}">Voir plus</a>
                                </div> `;   
                                
      });
    }
    
    }

    //Search By Location In the Home Code
    searchIcon.addEventListener('click', () => {
      const searchTerm = searchInput.value.trim().toLowerCase();
      const  Filterlands = allLands.filter(land => 
      land.location?.toLowerCase().includes(searchTerm)
      );
    displayLands(Filterlands);
    })
    
  }


  // the if statment in the details page
  // if (isDetails) {

  //   let allLands
  //   const params = new URLSearchParams(window.location.search);
  //   const landID = parseInt( params.get('id'));
  //   fetch('/static/land.json').then(res => res.json())
  //   .then(lands => {
  //     allLands = lands;
  //     const land = lands.find(i => i.id == landID);
  //     const container = document.querySelector('.land-details');
  //     if (land) {
  //      const gallery = land.images?.map(img => `<img src="${img}" class="gallery-img">`).join('');
  //      //notaion for the contact info
  //      const contact = land.contact || {};
  //      const OwnerName = contact.name || 'Name not provided';
  //      const contactPhone = contact.phone || 'Phone not provided';
  //      const contactEmail = contact.email || 'Email not provided';
  //      //ends here
  //      const featuresList = land.features?.map(feature => 
  //       `<li>${feature}</li>`).join('') || `<li>No features listed.</li>`;
  //       const description = land.description || 'No description available.';
  //       container.innerHTML += ` <div class="gallery">
  //                               ${gallery}
  //                              <h2>${land.title}</h2>
  //                              <p> <strong>Emplacement: </strong> ${land.location} </p> 
  //                              <p> <strong>Prix: </strong> ${land.price} </p> 
  //                             <h3> Features:</h3>
  //                             <ul>${featuresList}</ul>
  //                             <p> <strong>Description<strong> ${description} </p>
  //                              <div class="conatct-info">
  //                             <h3>Contacter le propriétaire</h3>
  //                             <p> <strong>propriétaire: </strong>${OwnerName} </p>
  //                             <p> <strong>Numero: </strong> <a href="tel:${contactPhone}">${contactPhone}</a> </p>
  //                             <p> <strong>Email: </strong><a href="mailto:${contactEmail}">${contactEmail} </a> </p>
  //                             <label for="message" id="Omsg">Envoie message</label>
  //                             <textarea type="text" class="Message"></textarea>
  //                             <button type="submit" id="Omsg-B">Soumettre</button>
  //                             </div>
  //                              <h3>Carte de localisation<h3>
                               
  //                              <iframe src="${land.map}" width="100%" height="300" style="border:0:" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
                               
  //                              <a href="index.html">Accueil</a>
  //                              </div>
  //                              `;  
  //      console.log(container) 
  //     } else {
  //       console.log(container)
  //       container.innerHTML = `<p>Land not found</p>`
  //       console.log(10+8)
  //     }
  //   });
  // }

  //All Lands Code


  if (alllands) {
    const container = document.querySelector('.all-Lands');
    const searchInput = document.getElementById('search-location');
    const searchIcon = document.getElementById('search-Icon');
    const noResult = document.querySelector('.No-result');
    let allLands = [];
  fetch('/static/land.json')
  .then(jalloh => jalloh.json())
  .then(Barrie => {
    allLands = Barrie;
    displayLands(allLands);

  });

  // console.log(displayLands)
    function displayLands(landsToDisplay) {
      if (landsToDisplay.length === 0) {
        noResult.style.display = 'block';
        return;
      }else{
        noResult.style.display = 'none';
      
      container.innerHTML = '';
      landsToDisplay.forEach(land =>{ 
        container.innerHTML += ` <section class="Lands-card"> <img src="${land.mainimage}" alt="${land.title}">
        <h2>${land.title}</h2> 
        <p> <strong> Emplacement: </strong>${land.location} </p> 
        <p> <strong> Prix: </strong>${land.price} </p> 
        <a href="/land/${land.id}" class="view-more-btn">Voir plus</a> </section>`;
        
      });
    }
  }
    // Code To Search for a country by Location in the all Lands Page
// function setupSearch(allLands) {

searchIcon.addEventListener('click', () =>  {
  const searchTerm = searchInput.value.trim().toLowerCase();
  const Filterlands = allLands.filter(land => {
    const Location = land.location?.toLowerCase();
    return Location && Location.includes(searchTerm);
  })
  // console.log(Filterlands)
  displayLands(Filterlands)
  });
  };
  

 //Contact Page
  const form = document.getElementById("contactForm");
  console.log(form)
  if (form) {
    const massages = document.getElementById("sentMessage");
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const firstName = document.getElementById('FirstName').value.trim();
      const lastName =document.getElementById('LastName').value.trim();
      const number = document.getElementById('phone').value.trim();
      const email = document.getElementById('email').value.trim();
      const message = document.getElementById('message').value.trim();

      const FullMessage = `Name: ${firstName}%0ALastName: ${lastName}%0ALastName: ${number}%0ANumber: ${email}%0AEmail ${message}`;
      const PhoneNumber = "224627021857";
      const WhatsApp = `https://wa.me/${PhoneNumber}?text=${FullMessage}`;
      window.open(WhatsApp,"_blank");
      form.reset();
      form.style.display = "none";
      massages.classList.remove("hidden");
    //  alert("Thank");
    });

  }
    
  

})

//All Lands Page 

// if (document.body.classList.contains('AllLands')){

 
// }



 

// let navbar = document.querySelector('header');
// window.onscroll = function (){
// if (window.scrollY >0) {
//   navbar.style.background = '#eefff9';
// }else{
//   navbar.style.background = 'transparent';
// }
// }



// }
