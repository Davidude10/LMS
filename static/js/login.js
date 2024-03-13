function selectUserType(userType) {
    var messageElement = document.getElementById("userMessage");
    switch (userType) {
        case "admin":
            messageElement.textContent = "Welcome Admin!";
            break;
        case "student":
            messageElement.textContent = "Welcome Student!";
            break;
        default:
            break;
    }
}