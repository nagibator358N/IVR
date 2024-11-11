console.log("JavaScript is working!");
/* Функция для форматирования даты */
function formatDate(inputDate, format) {
    const date = new Date(inputDate);
    switch (format) {
        case "ru-long":
            return date.toLocaleDateString('ru-RU', {
                weekday: 'long',
                day: 'numeric',
                month: 'long',
                year: 'numeric',
            });
        case "ru-datetime":
            return date.toLocaleString('ru-RU', {
                day: '2-digit',
                month: '2-digit',
                year: 'numeric',
                hour: '2-digit',
                minute: '2-digit',
            });
        case "ru-datetime-seconds":
            return date.toLocaleString('ru-RU', {
                day: '2-digit',
                month: '2-digit',
                year: 'numeric',
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit'
            });
    }
}
/* Функция для форматирования времени в секундах */
function formatTime(seconds) {
    const totalSeconds = Math.round(seconds);
    const hours = Math.floor(totalSeconds / 3600);
    const minutes = Math.floor((totalSeconds % 3600) / 60);
    const remainingSeconds = totalSeconds % 60;

    let timeString = '';

    if (hours > 0) {
        timeString += `${hours} ${hours === 1 ? 'час' : 'часа'}`;
    }

    if (minutes > 0) {
        timeString += `${timeString ? ' ' : ''}${minutes} ${minutes === 1 ? 'мин' : 'мин'}`;
    }

    if (remainingSeconds > 0) {
        timeString += `${timeString ? ' ' : ''}${remainingSeconds} ${remainingSeconds === 1 ? 'сек' : 'сек'}`;
    }

    return timeString;
}
/* Функция для получения cookie */
function get_cookie(name) {
    const cookieArr = document.cookie.split(";");
    for (let i = 0; i < cookieArr.length; i++) {
        let cookiePair = cookieArr[i].split("=");
        if (cookiePair[0].trim() === name) {
            return cookiePair[1];
        }
    }
    return null;
}
/* Функция для получения списка itemов для главного меню*/
function get_list_item_main_menu() {
    return [
        {
            "label": "Тесты",
            "action": show_tests_list_with_button
        },
        {
            "label": "Мои тесты",
            "action": show_my_tests_menu
        },
        {
            "label": "Результаты",
            "action": show_my_session_list
        },
        {
            "label": "Профиль",
            "action": show_my_profile
        },
        {
            "label": "Помощь",
            "action": show_help
        }

    ];
}
function get_list_help_q_a(){
    return [
        {
            q:"Что такое Тесты?",
            a:"Тесты - это список всех существующих тестов в системе, который вы можете просмотреть"
        },
        {
            q:"Что такое Мои тесты?",
            a:"Мои тесты - это меню, в котором вы можете создать тест, добавить вопросы и ответы на вопросы к тесту, просмотреть статистику по вашим тестам "
        },
        {
            q:"Что такое Результаты?",
            a:"Результаты - это меню, в котором вы можете просмотреть свои результаты не тесты и при нажатии увидеть ваши баллы за вопрос и подробности прохождения теста"
        },
        {
            q:"Что такое Профиль?",
            a:"Профиль - это меню, в котором вы можете изменить свои данные(пароль и email)"
        },
        {
            q:"Как создать тест?",
            a:"Выберите меню Мои тесты и нажмите Создать тест, далее введите данные, и тест будет создан"
        },
        {
            q:"Как изменить тест?",
            a:"Выберите меню Мои тесты и нажмите Список тестов, далее выберите нужный вам тест, нажмите на него и нажмите на кнопку изменить, затем измените нужные данные"
        },
        {
            q:"Как удалить тест?",
            a:"Выберите меню Мои тесты и нажмите Список тестов, далее выберите нужный вам тест, нажмите на него и нажмите на кнопку Удалить тест"
        },       
        {
            q:"Как создать вопрос?",
            a:"Выберите меню Мои тесты и нажмите список тестов, затем вопросы к тесту и кнопку добавить вопрос"
        },
        {
            q:"Как изменить вопрос?",
            a:"Выберите меню Мои тесты и нажмите список тестов, затем вопросы к тесту, после нажмите на нужный вопрос и кнопку Изменить, введя нужные данные"
        },
        {
            q:"Как удалить вопрос?",
            a:"Выберите меню Мои тесты и нажмите список тестов, затем вопросы к тесту, после нажмите на нужный вопрос и кнопку Удалить вопрос"
        },
        {
            q:"Как добавить вариант ответа на вопрос?",
            a:"Выберите меню Мои тесты и нажмите Список тестов, выберите нужный, нажмите вопросы к тесту, выберите нужный вопрос и нажмите кнопку Добавить ответ"
        },
        {
            q:"Как просмотреть Статистику?",
            a:"Выберите меню Мои тесты и нажмите Статистика, далее выберите нужный вам тест"
        },
        {
            q:"Как просмотреть свой email?",
            a:"Выберите меню Профиль и вы увидите свою почту"
        }, 
    ]
}
function show_help(){
    let main_content = get_main_content(["left-padding"]);
    let list_help = get_list_help_q_a();
    list_help.forEach(item=>{
        let q = document.createElement("div");
        q.append(item.q);
        q.classList.add("help_q");
        let a = document.createElement("div");
        a.append(item.a);
        a.classList.add("help_a");
        main_content.append(q,a);
    })
    main_content.append(create_button_back_to_main_menu())
}
/* Функция для получения списка itemов для меню Мои тесты*/
function get_list_item_my_tests_menu() {
    return [
        {
            "label": "Создать тест",
            "action": show_form_add_test
        },
        {
            "label": "Список тестов",
            "action": show_my_tests_list_click
        },
        {
            "label": "Статистика",
            "action": show_statistics_list
        },
        {
            "label": "Назад",
            "action": show_main_menu
        }
    ];
}
/* Функция для создания label*/
function create_label(name, par) {
    let label = document.createElement("label");
    label.append(name);
    label.setAttribute("for", par);
    return label;
}
/* Функция для создания input*/
function create_input(type, name, value, id, classList = [], eventList = {}, attr = {}) {
    attr["type"] = type;
    attr["name"] = name;
    attr["value"] = value;
    attr["id"] = id;
    let input = create_element("input", null, attr, classList, eventList)
    return input;
}
/* Функция для создания input'а с label'ом*/
function create_input_with_label(title, type, name, value, id, classList = [], eventList = {}, attr = {}) {
    let div = document.createElement("div");
    let input = create_input(type, name, value, id, classList, eventList, attr);
    let label = create_label(title, id);
    div.append(label, input);
    return div;
}
/* Функция для создания поля с выпадающим списком с выбором*/
function create_select_yes_no(value, attr = {}, classList = [], eventList = {}) {
    let sel = document.createElement("select");
    let sel_yes = document.createElement("option");
    sel_yes.append("Да");
    sel_yes.value = 1;
    let sel_no = document.createElement("option");
    sel_no.append("Нет");
    sel_no.value = 0;
    sel.append(sel_yes, sel_no);
    if (value) {
        sel_yes.setAttribute("selected", "true");
    }
    else {
        sel_no.setAttribute("selected", "true")
    }
    add_attributes_to_element(sel, attr, classList, eventList);
    return sel;
}
/* Функция для создания поля с выпадающим списком с выбором с назаванием*/
function create_yes_no_with_label(title, value, attr = {}, classList = [], eventList = {}) {
    let div = document.createElement("div");
    let yes_no = create_select_yes_no(value, attr, classList, eventList);
    let label = create_label(title, attr.id);
    div.append(label, yes_no);
    return div;
}
/* Функция для создания формы создания или изменения теста*/
function create_form_add_test(quiz) {
    let form = document.createElement("form");

    form.append(create_input_with_label("Имя теста", "text", "quiz_name", quiz ? quiz.quiz_name : "", "quiz_name", ["data_to_send"]));

    form.append(create_input("hidden", "user_id", get_cookie("user_id"), "user_id", ["data_to_send"]));

    form.append(create_input_with_label("Время прохождения теста", "text", "duration", quiz ? quiz.duration : "", "duration", ["data_to_send"]));

    form.append(create_input_with_label("Минимальное количество вопросов", "text", "questions_amount_to_complete", quiz ? quiz.questions_amount_to_complete : "", "questions_amount_to_complete", ["data_to_send"]));

    form.append(create_label("Описание теста", "quiz_description"));

    form.append(create_element("textarea", quiz ? quiz.quiz_description : "", { id: "quiz_description", type: "text", name: "quiz_description", value: quiz ? quiz.quiz_description : "" }, ["data_to_send"]));

    form.append(create_input_with_label("Количество попыток на прохождение теста", "text", "quiz_tries", quiz ? quiz.quiz_tries : "", "quiz_tries", ["data_to_send"]));

    form.append(create_yes_no_with_label("Показать ответы пользователю после прохождения теста", quiz ? quiz.show_ans_res : 1, { id: "show_ans_res", type: "checkbox", name: "show_ans_res" }, ["data_to_send"]));

    form.append(create_input_with_label("Баллы за тест(оценка)", "text", "quiz_mark_type", quiz ? quiz.mark_type : "", "quiz_mark_type", ["data_to_send"]));

    form.append(create_yes_no_with_label("Возможность переключения между вопросами", quiz ? quiz.question_switch : 1, { id: "question_switch", type: "checkbox", name: "question_switch" }, ["data_to_send"]));

    form.append(create_yes_no_with_label("Возможность ответить на вопрос заново", quiz ? quiz.reanswer : 1, { id: "reanswer", type: "checkbox", name: "reanswer" }, ["data_to_send"]));

    form.append(create_input_with_label("Количество простых вопросов", "text", "question_easy", quiz ? quiz.question_easy : "", "question_easy", ["data_to_send"]));

    form.append(create_input_with_label("Количество средних вопросов", "text", "question_medium", quiz ? quiz.question_medium : "", "question_medium", ["data_to_send"]));

    form.append(create_input_with_label("Количество сложных вопросов", "text", "question_hard", quiz ? quiz.question_hard : "", "question_hard", ["data_to_send"]));

    let create_test_button = document.createElement("button");
    create_test_button.type = "submit";
    if (quiz) {
        create_test_button.append("Изменить тест");
    }
    else {
        create_test_button.append("Создать тест");
    }
    form.append(create_test_button);
    let error_message = document.createElement("div");
    let url = "/quiz/add/";
    let method = "POST";
    let success_function = () => show_main_menu("Тест успешно создан");
    if (quiz) {
        url = "/quiz/" + quiz.id + "/update";
        method = "PUT";
        success_function = () => show_one_my_test(quiz.id);
    }
    form.setAttribute("method", method);
    let submit_form = create_submit_function(success_function, function (json) {
        if (json.error) {
            error_message.innerHTML = json.error;
            alert(json.error);
        }
    }, url);
    form.onsubmit = submit_form;
    form.setAttribute("action", url);
    return form;
}
/* Функция для выбора типа вопроса(а именно выпадающий список с выбором)*/
function create_select_question_type(value, attr = {}, classList = [], eventList = {}) {
    let sel = document.createElement("select");
    let sel_one_ans = document.createElement("option");
    sel_one_ans.textContent = "Вопрос с выбором одного варианта ответа";
    sel_one_ans.value = 1;
    let sel_multiple_ans = document.createElement("option");
    sel_multiple_ans.textContent = "Вопрос с выбором нескольких вариантов ответа";
    sel_multiple_ans.value = 2;
    let sel_free_response = document.createElement("option");
    sel_free_response.textContent = "Вопрос со свободным ответом";
    sel_free_response.value = 3;
    sel.append(sel_one_ans, sel_multiple_ans, sel_free_response);
    if (value === 1) {
        sel_one_ans.setAttribute("selected", "true");
    } else if (value === 2) {
        sel_multiple_ans.setAttribute("selected", "true");
    } else if (value === 3) {
        sel_free_response.setAttribute("selected", "true");
    }
    add_attributes_to_element(sel, attr, classList, eventList);
    return sel;
}
/* Функция для выбора типа вопроса с label'ом*/
function create_select_question_type_with_label(title, value, attr = {}, classList = [], eventList = {}) {
    let div = document.createElement("div");
    let question_type = create_select_question_type(value, attr, classList, eventList);
    let label = create_label(title, attr.id);
    div.append(label, question_type);
    return div;
}
/* Функция для создания формы создания или изменения вопроса*/
function create_form_add_question(quiz, question = null) {
    let form = document.createElement("form");

    form.append(create_input_with_label("Текст вопроса", "text", "question_text", question ? question.question_text : "", "question_text", ["data_to_send"]));

    form.append(create_label("Описание вопроса", "question_description"));

    form.append(create_element("textarea", question ? question.question_description : "", { id: "question_description", type: "text", name: "question_description", value: question ? question.question_description : "" }, ["data_to_send"]));

    form.append(create_input_with_label("Время на вопрос", "text", "question_time", question ? question.question_time : "", "question_time", ["data_to_send"]));

    form.append(create_input_with_label("Количество баллов за вопрос", "text", "question_points", question ? question.question_points : "", "question_points", ["data_to_send"]));

    form.append(create_select_question_type_with_label("Тип вопроса", question ? question.question_type : 1, { id: "question_type", type: "checkbox", name: "question_type" }, ["data_to_send"]));

    form.append(create_input("hidden", "quiz_id", quiz.id, "quiz_id", ["data_to_send"]));

    form.append(create_input_with_label("Номер вопроса", "text", "question_number", question ? question.question_number : "", "question_number", ["data_to_send"]));

    form.append(create_input_with_label("Сложность вопроса", "text", "question_difficulty", question ? question.question_difficulty : "", "question_difficulty", ["data_to_send"]));

    form.append(create_input_with_label("Подсказка на вопрос", "text", "question_hint", question ? question.question_hint : "", "question_hint", ["data_to_send"]));

    let create_test_button = document.createElement("button");
    create_test_button.type = "submit";
    if (question) {
        create_test_button.append("Изменить вопрос");
    }
    else {
        create_test_button.append("Создать вопрос");
    }
    form.append(create_test_button);
    let error_message = document.createElement("div");
    let url = "/quiz/question/add";
    let method = "POST";
    let success_function = () => show_questions_list_for_quiz("", quiz);
    if (question) {
        url = "/question/" + question.id + "/update";
        method = "PUT";
        success_function = () => show_questions_list_for_quiz("", quiz);
    }
    form.setAttribute("method", method);
    let submit_form = create_submit_function(success_function, function (json) {
        if (json.error) {
            error_message.innerHTML = json.error;
            alert(json.error);
        }
    }, url);
    form.onsubmit = submit_form;
    form.setAttribute("action", url);
    return form;
}
/* Функция для выбора типа ответа(правильный или неправильный)*/
function create_select_answer_type(value, attr = {}, classList = [], eventList = {}) {
    let sel = document.createElement("select");
    let sel_correct = document.createElement("option");
    sel_correct.textContent = "Правильный вариант ответа";
    sel_correct.value = 1;
    let sel_incorrect = document.createElement("option");
    sel_incorrect.textContent = "Неправильный вариант ответа";
    sel_incorrect.value = 0;
    sel.append(sel_correct, sel_incorrect);
    if (value === 1) {
        sel_correct.setAttribute("selected", "true");
    } else if (value === 0) {
        sel_incorrect.setAttribute("selected", "true");
    }
    add_attributes_to_element(sel, attr, classList, eventList);
    return sel;
}
/* Функция для выбора типа ответа(правильный или неправильный) с label'ом*/
function create_select_answer_type_with_label(title, value, attr = {}, classList = [], eventList = {}) {
    let div = document.createElement("div");
    let answer_type = create_select_answer_type(value, attr, classList, eventList);
    let label = create_label(title, attr.id);
    div.append(label, answer_type);
    return div;
}
/* Функция для создания формы создания или изменения ответа на вопрос*/
function create_form_add_question_answer(quiz, question, answer = null) {
    let form = document.createElement("form");

    form.append(create_input_with_label("Текст ответа", "text", "answer_text", answer ? answer.answer_text : "", "answer_text", ["data_to_send"]));

    form.append(create_input_with_label("Количество баллов за ответ", "text", "answer_points", answer ? answer.answer_points : "", "answer_points", ["data_to_send"]));

    form.append(create_input("hidden", "question_id", question.id, "question_id", ["data_to_send"]));

    form.append(create_input_with_label("Номер ответа", "text", "answer_number", answer ? answer.answer_number : "", "answer_number", ["data_to_send"]));

    form.append(create_select_answer_type_with_label("Правильный ответ на вопрос", answer ? answer.answer_correct : 2, { id: "answer_correct", type: "checkbox", name: "answer_correct" }, ["data_to_send"]))

    let create_answer_button = document.createElement("button");
    create_answer_button.type = "submit";
    if (answer) {
        create_answer_button.append("Изменить вариант ответа");
    }
    else {
        create_answer_button.append("Добавить вариант ответа");
    }
    form.append(create_answer_button);
    let error_message = document.createElement("div");
    let url = "/question/answer/add";
    let method = "POST";
    let success_function = () => show_one_my_question(quiz, question, "Ответ успешно добавлен");
    if (answer) {
        url = "/question/answer/" + answer.id + "/update";
        method = "PUT";
        success_function = () => show_one_question(quiz, question, "Ответ успешно обновлен");
    }
    form.setAttribute("method", method);
    let submit_form = create_submit_function(success_function, function (json) {
        if (json.error) {
            error_message.innerHTML = json.error;
            alert(json.error);
        }
    }, url);
    form.onsubmit = submit_form;
    form.setAttribute("action", url);
    return form;
}
/* Функция отправки запроса для начала сессии*/
function start_session(quiz, success_func, fail_func) {
    let user_id = get_cookie("user_id");
    let quiz_id = quiz.id;
    console.log(quiz_id);
    let url = "/session/user/" + user_id + "/start_quiz/" + quiz_id + "/";
    let method = "POST";
    let response = fetch(url, { "method": method });
    response.then(r => r.json()).then(function (data) {
        if (data.success) {
            success_func(data);
        }
        else {
            fail_func(data);
        }
    })
}
/* Функция для отрисовки ответо на вопрос для сессии*/
function create_session_question_answer(data) {
    console.log(data);
    if (!data.question_with_choice) {
        return create_element("textarea", "", {}, ["data_to_send"]);
    }
    else if (data.question_multiple_choice) {
        let ul = document.createElement("ul");
        data.answer_list.forEach(item => {
            ul.append(create_element("li", create_input_with_label(item.answer_text, "checkbox", "ans_" + item.id, item.id, "ans_" + item.id, ["data_to_send"])));
        });
        return ul;
    }
    else {
        let ul = document.createElement("ul");
        data.answer_list.forEach(item => {
            ul.append(create_element("li", create_input_with_label(item.answer_text, "radio", "answer", item.id, "ans_" + item.id, ["data_to_send"])));
        });
        return ul;
    }
}
/* Функция для отправки запроса для удаления теста*/
function delete_my_test(quiz_id, success_func, fail_func) {
    let url = "/quiz/" + quiz_id + "/delete";
    let method = "DELETE";
    let response = fetch(url, { "method": method });
    response.then(r => r.json()).then(function (data) {
        if (data.success) {
            success_func(data);
        }
        else {
            fail_func(data);
        }
    })
}
/* Функция для отправки запроса для удаления вопроса*/
function delete_my_question(question_id, success_func, fail_func, quiz, question) {
    let url = "/question/" + question_id + "/delete";
    let method = "DELETE";
    let response = fetch(url, { "method": method });
    response.then(r => r.json()).then(function (data) {
        if (data.success) {
            success_func("", quiz);
        }
        else {
            fail_func(data);
        }
    })
}
/* Функция для отправки запроса для получения списка всех тестов*/
function load_test_list(insert_function) {
    let url = "/quiz/all";
    let response = fetch(url);
    response.then(r => r.json()).then(function (data) {
        data.data.forEach(function (item) {
            insert_function(item);
        });
    });
}
/* Функция для отправки запроса для получения списка всех вопросов к тесту*/
function load_question_list(insert_function, quiz) {
    let quiz_id = (typeof quiz == "object") ? quiz.id : quiz;
    let url = "/quiz/" + quiz_id + "/question_list";
    let response = fetch(url);
    response.then(r => r.json()).then(function (data) {
        data.data.forEach(function (item) {
            insert_function(item);
        });
    })
}
/* Функция для отправки запроса для получения списка всех вопросов к сессии для показа результатов пользователю*/
function load_question_list_for_session(insert_function, session) {
    let session_id = session.session_id;
    let url = "/questions_for_session/" + session_id;
    let response = fetch(url);
    response.then(r => r.json()).then(function (data) {
        data.data.forEach(function (item) {
            insert_function(item);
        });
    })
}
/* Функция для отправки запроса для получения списка всех вопросов к сессии для показа статистики создателю теста*/
function load_question_list_for_session_creator(insert_function, session) {
    let session_id = session.session_id;
    let url = "/question_for_session_creator/" + session_id;
    let response = fetch(url);
    response.then(r => r.json()).then(function (data) {
        data.data.forEach(function (item) {
            insert_function(item);
        });
    })
}
/* Функция для отправки запроса для получения списка всех ответов к вопросу*/
function load_answer_list(insert_function, question) {
    let question_id = question.id;
    let url = "/question/" + question_id + "/answer_list";
    let response = fetch(url);
    response.then(r => r.json()).then(function (data) {
        data.data.forEach(function (item) {
            insert_function(item);
        });
    })
}
/* Функция для отображения одного теста в списке*/
function create_item_test_list(item, eventList = {}) {
    let li = document.createElement("li");
    let quiz_name = document.createElement("div");
    for (let key in eventList) {
        quiz_name.addEventListener(key, eventList[key]);
    }
    let quiz_description = document.createElement("div");
    quiz_name.append(item.quiz_name);
    let description = item.quiz_description;
    if (description.length > 40) {
        description = description.substring(0, 40) + "...";
    }
    quiz_description.append(description);
    quiz_description.onclick = function () {
        quiz_description.innerHTML = item.quiz_description;
    }
    li.append(quiz_name, quiz_description);
    return li
}
/* Функция для отображения одной сессии в списке результатов*/
function create_item_session_list(session, eventList = {}) {
    let field_session = my_session_field();
    let one_session = document.createElement("li");
    for (let key in field_session) {
        let div = document.createElement("div");
        let title = document.createElement("span");
        title.classList.add("session-field-title");
        title.append(field_session[key]);
        div.append(title);
        let value = document.createElement("span");
        if (key != 'beginning_time') {
            value.append(session[key]);
        }
        else {
            value.append(formatDate(session[key], "ru-datetime"));
        }
        div.append(value);
        one_session.append(div);
    }
    for (let key in eventList) {
        one_session.addEventListener(key, eventList[key]);
    }
    return one_session;
}
/* Функция для отображения одной сессии в списке статистики на тест*/
function create_item_statistics_session_list(session, eventList = {}) {
    let field_session = my_statistics_field();
    let one_session = document.createElement("li");
    for (let key in field_session) {
        let div = document.createElement("div");
        let title = document.createElement("span");
        title.classList.add("session-field-title");
        title.append(field_session[key]);
        div.append(title);
        let value = document.createElement("span");
        if (key != 'beginning_time') {
            value.append(session[key]);
        }
        else {
            value.append(formatDate(session[key], "ru-datetime"));
        }
        div.append(value);
        one_session.append(div);
    }
    for (let key in eventList) {
        one_session.addEventListener(key, eventList[key]);
    }
    return one_session;
}
/* Функция для отображения средних реузльтатов на тест и количества попыток*/
function create_med_res_and_session_am(item) {
    let field_session = med_res_and_session_am();
    let sessions_med = document.createElement("div");
    for (let key in field_session) {
        let div = document.createElement("div");
        let title = document.createElement("span");
        title.classList.add("session-field-title");
        title.append(field_session[key]);
        div.append(title);
        let value = document.createElement("span");
        value.append(item[key]);
        div.append(value);
        sessions_med.append(div);
    }
    return sessions_med;
}
/* Функция для отображения одного вопроса в списке*/
function create_item_question_list(item, eventList = {}) {
    console.log(item);
    let li = document.createElement("li");
    let question_text = document.createElement("div");
    for (let key in eventList) {
        question_text.addEventListener(key, eventList[key]);
    }
    question_text.append(item.question_text);
    li.append(question_text);
    console.log(item.question_description);
    if (item.question_description) {
        let question_description = document.createElement("div");
        let description = item.question_description;
        if (description.length > 40) {
            description = description.substring(0, 40) + "...";
        }
        question_description.append(description);
        question_description.onclick = function () {
            question_description.innerHTML = item.question_description;
        }
        li.append(question_description);
    }

    return li
}
/* Функция для отображения одного вопроса в результатах сессий*/
function create_item_question_session_list(session) {
    let field_session = one_question_session_field();
    let one_session = document.createElement("li");
    for (let key in field_session) {
        let div = document.createElement("div");
        let title = document.createElement("span");
        title.classList.add("session-field-title");
        title.append(field_session[key]);
        div.append(title);
        let value = document.createElement("span");
        value.append(session[key]);
        div.append(value);
        one_session.append(div);
    }
    return one_session;
}
/* Функция для отображения одного вопроса в статистике сессий*/
function create_item_question_session_list_creator(session, eventList = {}) {
    let field_session = one_question_session_field_creator();
    let one_session = document.createElement("li");
    for (let key in field_session) {
        let div = document.createElement("div");
        let title = document.createElement("span");
        title.classList.add("session-field-title");
        title.append(field_session[key]);
        div.append(title);
        let value = document.createElement("span");
        value.append(session[key]);
        div.append(value);
        one_session.append(div);
    }
    for (let key in eventList) {
        one_session.addEventListener(key, eventList[key]);
    }
    console.log(one_session);
    return one_session;
}
/* Функция для отображения одного ответа на вопрос*/
function create_item_answer_list(item, eventList = {}) {
    console.log(item);
    let li = document.createElement("li");
    let answer_text = document.createElement("div");
    for (let key in eventList) {
        answer_text.addEventListener(key, eventList[key]);
    }
    answer_text.append(item.answer_text);
    return li
}
/* Функция для отправки запроса для получения списка всех тестов принадлежащих пользователю*/
function load_my_test_list(insert_function, fail_function) {
    let index = get_cookie("user_id");
    let url = "/quiz/all/" + index;
    let response = fetch(url);
    response.then(r => r.json()).then(function (data) {
        if (data.success) {
            data.data.forEach(function (item) {
                insert_function(item);
            });
        }
        else {
            fail_function(data);
        }
    });
}
/* Функция для отправки запроса для получения списка всех сессий пользователя*/
function load_my_session_list(insert_function, fail_function) {
    let index = get_cookie("user_id");
    let url = "/session_list/" + index;
    let method = "GET";
    let response = fetch(url, { "method": method });
    response.then(r => r.json()).then(function (data) {
        if (data.success) {
            data.data.forEach(function (item) {
                insert_function(item);
            });
        }
        else {
            fail_function(data);
        }
    });
}
/* Функция для отправки запроса для получения списка всех сессий */
function load_my_statistics_list(insert_function, fail_function, quiz) {
    let index = get_cookie("user_id");
    console.log(quiz);
    let quiz_id = quiz.id;
    let url = "/all_sessions/" + index + "/" + quiz_id;
    let method = "GET";
    let response = fetch(url, { "method": method });
    response.then(r => r.json()).then(function (data) {
        if (data.success) {
            data.data.forEach(function (item) {
                insert_function(item);
            });
        }
        else {
            fail_function(data);
        }
    });
}
/* Функция для отправки запроса для получения среднего результата и количества сессий на тест */
function load_medium_result_and_tries_amount(insert_function, fail_function, quiz) {
    let quiz_id = quiz.id;
    let url = "/get_session_results_and_amount/" + quiz_id;
    let method = "GET";
    let response = fetch(url, { "method": method });
    response.then(r => r.json()).then(function (data) {
        if (data.success) {
            console.log(data.data);
            insert_function(data.data);
        }
        else {
            fail_function(data);
        }
    });
}
/* Функция для создания полей для "моих сессий" */
function my_session_field() {
    return {
        'quiz_name': 'Название теста',
        'beginning_time': 'Время начала сессии',
        'session_id': 'Id сессии',
        'result': 'Результат попытки',
    }
}
/* Функция для создания полей для статистики */
function my_statistics_field() {
    return {
        'quiz_name': 'Название теста',
        'quiz_id': 'Id теста',
        'user_email': 'Почта пользователя',
        'user_id': 'Id пользователся',
        'beginning_time': 'Время начала сессии',
        'session_id': 'Id сессии',
        'result': 'Результат попытки',
    }
}
/* Функция для создания полей для среднего результата и кол-ва попыток */
function med_res_and_session_am() {
    return {
        'medium_result': "Средний результат",
        'session_amount': "Количество попыток"
    }
}
/* Функция для создания полей для теста*/
function get_quiz_field() {
    return {
        'quiz_name': 'Название теста',
        'quiz_description': 'Описание теста',
        'id': 'Id теста',
        'duration': 'Время на прохождение теста',
        'created_date': 'Дата создания',
        'question_amount': 'Количество вопросов',
        'questions_amount_to_complete': 'Количество вопросов необходимое для завершения',
        'quiz_tries': 'Количество попыток на тест',
        'show_ans_res': 'Возможность увидеть правильность ответов после прохождения теста',
        'mark_type': 'Тип оценивания теста',
        'question_switch': 'Возможность переключения между вопросами',
        'reanswer': 'Возможность дать потворный ответ на вопрос'
    }
}
/* Функция для создания полей для сессии в результатах*/
function get_session_field() {
    return {
        'quiz_name': 'Название теста',
        'quiz_id': 'Id теста',
        'beginning_time': 'Время начала сессии',
        'finishing_time': 'Время окончания сесии',
        'total_time': 'Время затраченное на попытку',
        'result': 'Результат попытки',
        'session_id': 'Id сессии',
    }
}
/* Функция для создания полей для сессии в статистике*/
function get_statistics_field() {
    return {
        'quiz_name': 'Название теста',
        'quiz_id': 'Id теста',
        "user_email": 'Почта пользователя',
        "user_id": 'Id пользователя',
        'beginning_time': 'Время начала сессии',
        'finishing_time': 'Время окончания сесии',
        'total_time': 'Время затраченное на попытку',
        'result': 'Результат попытки',
        'session_id': 'Id сессии',
    }
}
/* Функция для создания полей для вопроса*/
function get_question_field() {
    return {
        "question_text": "Текст вопроса",
        "question_description": "Описание вопроса",
        "id": "Id вопроса",
        "question_time": "Время на вопрос",
        "question_points": "Количество баллов за вопрос",
        "question_type": "Тип вопроса",
        "quiz_id": "Id теста которому принадлежит вопрос",
        "question_number": "Номер вопроса в тесте",
        "question_difficulty": "Сложность вопроса",
        "question_hint": "Наличие подсказки"
    }
}
/* Функция для создания полей для ответа*/
function get_answer_field() {
    return {
        "answer_text": "Текст ответа",
        "question_id": "Id вопроса которому принадлежит ответ",
        "id": "Id ответа",
        "answer_number": "Номер вопроса",
        "answer_points": "Количество баллов за вопрос",
        "answer_correct": "Правильный ответ на вопрос"
    }
}
/* Функция для создания полей для вопроса в сесии в результатах*/
function one_question_session_field() {
    return {
        "question_number": "Номер вопроса",
        "question_points": "Баллы за ответ"
    }
}
/* Функция для создания полей для вопроса в сесии в статистике*/
function one_question_session_field_creator() {
    return {
        "question_number": "Номер вопроса",
        "question_text": "Текст вопроса",
        "question_points": "Баллы за ответ",
    }
}
/* Функция для создания полей для вопроса в сесии в статистике при нажатии*/
function get_question_session_field() {
    return {
        "question_text": "Текст вопроса",
        "user_answer": "Ответ пользователя",
        "question_points": "Баллы за ответ",
    }
}
function create_answer_view(answer_structure) {
    let field_list = get_answer_field();
    let answer = document.createElement("div");
    for (let key in field_list) {
        let div = document.createElement("div");
        let title = document.createElement("span");
        title.classList.add("answer_structure-field-title");
        title.append(field_list[key]);
        div.append(title);
        let value = document.createElement("span");
        if (key != 'answer_correct') {
            value.append(answer_structure[key]);
        }
        else {
            value.append(answer_structure[key] ? "Да" : "Нет")
        }
        div.append(value);
        answer.append(div);
    }
    answer.classList.add("answer_padding");
    return answer;
}
function create_question_view(question_structure) {
    let field_list = get_question_field();
    let question = document.createElement("div");
    for (let key in field_list) {
        let div = document.createElement("div");
        let title = document.createElement("span");
        title.classList.add("question_structure-field-title");
        title.append(field_list[key]);
        div.append(title);
        let value = document.createElement("span");
        value.append(question_structure[key]);
        div.append(value);
        question.append(div);
    }
    return question;
}
function create_test_view(quiz) {
    let field_list = get_quiz_field();
    let test = document.createElement("div");
    for (let key in field_list) {
        let div = document.createElement("div");
        let title = document.createElement("span");
        title.classList.add("quiz-field-title");
        title.append(field_list[key]);
        div.append(title);
        let value = document.createElement("span");
        if (key != 'created_date') {
            value.append((quiz[key] === true || quiz[key] === false) ? (quiz[key] ? "Да" : "Нет") : quiz[key]);
        }
        else {
            value.append(formatDate(quiz[key], "ru-long"));
        }
        div.append(value);
        test.append(div);
    }
    return test;
}
function create_one_question_statistics_view(session) {
    let field_session = get_question_session_field();
    let one_session = document.createElement("div");
    for (let key in field_session) {
        let div = document.createElement("div");
        let title = document.createElement("span");
        title.classList.add("session-field-title");
        title.append(field_session[key]);
        div.append(title);
        let value = document.createElement("span");
        value.append(session[key]);
        div.append(value);
        one_session.append(div);
    }
    return one_session;
}
function create_session_view(session) {
    let field_session = get_session_field();
    let one_session = document.createElement("div");
    for (let key in field_session) {
        let div = document.createElement("div");
        let title = document.createElement("span");
        title.classList.add("session-field-title");
        title.append(field_session[key]);
        div.append(title);
        let value = document.createElement("span");
        if (key == 'total_time') {
            value.append(formatTime(session[key]));
        }
        else if (key != 'beginning_time' && key != 'finishing_time') {
            value.append(session[key]);
        }
        else {
            value.append(formatDate(session[key], "ru-datetime-seconds"));
        }
        div.append(value);
        one_session.append(div);
    }
    return one_session;
}
function create_session_statistics_view(session) {
    let field_session = get_statistics_field();
    let one_session = document.createElement("div");
    for (let key in field_session) {
        let div = document.createElement("div");
        let title = document.createElement("span");
        title.classList.add("session-field-title");
        title.append(field_session[key]);
        div.append(title);
        let value = document.createElement("span");
        if (key == 'total_time') {
            value.append(formatTime(session[key]));
        }
        else if (key != 'beginning_time' && key != 'finishing_time') {
            value.append(session[key]);
        }
        else {
            value.append(formatDate(session[key], "ru-datetime-seconds"));
        }
        div.append(value);
        one_session.append(div);
    }
    return one_session;
}
function load_one_test(quiz_id, success_func, fail_func) {
    let url = "/quiz/" + quiz_id;
    let response = fetch(url);
    response.then(r => r.json()).then(function (data) {
        if (data.success) {
            success_func(data);
        }
        else {
            fail_func(data);
        }
    });
}
function show_one_my_test(quiz_id) {
    load_one_test(quiz_id, (json) => {
        let quiz = json.data;
        show_one_test(json.data, [create_button_edit_test(quiz), create_button_delete_test(quiz), create_button_questions(quiz), create_button_back_to_my_quiz_list_menu()]);
    }, (json) => console.log(json));
}

