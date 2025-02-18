const tbody = document.getElementsByTagName('tbody')[0];

function newBookEntry(bookJSON) {
    // adds a new row in books table
    const tr = document.createElement('tr');
    const id = document.createElement('td');
    const title = document.createElement('td');
    const price = document.createElement('td');
    id.innerText = bookJSON.id;
    title.innerText = bookJSON.title;
    price.innerText = bookJSON.price.toFixed(2);
    if(bookJSON.soldout)
        tr.classList.add('soldout');
    tr.appendChild(id);
    tr.appendChild(title);
    tr.appendChild(price);
    tbody.appendChild(tr);
}

function buildBookTable(booksJSONArray) {
    // remove all tbody entries and adds new ones
    tbody.replaceChildren();
    if(booksJSONArray.length < 1) {
        const tr = document.createElement('tr');
        const td = document.createElement('td');
        td.colSpan = 3;
        td.innerText = "Empty database :("
        tr.appendChild(td);
        tbody.appendChild(tr);
        return;
    }
    for(let i = 0; i < booksJSONArray.length; i++) {
        newBookEntry(booksJSONArray[i]);
    }
}

function fetchBooksAndUpdate() {
    // fetch all books from Book API and build them in a tbody elem
    fetch('/get-books')
        .then(response => {
            if(!response.ok) {
                throw new Error('Network response failed.');
            }
            return response.json();
        })
        .then(booksJSONArray => {
            buildBookTable(booksJSONArray);
        })
        .catch(error => {
            console.log('Error while loading books: ', error);
        });
}

function __init() {
    // fetch books from API, update books table and repeat every second.
    fetchBooksAndUpdate();
    setInterval(fetchBooksAndUpdate, 1000);
}

__init();
