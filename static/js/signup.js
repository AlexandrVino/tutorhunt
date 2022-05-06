window.onload = () => {
    let regForm = document.forms[0];

    let password1 = document.getElementById('id_password1')
    let password2 = document.getElementById('id_password2')
    let username = document.getElementById('username')
    let button = document.getElementById('submit')
    let email = document.getElementById('id_email')
    let role = document.getElementById('id_role')

    let letters = 'qwertyuiopasdfghjklzxcvbnm'
    let numbers = '01234567890'
    let special_chars = '-_'
    let all_symbols = letters + numbers + special_chars

    role.classList.add('form-control')
    role.classList.add('input-field')
    role.classList.add('role')

    function check_passwords() {

        let password1_value = password1.value.toLowerCase()
        let password2_value = password2.value.toLowerCase()

        let has_letters = false
        let has_numbers = false

        let mess = ''

        for (let char of password1_value) {
            if (all_symbols.indexOf(char) === -1) {
                mess = 'Для пароля рарешено использовать только латинские буквы, цифры и -_'
                return [false, mess]
            }

            if (letters.indexOf(char) !== -1) {
                has_letters = true
            }

            if (numbers.indexOf(char) !== -1) {
                has_numbers = true
            }
        }

        mess = mess + (password1_value === password2_value ? '' : '\nПароли не совпадают')
        mess = mess + (has_numbers ? '' : '\nВ пароле должна быть хотя бы одна цифра')
        mess = mess + (has_letters ? '' : '\nВ пароле должна быть хотя бы одна буква')
        mess = mess + (password1_value.length >= 8 ? '' : '\nПароль должен состоять минимум из 8 символов')

        return [password1_value === password2_value && has_letters && has_numbers, mess]

    }

    function validate_email() {
        let mess = 'Введите корректный email'
        let email_text = email.value
        let is_valid = String(email_text)
            .toLowerCase()
            .match(
                /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
            )

        return [is_valid, is_valid === null ? mess : '']
    }

    function check_username() {
        let username_value = username.value

        for (let char of username_value) {
            if (all_symbols.indexOf(char) === -1) {
                return [false, 'Для имени рарешено использовать только латинские буквы, цифры и -_']
            }
        }
        return [true, '']
    }

    regForm.addEventListener('submit', function () {

    })

    button.onclick = () => {
        let mes_password = check_passwords();
        let mes_username = check_username();
        let mes_email = validate_email();

        if (mes_password[0] && mes_username[0] && mes_email[0]) {
                    console.log(regForm)
            regForm.submit()
        } else {
            alert(mes_username[1] + '\n' + mes_password[1] + '\n' + mes_email[1])
        }
    }
}