var count = 0;
function testCase(){ 
    count+=1;
    const testCaseLabel = document.getElementById("testcaselabel");
    testCaseLabel.setAttribute("style", "display:block;")

    const solutionbutton = document.getElementById("solutionbutton");
    solutionbutton.setAttribute("style", "display:none;")
    
    const testCaseDiv = document.createElement("div");
    testCaseDiv.setAttribute("id", `testcase${count}`);
    testCaseDiv.setAttribute("class", "input-group");

    const innerTestCaseDiv = document.createElement("div");
    innerTestCaseDiv.setAttribute("class", "input-group-text");
    innerTestCaseDiv.innerHTML = `Test Case ${count}`;
    innerTestCaseDiv.innerHTML = `Test Case ${count}`;
    testCaseDiv.appendChild(innerTestCaseDiv)

    const stdinInput = document.createElement("input");
    stdinInput.setAttribute("type", "text");
    stdinInput.setAttribute("id", `stdin${count}`);
    stdinInput.setAttribute("name", `stdin${count}`);
    stdinInput.setAttribute("placeholder", "Enter Input");
    stdinInput.setAttribute("required", "true");
    stdinInput.setAttribute("class", "form-control");
    testCaseDiv.appendChild(stdinInput)
    
    const stdoutInput = document.createElement("input");
    stdoutInput.setAttribute("type", "text");
    stdoutInput.setAttribute("id", `stdout${count}`);
    stdoutInput.setAttribute("name", `stdout${count}`);
    stdoutInput.setAttribute("placeholder", "Enter Expected Output");
    stdoutInput.setAttribute("required", "true");
    stdoutInput.setAttribute("class", "form-control");
    testCaseDiv.appendChild(stdoutInput)

    const currentDiv = document.getElementById("choicebuttons");

    const parentDiv = document.getElementById("exercisedetails");

    parentDiv.insertBefore(testCaseDiv, currentDiv);
}