function show_one_test(quiz, buttonlist = []) {
    let content = get_main_content(["left-padding", "container_with_button"])
    let container = document.createElement("div");
    container.append(create_test_view(quiz));
    buttonlist.forEach(btn => container.append(btn));
    content.append(container);
}
function show_one_session_statistics_creator(session, buttonlist = []) {
    let content = get_main_content(["left-padding"])
    let container = document.createElement("div");
    container.append(create_one_question_statistics_view(session));
    buttonlist.forEach(btn => container.append(btn));
    content.append(container);
}
function show_one_session(session, buttonlist) {
    let content = get_main_content(["left-padding"])
    let container = document.createElement("div");
    container.append(create_session_view(session));
    buttonlist.forEach(btn => container.append(btn));
    content.append(container);
    show_questions_list_for_session(session);
}
function show_one_session_statistics(session) {
    let content = get_main_content(["left-padding"])
    let container = document.createElement("div");
    container.append(create_session_statistics_view(session));
    content.append(container);
    content.append(create_questions_list_for_session_creator(session));
    content.append(create_button_back_to_main_menu());
}
function show_one_question(question, buttonlist = [], message = null) {
    let content = get_main_content(["left-padding", "container_with_button"])
    if (message) {
        content.append(create_element("div", message));
    }
    let container = document.createElement("div");
    let ul = document.createElement("ul");
    container.append(create_question_view(question));
    container.append(ul);
    load_answer_list(function (item) {
        ul.append(create_answer_view(item));
    }, question);
    buttonlist.forEach(btn => container.append(btn));
    content.append(container);
}
function show_one_my_question(quiz, question, message = null) {
    show_one_question(question, [create_button_questions(question.quiz_id), create_button_add_answer(quiz, question), create_button_edit_question(quiz, question), create_button_delete_question(quiz, question)], message);

}
function show_one_answer(answer, buttonlist = []) {
    let content = get_main_content(["left-padding", "container_with_button"])
    let container = document.createElement("div");
    container.append(create_answer_view(answer));
    buttonlist.forEach(btn => container.append(btn));
    content.append(container);
}
function get_question_by_id(question_id, success_func, fail_func) {
    let method = "GET";
    let url = "/question/" + question_id;
    let response = fetch(url, { "method": method });
    response.then(r => r.json()).then(function (data) {
        if (data.success) {
            return success_func(data);
        }
        else {
            return fail_func(data);
        }
    })
}
function show_question(data) {
    let content = get_main_content(["left-padding", "container_with_button"])
    let container = document.createElement("div");
    container.append(data);
    // buttonlist.forEach(btn=>container.append(btn));
    content.append(container);
}
function create_button_log_out() {
    return create_button("Выйти из аккаунта", {}, [], {
        "click": (e) => {
            e.preventDefault();
            show_login_form();
        }
    });
}
function create_button_edit_test(quiz) {
    return create_button("Изменить", {}, [], {
        "click": (e) => {
            e.preventDefault();
            show_form_edit_test(quiz);
        }
    });
}
function create_button_edit_question(quiz, question) {
    return create_button("Изменить", {}, [], {
        "click": (e) => {
            e.preventDefault();
            show_form_edit_question(quiz, question);
        }
    });
}
function create_button_back_to_main_menu() {
    return create_button("Вернуться в главное меню", {}, [], {
        "click": (e) => {
            e.preventDefault();
            show_main_menu("");
        }
    });
}
function create_button_back_to_results() {
    return create_button("Вернуться к результатам", {}, [], {
        "click": (e) => {
            e.preventDefault();
            show_my_session_list();
        }
    });
} function create_button_back_to_results_creator(quiz_id) {
    return create_button("Вернуться к результатам", {}, [], {
        "click": (e) => {
            e.preventDefault();
            let method = "GET";
            let url = "/quiz/" + quiz_id
            let response = fetch(url, { "method": method });
            response.then(r => r.json()).then(function (data) {
                if (data.success) {
                    return show_statistics_list_for_quiz(data.data);
                }
                else {
                    return console.log(data.data);
                }
            })
        }
    });
}
function create_button_back_to_my_quiz_list_menu() {
    return create_button("Вернуться к списку тестов", {}, [], {
        "click": (e) => {
            e.preventDefault();
            show_my_tests_list();
        }
    });
}
function create_button_back_to_my_quiz_session_list_menu() {
    return create_button("Вернуться к списку тестов", {}, [], {
        "click": (e) => {
            e.preventDefault();
            show_statistics_list();
        }
    });
}
function create_button_back_to_menu_my_test_creation() {
    return create_button("Вернуться", {}, [], {
        "click": (e) => {
            e.preventDefault();
            show_my_tests_menu();
        }
    });
}
function get_next_question_by_session(session_id, success_func, fail_func) {
    console.log(session_id);
    let method = "GET";
    let url = "/get_next_question/" + session_id;
    let response = fetch(url, { "method": method });
    response.then(r => r.json()).then(function (data) {
        if (data.success) {
            return success_func(data);
        }
        else {
            return fail_func(data);
        }
    })
}
function show_number_of_question_session(data) {
    let question_number = data.question_number + 1
    let question_total_amount = data.question_total_amount
    let now_question_number_total_amount = question_number + "/" + question_total_amount
    let div = document.createElement("div");
    div.append(now_question_number_total_amount);
    div.classList.add("question_number")
    return div
}
function show_session_question(json) {
    let content = get_main_content(["left-padding", "quiz_session"])
    let container = document.createElement("div");
    content.append(show_number_of_question_session(json.data));
    container.append(json.data.question_text);
    content.append(container);
    content.append(create_session_question_answer(json.data));
    if (json.data.question_hint != "") {
        let div = document.createElement("div");
        div.classList.add("btn_show_hint_div");
        div.append(create_button_show_hint(json.data.question_hint));
        content.append(div);
    }
    if (json.data.question_number + 1 == json.data.question_total_amount) {
        content.append(create_button_commit_session(json.data.session_id));
        return;
    }
    content.append(create_button_show_next_question(json.data.session_id));
    console.log(json.data)
}
function process_success_start_session_request(json) {
    get_next_question_by_session(json.data.session_id, show_session_question, (json) => console.log(json))
}
function end_session(session_id) {
    let method = "POST";
    let url = "/end_session/" + session_id;
    let response = fetch(url, { "method": method });
    response.then(r => r.json()).then(function (data) {
        if (data.success) {
            return show_main_menu("Тестирование завершено");
        }
        else {
            return console.log(data);
        }
    })
}
function send_user_answer_on_server(listanswers, textanswer, success_func) {
    let method = "POST";
    let url = "/set_answers/";
    send_request(method, url, { "answers": listanswers, "text_answer": textanswer }, success_func, (data) => alert("Что-то пошло не так"));
}
function create_button_commit_session(session_id) {
    return create_button("Завершить тест", {}, [], {
        "click": (e) => {
            e.preventDefault();
            send_user_answer(() => end_session(session_id));
        }
    });
}
function send_user_answer(success_func) {
    let text = session_get_answer_textarea();
    let list_answers = session_get_answer_checkbox_and_radio();
    console.log(text, list_answers);
    if (!text && list_answers.length == 0) {
        alert("Вы не ответили на вопрос");
        return false;
    }
    send_user_answer_on_server(list_answers, text, success_func)
    return true;
}
function create_button_show_next_question(session_id) {
    return create_button("Следующий вопрос", {}, [], {
        "click": (e) => {
            e.preventDefault();
            send_user_answer(() => get_next_question_by_session(session_id, show_session_question, (json) => console.log(json)));
        }
    });
}
function session_get_answer_textarea() {
    let textarea = document.querySelector("textarea");
    if (!textarea) {
        return null
    }
    return textarea.value;
}
function session_get_answer_checkbox_and_radio() {
    let input_list = document.querySelectorAll("input");
    let list_result = [];
    input_list.forEach(item => {
        if (item.checked) {
            list_result.push(item.value);
        }
    });
    return list_result;
}
function create_button_show_hint(question_hint) {
    return create_button("Показать подсказку", {}, ["btn_show_hint"], {
        "click": (e) => {
            e.preventDefault();
            let buttonElement = e.target;
            buttonElement.style.display = "none";
            buttonElement.parentElement.append(question_hint);
        }
    })
}
function create_button_start_test(quiz) {
    return create_button("Начать тест", {}, [], {
        "click": (e) => {
            e.preventDefault();
            start_session(quiz, process_success_start_session_request, (json) => console.log(json));
        }
    });
}
function create_button_leave_test(quiz) {
    return create_button("Вернуться к тестам", {}, [], {
        "click": (e) => {
            e.preventDefault();
            show_tests_list_with_button();
        }
    });
}
function create_button_delete_test(quiz) {
    return create_button("Удалить тест", {}, [], {
        "click": (e) => {
            e.preventDefault();
            delete_my_test(quiz.id, show_my_tests_list, (json) => console.log(json));
        }
    });
}
function create_button_delete_question(quiz, question) {
    return create_button("Удалить вопрос", {}, [], {
        "click": (e) => {
            e.preventDefault();
            delete_my_question(question.id, show_questions_list_for_quiz, (json) => console.log(json), quiz, question);
        }
    });
}
function create_button_questions(quiz) {
    return create_button("Вопросы к тесту", {}, [], {
        "click": (e) => {
            e.preventDefault();
            show_questions_list_for_quiz(e, quiz);
        }
    });
}
function create_button_answers(quiz, question) {
    return create_button("Ответы к вопросу", {}, [], {
        "click": (e) => {
            e.preventDefault();
            show_answer_list_for_question(e, question);
        }
    });
}
function create_button_add_question(quiz, question = null) {
    return create_button("Добавить вопрос", {}, [], {
        "click": (e) => {
            e.preventDefault();
            show_form_add_question(quiz, question);
        }
    });
}
function create_button_add_answer(quiz, question, answer = null) {
    return create_button("Добавить ответ", {}, [], {
        "click": (e) => {
            e.preventDefault();
            show_form_add_answer(quiz, question, answer);
        }
    });
}
function create_button_back_to_quiz(quiz) {
    return create_button("Вернуться к тесту", {}, [], {
        "click": (e) => {
            e.preventDefault();
            show_one_test(quiz, [create_button_edit_test(quiz), create_button_delete_test(quiz), create_button_questions(quiz), create_button_back_to_my_quiz_list_menu()]);
        }
    });
}
function create_button_back_to_question(question) {
    return create_button("Вернуться к вопросу", {}, [], {
        "click": (e) => {
            e.preventDefault();
            show_one_test(question);
        }
    });
}
function create_button_add_points(session) {
    return create_button("Добавить баллы", {}, [], {
        "click": (e) => {
            e.preventDefault();
        }
    });
}
function show_change_points(session, session_result_question) {
    const textarea = document.createElement('textarea');
    textarea.value = session_result_question.question_points;
    console.log(session);
    const saveButton = create_button("Сохранить изменения", {}, [], {
        "click": () => {
            let method = "POST";
            let url = "/set_points/" + session.session_id + "/" + session_result_question.question_number;
            let body = { "points": textarea.value };
            send_request(method, url, body, () => {
                let url = "/get_session_by_id/" + session.session_id;
                send_request("GET", url, {}, (json) => show_one_session_statistics(json.data), (data) => alert("Что-то пошло не так"))
            }, (data) => alert("Что-то пошло не так"));
        }
    });
    content = document.getElementById("main_content");
    content.append(textarea);
    content.append(saveButton);
}
function show_questions_list_for_quiz(event, quiz) {
    if (event != "") {
        event.preventDefault();
    }
    let content = get_main_content(["left-padding", "container_with_button"])
    let ul = document.createElement("ul");
    load_question_list(function (item) {
        ul.append(create_item_question_list(item, {
            "click": (event) => {
                event.preventDefault();
                show_one_my_question(quiz, item);
            }
        }));
    }, quiz);
    content.append(ul, create_button_add_question(quiz), create_button_back_to_quiz(quiz));
}
function show_questions_list_for_session(session) {
    content = document.getElementById("main_content");
    let ul = document.createElement("ul");
    ul.classList.add("question_results");
    load_question_list_for_session(function (item) {
        ul.append(create_item_question_session_list(item));
    }, session);
    content.append(ul, create_button_back_to_results());
}
function create_questions_list_for_session_creator(session) {
    let ul = document.createElement("ul");
    load_question_list_for_session_creator(function (item) {
        ul.append(create_item_question_session_list_creator(item, {
            "click": (event) => {
                event.preventDefault();
                show_one_session_statistics_creator(item, [create_button_back_to_results_creator(session.quiz_id)]);
                if (!item.answer_checked) {
                    show_change_points(session, item);
                }
            }
        }));
    }, session);
    return ul;
}
function show_answer_list_for_question(event, quiz, question) {
    event.preventDefault();
    let content = get_main_content(["left-padding", "container_with_button"])
    let ul = document.createElement("ul");
    load_answer_list(function (item) {
        ul.append(create_item_answer_list(item, {
            "click": (event) => {
                event.preventDefault();
                console.log("НЕГРЫ ПИДОРЫ");
            }
        }));
    }, question);
    content.append(ul, create_button_add_answer(quiz, question), create_button_back_to_question(question));
}
function show_tests_list() {
    let content = get_main_content(["left-padding", "show_tests_list"])
    let ul = document.createElement("ul");
    load_test_list(function (item) {
        ul.append(create_item_test_list(item, {
            "click": (event) => {
                event.preventDefault();
                show_one_test(item, [create_button_start_test(item), create_button_leave_test(item)]);
            }
        }));
    });
    content.append(ul);
}
function show_tests_list_with_button() {
    show_tests_list();
    content = document.getElementById("main_content");
    content.append(create_button_back_to_main_menu());
}
function show_my_session_list() {
    let content = get_main_content(["left-padding"])
    let ul = document.createElement("ul");
    load_my_session_list(function (item) {
        ul.append(create_item_session_list(item, {
            "click": (event) => {
                event.preventDefault();
                show_one_session(item, []);
            }
        }));
    }, function (data) {
        console.log(data);
        alert(data.error);
        content.innerHTML = data.error;
    });
    content.append(ul);
    content.append(create_button_back_to_main_menu());
}
function show_statistics_list() {
    let content = get_main_content(["left-padding"])
    let ul = document.createElement("ul");
    load_my_test_list(function (item) {
        ul.append(create_item_test_list(item, {
            "click": (event) => {
                event.preventDefault();
                show_statistics_list_for_quiz(item);
                console.log(item);
                console.log(item);
            }
        }));
    }, function (data) {
        console.log(data);
        alert(data.error);
        content.innerHTML = data.error;
    });
    content.append(ul);
    content.append(create_button_back_to_menu_my_test_creation());
}
function show_statistics_list_for_quiz(quiz) {
    let content = get_main_content(["left-padding"])
    let ul = document.createElement("ul");
    load_my_statistics_list(function (item) {
        ul.append(create_item_statistics_session_list(item, {
            "click": (event) => {
                event.preventDefault();
                show_one_session_statistics(item);
            }
        }));
    }, function (data) {
        console.log(data);
        alert(data.error);
        content.innerHTML = data.error;
    }, quiz);
    let medium_result = document.createElement("div");
    medium_result.classList.add("margin-bottom")
    load_medium_result_and_tries_amount(function (data) {
        medium_result.append(create_med_res_and_session_am(data));
    }, function (data) {
        console.log(data);
        alert(data.error);
        content.innerHTML = data.error;
    }, quiz)
    content.append(medium_result);
    content.append(ul);
    content.append(create_button_back_to_my_quiz_session_list_menu());
}
function show_my_tests_list() {
    let content = get_main_content(["left-padding"])
    let ul = document.createElement("ul");
    load_my_test_list(function (item) {
        ul.append(create_item_test_list(item, {
            "click": (event) => {
                event.preventDefault();
                show_one_test(item, [create_button_edit_test(item), create_button_delete_test(item), create_button_questions(item), create_button_back_to_my_quiz_list_menu()]);
            }
        }));
    }, function (data) {
        console.log(data);
        alert(data.error);
        content.innerHTML = data.error;
    });
    content.append(ul);
    content.append(create_button_back_to_menu_my_test_creation())
}
function show_my_tests_list_click(event) {
    event.preventDefault();
    show_my_tests_list();
    // content = document.getElementById("main_content");
    // content.append(create_button_back_to_menu_my_test_creation());
}
function show_form_add_test(event) {
    event.preventDefault();
    let content = get_main_content(["left-padding"])
    content.append(create_form_add_test());
    content.append(create_button_back_to_menu_my_test_creation());
}
function show_form_edit_test(quiz) {
    let content = get_main_content(["left-padding"])
    content.append(create_form_add_test(quiz));
}
function show_form_add_question(quiz_id, question = null) {
    let content = get_main_content(["left-padding"])
    content.append(create_form_add_question(quiz_id, question));
}
function show_form_edit_question(quiz_id, question) {
    let content = get_main_content(["left-padding"])
    content.append(create_form_add_question(quiz_id, question));
}
function show_form_add_answer(quiz, question, answer = null) {
    let content = get_main_content(["left-padding"])
    content.append(create_form_add_question_answer(quiz, question, answer));
}
function create_form_password() {
    let password_1 = create_input("password", "new_password", '', "new_password", ["data_to_send"]);
    let password_2 = create_input("password", "old_password", '', "old_password", ["data_to_send"]);
    let index = get_cookie("user_id");
    let url = "/user/update/" + index;
    let message_error = document.createElement("div");
    let submit_form = create_submit_function(() => show_my_profile(), function (json) {
        if (json.error) {
            message_error.innerHTML = json.error;
            alert(json.error);
        }
    });
    let form = create_form([password_1, password_2, create_button_save(), create_button_remove_form(), message_error], { action: url, method: "PUT" }, [], { "submit": submit_form });
    let div = document.createElement("div");
    div.append(form);
    div.classList.add("my_profile")
    return div;
}
function create_form_email() {
    let email = create_input("email", "mail", '', "mail", ["data_to_send"]);
    let index = get_cookie("user_id");
    let url = "/user/update/" + index;
    let submit_form = create_submit_function(() => show_my_profile(), () => { });
    let form = create_form([email, create_button_save(), create_button_remove_form()], { action: url, method: "PUT" }, [], { "submit": submit_form });
    let div = document.createElement("div");
    div.append(form);
    div.classList.add("my_profile")
    return div;
}
function get_data_from_form(form) {
    let list_data_to_send = form.querySelectorAll(".data_to_send");
    let result = {};
    list_data_to_send.forEach(item => {
        result[item.getAttribute("name")] = item.value;
    });
    return result;
}
function send_request(method, url, body, success_function, fail_function) {
    let option = {};
    if (method != "GET") {
        option = {
            method: method,
            body: JSON.stringify(body),
            headers: {
                "Content-type": "application/json; charset=UTF-8"
            }
        }
    }
    fetch(url, option)
        .then(response => response.json())
        .then(json => {
            if (json.success) {
                success_function(json);
            }
            else {
                fail_function(json);
            }
        })
}
function create_submit_function(success_function, fail_function) {
    return function (event) {
        event.preventDefault();
        console.log("submit_form");
        let form = event.target;
        let data = get_data_from_form(form);
        let action = form.getAttribute("action");
        let method = form.getAttribute("method");
        console.log(data);
        send_request(method, action, data, success_function, fail_function);
    }
}

