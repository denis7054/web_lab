/*
Реализация AJAX с помощью асинхронного метода fetch. Современный вариант реализации AJAX.
*/

var sendbtn = document.getElementById("btn-send");    // выбираем DOM-елемент (кнопку)

// Привязываем к элементу обработчик события "click"
sendbtn.addEventListener("click", function (e) {
    /* Инструкция preventDefault позволяет переопределить стандартное поведение браузера,
    если ее убрать, то браузер по-умолчанию обновит страницу после отправки данных формы */
    e.preventDefault();
    // Получаем данные полей формы
    let firstname = document.getElementsByName("firstname")[0].value;
    let email = document.getElementsByName("femail")[0].value;
    let fnum = document.getElementsByName("fnum")[0].value;
    let mess = document.getElementsByName("mess")[0].value;
    
    // Преобразуем полученные данные в JSON
    // var formdata = JSON.stringify({ firstname: firstname});
    var formdata = JSON.stringify({ firstname: firstname, email: email, fnum: fnum, mess: mess});

    // alert(formdata);
    // Отправляем запрос через fetch (необходимо выставить соответствующий заголовок (headers)!)
    fetch("/api/contactrequest",
    {
        method: "POST",
        body: formdata,
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then( response => {
        // fetch в случае успешной отправки возвращает Promise, содержащий response объект (ответ на запрос)
        // Возвращаем json-объект из response и получаем данные из поля message
        response.json().then(function(data) {
            // alert(data);
            console.log(data.message)
            let statfield = document.getElementById("statusfield");
            statfield.textContent = data.message;
            //statfield.textContent.bold();
            // alert(data.message);
        });
    })
    .catch( error => {
        alert(error);
        console.error('error:', error);
    });

});
