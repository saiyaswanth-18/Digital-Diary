let message=document.getElementById('alert_message').innerText
const alert_box=document.getElementById('alert_box')
if(message){
    alert_box.classList.remove('hidden')
    alert_box.classList.add('show')
}
document.getElementById('close_alert').addEventListener('click', () => {
    alert_box.classList.add('hidden');
    alert_box.classList.remove('show');
});
