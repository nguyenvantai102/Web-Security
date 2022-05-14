if (document.querySelector(".errorlist .errorlist li")) {
    var error = document.querySelector(".errorlist .errorlist li").textContent;
    alert(error);    
}


// Đối tượng `Validator`
function Validator(options) {

    function getParentElement(element, selector) {
        
        while(element.parentElement) {
            if (element.parentElement.matches(selector)) 
                return element.parentElement;
            element = element.parentElement;
        }
    }

    var selectorRules = {};

    function Validate(inputElement, rule) {

        var errorElement = getParentElement(inputElement, options.formGroupSelector).querySelector(options.errorSelector);
        var errorMessage;
        // Lấy ra các rules của selector
        var rules = selectorRules[rule.selector];

        // Lặp qua từng rule và kiểm tra
        // Nếu có lỗi, dừng kiểm tra
        for (var i = 0; i < rules.length; i++) {
            switch(inputElement.type) {
                case 'radio':
                case 'checkbox':
                    errorMessage = rules[i](formElement.querySelector(rule.selector + ':checked'))
                    break;
                default:
                    errorMessage = rules[i](inputElement.value);
                }

            if (errorMessage)
                break;
        }

        if (errorMessage) {
            errorElement.innerText = errorMessage;
            getParentElement(inputElement, options.formGroupSelector).classList.add('invalid');
        }
        else {
            errorElement.innerText = '';
            getParentElement(inputElement, options.formGroupSelector).classList.remove('invalid');
        }
        return !errorMessage;
    }

    //Lấy element của form cần validate
    var formElement = document.querySelector(options.form);

    if (formElement) {
        //Ngăn chặn submit form khi input không hợp lệ
        formElement.onsubmit = function(e) {

            e.preventDefault();
            var isFormValid = true;
            //Lặp qua từng rules và validate
            options.rules.forEach(function (rule) {
                var inputElement = formElement.querySelector(rule.selector);
                var isValid = Validate(inputElement, rule);
                if (!isValid) {
                    isFormValid = false;
                }
            });
            
            
            if (isFormValid) {
                // Trường hợp submit với js
                if (typeof options.onSubmit === 'function') {

                    var enableInputs = formElement.querySelectorAll('[name]:not([disable])')

                    var formValues = Array.from(enableInputs).reduce(function (values, input) {
                        
                        switch (input.type) {
                            case 'radio':
                                values[input.name] = formElement.querySelector('input[name="' + input.name + '"]:checked').value;
                                break;
                            case 'checkbox':
                                if (!input.matches(':checked')) {
                                    values[input.name] = '';
                                    return values;
                                }
                                if (!Array.isArray(values[input.name])) {
                                    values[input.name] = [];
                                }
                                values[input.name].push(input.value);
                                break;
                            case 'file':
                                values[input.name] = input.files;
                                break;
                            default:
                                values[input.name] = input.value;
                        }
                        return values;
                }, {});

                    options.onSubmit(formValues);
                }
                // Trường hợp submit với hành vi mặc định
                else {
                    formElement.submit();
                }
            }
        }
        //Lặp qua mỗi lần lắng nghe sự kiện
        options.rules.forEach(function (rule) {

            // Lưu lại các rules cho mỗi input
            if (Array.isArray(selectorRules[rule.selector])) {
                selectorRules[rule.selector].push(rule.test);
            } 
            else {
                selectorRules[rule.selector] = [rule.test];
            }

            var inputElements = formElement.querySelectorAll(rule.selector);

            //Array .from để chuyển inputElements từ kiểu object(Nodelist) sang kiểu Array
            Array.from(inputElements).forEach(function (inputElement) {
                // Xử lí trường hợp blur khỏi input
                inputElement.onblur = function () {
                    Validate(inputElement, rule);
                }

                // Xử lí trường hợp khi người dùng nhập vào input
                inputElement.oninput = function () {
                    var errorElement = getParentElement(inputElement, options.formGroupSelector).querySelector(options.errorSelector);
                    errorElement.innerText = '';
                    getParentElement(inputElement, options.formGroupSelector).classList.remove('invalid');
                }
            })
        });
    }
}

// Định nghĩa rules
// Nguyên tắc của các rules:
// 1.Khi có lỗi => Trả ra lỗi
// 2.Khi không có lỗi => Không trả ra gì cả(undefined)
Validator.isRequired = function (selector, message) {
    return {
        selector: selector,
        test: function (value) {
            return value ? undefined : message || 'Vui lòng nhập trường này';
        }
    }
}

Validator.isEmail = function (selector) {
    return {
        selector: selector,
        test: function (value) {
            // Cú pháp kiểm tra email
            var regex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
            return regex.test(value) ? undefined : 'Trường này phải là email' 
        }
    }
}

Validator.minLength = function (selector, min) {
    return {
        selector: selector,
        test: function (value) {
            return value.length >= min ? undefined : `Vui lòng nhập tối thiểu ${min} kí tự`
        }
    }
}

Validator.isConfirmed = function (selector, getConfirmValue, message) {
    return {
        selector: selector,
        test : function (value) {
            return value === getConfirmValue() ? undefined : message || 'Giá trị nhập vào không chính xác'
        }
    }
}