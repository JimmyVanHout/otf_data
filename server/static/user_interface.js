function displayOnCheck(checkbox) {
    let div = document.getElementById("forwarding_input");
    if (checkbox.checked) {
        let ids = ["forwarding_email_address", "forwarding_password", "forwarding_confirm_password", "forwarding_receiving_email_address", "forwarding_mailbox"];
        let descriptions = ["Enter email address of forwarding account: ", "Enter password of forwarding account: ", "Confirm password of forwarding account: ", "Enter receiving email address: ", "Enter mailbox to search (left blank, default is inbox): "];
        let input_types = ["email", "password", "password", "email", "text"];
        h2 = document.createElement("h2");
        h2.id = "forwarding_heading";
        h2.innerText = "One-Time Forwarding of All Past OT Beat Report Emails from This Account:";
        div.appendChild(h2);
        for (let i = 0; i < ids.length; i++) {
            input = document.createElement("input");
            input.type = input_types[i];
            input.name = ids[i];
            input.id = ids[i];
            label = document.createElement("label");
            label.for = input.id;
            label.id = input.id.concat("_label");
            label.innerText = descriptions[i];
            div.appendChild(label);
            div.appendChild(input);
            div.appendChild(document.createElement("br"));
        }
    } else {
        for (let i = div.children.length - 1; i >=0; i--) {
            div.children[i].remove();
        }
    }
}

function checkPasswordsMatch(password_id, confirm_password_id, error_message, error_id) {
    let password = document.getElementById(password_id);
    let confirm_password = document.getElementById(confirm_password_id);
    let div = document.getElementById("above_submit");
    if (password.value != confirm_password.value) {
        if (Array.from(div.children).filter(child => child.id == error_id).length == 0) {
            let p = document.createElement("p");
            p.className = "error_message";
            p.innerText = error_message;
            p.id = error_id;
            div.appendChild(p);
        }
        console.log(password.value);
        console.log(confirm_password.value);
        return false;
    } else {
        let p = document.getElementById(error_id);
        div.children[Array.from(div.children).indexOf(p)].remove();
        console.log(true);
        return true;
    }
}

function checkAllPasswordsMatch() {
    let forwarding_password = document.getElementById("forwarding_password");
    let forwarding_passwords_match = true;
    if (forwarding_password) {
        forwarding_passwords_match = checkPasswordsMatch("forwarding_password", "forwarding_confirm_password", "Passwords for account to forward messages from did not match. Please reenter them and then resubmit.", "forwarding_passwords_error");
    }
    let searching_passwords_match = checkPasswordsMatch("password", "confirm_password", "Passwords for account to get OT data from did not match. Please reenter them and then resubmit.", "searching_passwords_error");
    return forwarding_passwords_match && searching_passwords_match;
}
