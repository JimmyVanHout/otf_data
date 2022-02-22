function displayOnCheck(checkbox) {
    let div = document.getElementById("forwarding_input");
    if (checkbox.checked) {
        let ids = ["forwarding_email_address", "forwarding_password", "forwarding_receiving_email_address", "forwarding_mailbox"];
        let descriptions = ["Enter email address of forwarding account: ", "Enter password of forwarding account: ", "Enter receiving email address: ", "Enter mailbox to search (left blank, default is inbox): "];
        let input_types = ["text", "password", "text", "text"];
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
            label.innerText = descriptions[i];
            div.appendChild(label);
            div.appendChild(input);
            div.appendChild(document.createElement("br"));
        }
        h2 = document.getElementById("searching_heading");
        h2.innerText = "Then Receive Them Here and Get OT Beat Report Data from This Account:";
    } else {
        for (let i = div.children.length - 1; i >=0; i--) {
            div.children[i].remove();
        }
        h2 = document.getElementById("searching_heading");
        h2.innerText = "Get OT Beat Report Data from This Account:";
    }
}
