let fields = document.querySelectorAll('.exceptions');

fields.forEach((field) => {
    field.addEventListener('keypress', (event) => {
        let key = event.keyCode;
        if (key === 32 || key === 39 || key === 34 || key === 61 ) {
            event.preventDefault();
        }
    })
})
