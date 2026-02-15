document.getElementById('register-btn').addEventListener('click', () => {
    const user_name = document.getElementById('u_name').value.trim();
    const user_mail = document.getElementById('u_mail').value.trim();
    const user_password = document.getElementById('u_password').value.trim();
    const confirm_password = document.getElementById('u_cpassword').value.trim();

    const alert_box = document.getElementById('alert_box');
    const alert_message_span = document.getElementById('alert_message');

    if (!user_name || !user_mail || !user_password || !confirm_password) {
        alert_message_span.textContent = "Please fill all the fields";
        alert_box.classList.remove('hidden');
        alert_box.classList.add('show');
        return;
    }
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(user_mail)) {
        alert_message_span.textContent = "Please enter a valid email";
        alert_box.classList.remove('hidden');
        alert_box.classList.add('show');
        return;
    }
    if(user_password.length<6){
        alert_message_span.textContent='Password should have atleast 6 charactes'
        alert_box.classList.remove('hidden')
        alert_box.classList.add('show')
        return;
    }
    if(user_password!==confirm_password){
        alert_message_span.textContent='Passwords do not match'
        alert_box.classList.remove('hidden')
        alert_box.classList.add('show')
        return;  
    }
    document.getElementById('reg-form').submit();

});

document.getElementById('close_alert').addEventListener('click', () => {
    const alert_box = document.getElementById('alert_box');
    alert_box.classList.add('hidden');
    alert_box.classList.remove('show');
    alert_message_span.textContent="";

});
