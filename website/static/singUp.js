function professorCheck() {
    if (document.getElementById('professor').checked) {
        document.getElementById('professor_token_div').style.display = 'block';
    }
    else document.getElementById('professor_token_div').style.display = 'none';
}