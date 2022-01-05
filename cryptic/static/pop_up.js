const answerBtn = document.querySelector('.answer-btn');
let answerInput = document.querySelector('.answer');

answerBtn.addEventListener('click', Popup);
answerInput.addEventListener('keyup', (event) => {
    console.log(event.keyCode);
    if (event.keyCode === 13) {
        event.preventDefault();
        Popup();
    }
});

function successPopup() {
    Swal.fire({
        title: 'Correct answer!', 
        icon: 'success',
        width: '40rem',
        background: '#1f1e1e',
        color: '#faf9f9',
        showConfirmButton: false,
        timer: 2000,
        position: 'top-end',
        timerProgressBar: true
    })
}

function errorPopup() {
    Swal.fire({
        title: 'Wrong answer!', 
        text: 'Try again',
        icon: 'error',
        width: '40rem',
        background: '#1f1e1e',
        color: '#faf9f9',
        showConfirmButton: false,
        timer: 2000,
        position: 'top-end',
        timerProgressBar: true
    })
}

function warningPopup() {
    Swal.fire({
        text: 'Please type an answer',
        icon: 'warning',
        width: '40rem',
        backdrop: false,
        background: '#1f1e1e',
        color: '#faf9f9',
        showConfirmButton: false,
        timer: 2000,
        position: 'top-end',
        timerProgressBar: true
    })
}
