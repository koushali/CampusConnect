// -------- LOGIN VALIDATION --------
function validateLogin() {
    var u = document.getElementById("username").value;
    var p = document.getElementById("password").value;

    if (u === "" || p === "") {
        alert("Username and Password cannot be empty");
        return false;
    }

    alert("Client-side validation passed (can be bypassed)");
    return true;
}

// -------- DISCUSSION WARNING --------
function showWarning() {
    alert("Warning: Inputs are not sanitized. This page is vulnerable to XSS.");
}
