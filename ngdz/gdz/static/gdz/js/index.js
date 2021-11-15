const isMobile = window.matchMedia("only screen and (max-width: 760px)").matches;

const lesson_buttons = document.querySelectorAll('#lesson-container button');
const klasses = JSON.parse(document.querySelector('#klasses_data').textContent);
const books = JSON.parse(document.querySelector('#books_data').textContent);

let display_klasses = [];
let selected_lesson = null;
let selected_klass = null;
let klass_buttons = [];

lesson_select(lesson_buttons[0]);
show_klasses();

function lesson_click(event) {
    lesson_select(event.target);
    show_klasses()
}

function klass_click(event) {
    klass_select(event.target)
    show_books()
}

function lesson_select(el) {
    lesson_buttons.forEach(element => {
        element.classList.remove('text-white', 'bg-dark');
        element.classList.add('text-secondary');
    });
    el.classList.remove('text-secondary');
    el.classList.add('text-white', 'bg-dark');
    selected_lesson = el;
}

function show_klasses() {
    const from_lesson = selected_lesson.innerHTML;
    const t_klasses = klasses.filter(kl_obj => kl_obj.lesson === from_lesson);
    const klasses_container = document.querySelector('#klasses-container');
    klasses_container.innerHTML = t_klasses.map(
        kl_obj => (
            `<li class="nav-item">
                <button class="nav-link text-secondary" onclick="klass_click(event)">${kl_obj.klass}</button>
            </li>`
        )
    ).join('\n');
    klass_buttons = document.querySelectorAll('#klasses-container button');
}

function klass_select(el) {
    klass_buttons.forEach(element => {
        element.classList.remove('text-white', 'bg-dark');
        element.classList.add('text-secondary');
    });
    el.classList.remove('text-secondary');
    el.classList.add('text-white', 'bg-dark');
    selected_klass = el;
}

function show_books() {
    const kl = selected_klass.innerHTML;
    const l = selected_lesson.innerHTML;

    const d_books = books.filter(book => book.lesson === l && book.klass === kl);
    
    let book_rows = d_books.map((book, idx) => {
        let r_bs = []
        if(isMobile) {
            if(idx % 2 !== 0) return;
            r_bs = [book, d_books[idx+1] || undefined].filter((el) => el !== undefined);
        } else {
            if(idx % 3 !== 0) return;
            r_bs = [book, d_books[idx+1] || undefined, d_books[idx+2] || undefined].filter((el) => el !== undefined); 
        }
        cols = r_bs.map(a_book => `<div class="col-${isMobile ? '6' : '4'}">
            <a class="text-decoration-none" onclick="postloader()" href="/${a_book.l_slug}/${a_book.klass}/${a_book.slug}/">
                <div class="border border-secondary rounded p-2 h-100 text-center text-dark">
                    <img class="mb-2 float-end rounded" src="${a_book['img']}">
                    <h4>${a_book.title}</h4>
                    <p>${a_book.author}</p>
                </div>
            </a>
        </div>`)
        return cols;
    }).filter((el) => el !== undefined);

    const books_container = document.querySelector('#books-container');
    if(book_rows.length) {
        books_container.innerHTML = book_rows.map(cols => (
            `<div class="row mb-4">
                ${cols[0] || ''}
                ${cols[1] || ''}
                ${!isMobile ? cols[2] || '' : ''}
            </div>`
        )).join('\n');
    } else {
        books_container.innerHTML = '<h4>Тут ничего нет.</h4><p>P.S. Делай сам</p>'
    }
}
