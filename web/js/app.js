var btn_submit = document.querySelector('.submitBtn');
var label_result = document.querySelector('.resultLabel')
var input_expression = document.querySelector(".expressionField")

btn_submit.onclick = function() { sendData() } // Handle btn press event

document.addEventListener("keyup", function(event) { // Handle enter btn click event
    if (event.key === "Enter") { 
        sendData() 
    }
})

function getData(res) {
    if (res.includes('error=')) {
        res = res.replace('error=', '')
        label_result.innerHTML = res;
        console.log(`error: ${res}`)
        return false;
        
    } else {
        label_result.innerHTML = `Résultat: ${res}`;
        console.log(`result: ${res}`)
        return res
    }
}

function sendData() { // Send input data to python
    var expression = input_expression.value;
    console.log(`expression: ${expression}`)

    if (expression == null || expression == "") {
        label_result.innerHTML = 'Veuillez remplir tous les champs.';
        return false;
        
    } else {
        eel.solve(expression)(getData);
        return true;
    }

}

input_expression.focus()
eel.expose(sendData);