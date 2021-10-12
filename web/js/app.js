var input_expression = document.querySelector(".expressionField")
var label_info = document.querySelector('.infoLabel')
var label_result = document.querySelector('.resultLabel')
var container_result = document.querySelector('#result')
var btn_submit = document.querySelector('.submitBtn');

btn_submit.onclick = function() { sendData() } // Handle btn press event

document.addEventListener("keyup", function(event) { // Handle enter btn click event
    if (event.key === "Enter") { 
        sendData() 
    }
})

function getData(res) {
    if (res.includes('error=')) {
        res = res.replace('error=', '')
        console.log(`error: ${res}`)
        label_info.innerHTML = res
        return false
        
    } else {
        label_result.innerHTML = res
        label_info.innerHTML = ''
        container_result.style.display = ''
        console.log(`result: ${res}`)
    }
    return res
}

function sendData() { // Send input data to python
    var expression = input_expression.value
    console.log(`expression: ${expression}`)

    if (expression == null || expression == "") {
        label_info.innerHTML = 'Veuillez remplir tous les champs.';
        return false
        
    } else {
        eel.solve(expression)(getData)
        return true
    }

}

input_expression.focus()
eel.expose(sendData);