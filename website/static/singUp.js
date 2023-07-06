function professorCheck() {
    if (document.getElementById('professor').checked) {
        document.getElementById('professor_token_div').style.display = 'block';
        setRequired(true);
    }
    else {
        document.getElementById('professor_token_div').style.display = 'none';
        setRequired(false);        
    }

    function setRequired(val){
        input = document.getElementById("professor_token");
        input.required = val;
    }
}