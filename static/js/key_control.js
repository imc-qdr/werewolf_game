// Get the input field
var input = document.getElementById("Pname");

// Execute a function when the user releases a key on the keyboard
input.addEventListener("keydown", function(event) {
// Number 13 is the "Enter" key on the keyboard
	if (event.keyCode === 13) {
		// Cancel the default action, if needed
		event.preventDefault();
		// Trigger the button element with a click
		document.getElementById("Create_Player").click();
	}
});