function create_button_save() {
    return create_button("Сохранить", { "type": "submit" });
}
function create_button_remove_form() {
    return create_button("Отменить", { "type": "button" }, [], { "click": remove_form });
}
function remove_form(event) {
    event.preventDefault();
    let form = event.target.closest("form");
    form.remove();
}
function add_attributes_to_element(element, attr = {}, classList = [], eventList = {}) {
    element.classList.add(...classList);
    for (let key in attr) {
        element.setAttribute(key, attr[key]);
    }
    for (let key in eventList) {
        element.addEventListener(key, eventList[key]);
    }
}
function create_element(tag_name, content, attr = {}, classList = [], eventList = {}) {
    let element = document.createElement(tag_name);
    add_attributes_to_element(element, attr, classList, eventList);
    if (content) {
        if (Array.isArray(content)) {
            content.forEach(item => element.append(item));
        }
        else {
            element.append(content);
        }
    }
    return element;
}
function create_button(content, attr = {}, classList = [], eventList = {}) {
    return create_element("button", content, attr, classList, eventList);
}
function create_form(content, attr = {}, classList = [], eventList = {}) {
    return create_element("form", content, attr, classList, eventList);
}
function show_my_profile(event) {
    if (event) {
        event.preventDefault();
    }
    let content = get_main_content(["my_profile"]);
    let ul = document.createElement("ul");
    let now_email = document.createElement("li");
    let now_password = document.createElement("li");
    let user_email = get_cookie("user_email");
    user_email = user_email.slice(1, user_email.length - 1);
    let us_pas = "********";
    now_email.append(user_email);
    let change_email_button = document.createElement("button");
    change_email_button.type = "button";
    change_email_button.append("Изменить почту");
    let change_password_button = document.createElement("button");
    change_password_button.type = "button";
    change_password_button.append("Изменить пароль");
    now_email.append(change_email_button);
    now_password.append(us_pas);
    now_password.append(change_password_button);
    ul.append(now_email);
    ul.append(now_password);
    content.append(ul);
    change_email_button.onclick = function (e) {
        e.preventDefault();
        if (!now_email.querySelector("form")) {
            now_email.append(create_form_email());
        }
    }
    change_password_button.onclick = function (e) {
        e.preventDefault();
        if (!now_password.querySelector("form")) {
            now_password.append(create_form_password());
        }
    }
    content.append(create_button_log_out());
    content.append(create_button_back_to_main_menu());
}
function create_login_form() {
    let user_email = create_input("email", "mail", '', "mail", ["data_to_send"], {}, { "placeholder": "email" });
    let user_password = create_input("password", "password", '', "password", ["data_to_send"], {}, { "placeholder": "пароль" });
    let login_button = create_button("Войти", { "type": "submit" }, ["btn_login"]);
    let error_message = document.createElement("div");
    error_message.classList.add("max_width");
    let url = "/user/login/"
    let registrate_button = create_button("Зарегистрироваться", { "type": "button" }, ["btn_show_registration_form"], { "click": show_registration_form });
    let submit_form = create_submit_function(() => show_main_menu(), () => { });
    let form = create_form([user_email, user_password, login_button, error_message, registrate_button], { action: url, method: "POST" }, [], { "submit": submit_form });
    let div = document.createElement("div");
    div.append(form);
    return div;
}
function create_item_menu(item) {
    let div = document.createElement("div");
    div.append(item.label);
    div.onclick = item.action;
    return div;
}
function show_menu(func_get_list_item_menu, message = null) {
    let content = get_main_content(["top_center_content", "menu"]);
    let ul = document.createElement("ul");

    func_get_list_item_menu().forEach(item => {
        let li = document.createElement("li");
        li.append(create_item_menu(item));
        ul.append(li);
    });
    if (message != null && typeof (message) == "string") {
        let msg = document.createElement("div");
        msg.classList.add("information-message");
        msg.append(message);
        content.append(msg);
    }
    content.append(ul);
}
function show_my_tests_menu(event) {
    if (event) {
        event.preventDefault();
    }
    show_menu(get_list_item_my_tests_menu);
    let content = document.getElementById("main_content");
}
function show_main_menu(message = null) {
    show_menu(get_list_item_main_menu, message);
}
function show_error(container, message) {
    let error = container.querySelector('.error_message');
    if (error) {
        error.remove();
    }
    let span = document.createElement("span");
    span.classList.add("error_message");
    span.append(message);
    container.append(span);
}
function send_json_post_request(url, data, success_func, fail_func) {
    fetch(url, {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }).then(result => result.json()).then(json => {
        if (!json.success) {
            fail_func(json);
        }
        else {
            success_func(json);
        }
    });
}
function registration_function(event) {
    event.preventDefault();
    console.log(event);
    let form = event.target;
    let email = form.querySelector('[name="email"]');
    let password = form.querySelector('[name="password"]');
    let password_match = form.querySelector('[name="password_match"]');
    if (password.value != password_match.value) {
        show_error(form, "Пароли не совпадают");
        return;
    }
    let post_data = {
        "mail": email.value,
        "password": password.value
    };
    send_json_post_request("/user/add/", post_data, show_main_menu, (data) => show_error(form, data.detail))
}
function show_registration_form() {
    let content = get_main_content(["center_content","max_width"])
    let registration_form = document.createElement("form");
    let email = document.createElement("input");
    email.type = "email";
    email.setAttribute("name", "email");
    email.setAttribute("required", "true");
    email.setAttribute("placeholder", "email");
    let password = document.createElement("input");
    password.type = "password";
    password.setAttribute("name", "password");
    password.setAttribute("required", "true");
    password.setAttribute("placeholder", "пароль");
    let password_match = document.createElement("input");
    password_match.type = "password";
    password_match.setAttribute("name", "password_match");
    password_match.setAttribute("required", "true");
    password_match.setAttribute("placeholder", "повторный пароль");
    let registration_button = document.createElement("button");
    registration_button.type = "submit";
    registration_button.append("Зарегистрироваться");
    registration_form.append(email);
    registration_form.append(password);
    registration_form.append(password_match);
    registration_form.append(registration_button);
    registration_form.onsubmit = registration_function;
    content.append(registration_form);
}
function show_login_form() {
    let content = get_main_content(["center_content"]);
    content.append(create_login_form());
}
function get_main_content(classList = []) {
    let content = document.getElementById("main_content");
    content.innerHTML = "";
    content.className = "";
    content.classList.add(...classList);
    return content;
}
function check_registration() {
    console.log(document.cookie);
    const user_cookie = get_cookie("user_id");
    if (user_cookie != null) {
        show_main_menu();
    }
    else {
        show_login_form();
    }
}
