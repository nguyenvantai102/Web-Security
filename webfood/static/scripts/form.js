form = document.querySelector('.contact1-form')
inputList = form.querySelectorAll('input')

// Thêm class and placeholder cho thẻ input trong form contact
placeholder = ["Họ & tên", "Địa chỉ mail", "Tiêu đề", "Nội dung feedback"]
for (var i = 1; i < 4; i++) {
    inputList[i].className = "input1"
    inputList[i].placeholder = placeholder[i - 1]
}

// Thêm class and placeholder cho thẻ textarea trong form contact
textarea = form.querySelector('textarea')
textarea.className = "input1"
textarea.placeholder = placeholder[3]
