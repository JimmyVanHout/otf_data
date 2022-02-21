function displayOnCheck(checkbox) {
    let div = document.getElementById("forwarding_input");
    if (checkbox.checked) {
        let ids = ["forwarding_email_address", "forwarding_password", "forwarding_receiving_email_address", "forwarding_mailbox"];
        let descriptions = ["Enter the email address of the account to search in: ", "Enter the password of the account to search in: ", "Enter receiving email address: ", "Enter mailbox to search (left blank, default is inbox): "];
        for (let i = 0; i < ids.length; i++) {
            input = document.createElement("input");
            input.type = "text";
            input.name = ids[i];
            input.id = ids[i];
            label = document.createElement("label");
            label.for = input.id;
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
