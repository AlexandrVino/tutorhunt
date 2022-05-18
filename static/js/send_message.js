window.onload = () => {
    let sendMessageForm = document.forms[0];
    let button = document.getElementById('send-mess-btn')
    let text = document.getElementById('input_message')
    let block = document.getElementById("messages-list");
    block.scrollTop = 9999999;

    sendMessageForm.addEventListener('submit', function () {

    })

    button.onclick = () => {
        sendMessageForm.submit()
    }
}