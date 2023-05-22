function singleSolution(){ 
    const solutionLabel = document.getElementById("solutionlabel");
    solutionLabel.setAttribute("style", "display:block;")

    const solution = document.getElementById("solution");
    solution.setAttribute("style", "display:block;")
    solution.setAttribute("required", "true")

    const testCaseButton = document.getElementById("testcasebutton");
    testCaseButton.setAttribute("style", "display:none;")

    const solutionbutton = document.getElementById("solutionbutton");
    solutionbutton.setAttribute("style", "display:none;")
}