function validateForm()
{
    var getPlayer = document.forms["PlayerForm"]["Pname"].value;
    if (getPlayer === "")
    {
           alert('Please input a Name');
        return false;
    } 
}

