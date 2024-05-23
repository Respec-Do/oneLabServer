// 알림 버튼 클릭시 목록 나오기
const announceBtn = document.querySelector('.announce-button-icon')
announceBtn.addEventListener("click", function(e) {
    const container = document.querySelector('.announce-list-container')
    container.classList.toggle('active');
});


// 파일 입력 필드에 변화가 있을 때 실행될 함수
const errorMessage = document.querySelector('div.upload-error')
document.getElementById("file-input").addEventListener('change', function(event) {
    var fileList = document.getElementById('file-list');
    var files = event.target.files;

    for (var i = 0; i < files.length; i++) {
        var file = files[i];

        if (file.type.startsWith('image/')) {
            var reader = new FileReader();
            reader.onload = (function(f) {
                return function(e) {
                    var cancelButton = document.createElement('button');
                    cancelButton.textContent = 'X';
                    cancelButton.className = 'cancel-upload';
                    
                    var thumbnail = document.createElement('img');
                    thumbnail.src = e.target.result;
                    thumbnail.alt = 'Thumbnail';
                    thumbnail.style.display = 'block';
                    thumbnail.width = 100;

                    var listItem = document.createElement('li');
                    listItem.appendChild(thumbnail);

                    
                    cancelButton.addEventListener('click', function() {
                        fileList.removeChild(listItem); // 취소된 파일 제거
                    });
                    listItem.appendChild(cancelButton);

                    fileList.appendChild(listItem);
                };
            })(file);
            reader.readAsDataURL(file);
            errorMessage.style.display = 'none'; 
        } else {
            errorMessage.style.display = 'block';  // 이미지 파일이 아닌 경우 에러 메시지 표시
        }
    }
});

// 업로드 취소 버튼에 클릭 이벤트 추가
const cancelBtns = document.querySelectorAll('button.cancel-upload')
cancelBtns.forEach((cancelBtn) => {
    cancelBtn.addEventListener('click', function(e) {
        cancelBtn.parentElement.remove;
    })
})


// 제목 글자수 계산
const input = document.querySelector('.maker-input');
const helperMsg = document.querySelector('.helper-msg');

input.addEventListener('input', function() {
    // input에 입력된 글자 수 계산
    const length = input.value.length;
    
    // 최대 글자 수는 30
    const maxLength = 30;
    
    // 남은 글자 수 계산
    const remaining = maxLength - length;
    
    // helper-msg의 텍스트를 업데이트
    helperMsg.textContent = remaining + '자 남음';
});


// 상세 내용 글자 수 계산
const textarea = document.querySelector('.textarea-input textarea');
const formFieldHelper = document.querySelector('.form-field-helper');

textarea.addEventListener('input', function() {
    // textarea에 입력된 글자 수 계산
    const length = textarea.value.length;

    // 최대 글자 수는 2000
    const maxLength = 2000;

    // 남은 글자 수를 계산합니다.
    const remaining = maxLength - length;

    formFieldHelper.textContent = remaining + '자 남음';
});


textarea.addEventListener('focus', function() {
    // textarea가 focus를 받았을 때 border 색을 변경
    textarea.style.borderColor = '#008243';
});

// 문서 전체에 click 이벤트를 추가합니다.
document.addEventListener('click', function(event) {
    // 클릭된 엘리먼트가 textarea가 아닌 경우에만 실행
    if (!event.target.closest('.textarea-input')) {
        // textarea 외부를 클릭했을 때 textarea의 border 색을 변경
        textarea.style.borderColor = '#dde2e6';
    }
});



const typeBtns = document.querySelectorAll('label.radio')
const activeBtns = document.querySelectorAll('span.radio-icon')
typeBtns.forEach((typeBtn) => {
    typeBtn.addEventListener('click', function(e){
        activeBtns.forEach((activeBtn) => {
            activeBtn.classList.remove('active')
        }) 
        const radioIcon = typeBtn.children[1];
        radioIcon.classList.add('active')
        if(typeBtn.classList[1]) {
            document.querySelector('.section-content.etc').style.display = 'block'
        }else {
            document.querySelector('.section-content.etc').style.display = 'none'
        }
    })
})

function getCSRFToken() {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.startsWith('csrftoken=')) {
            return cookie.split('=')[1];
        }
    }
    return '';
}

// 필요한 변수를 선언합니다.
const aiBtn = document.querySelector('#aiButton');
const box = document.querySelector('.ai-recommend-container')
const save_btn = document.querySelector('.save-btn');
let temp = '';
// 비동기 방식으로 추천된 내용을 가져오기 위해 addEventListener에 async로 설정해줍니다.
aiBtn.addEventListener('click', async (e) => {
    // 로딩되는 화면을 구현하기 위해 loading이라는 id를 불러와서 할당합니다.
    const loading = document.getElementById('loading');
    // 비동기방식을 이용하여 view로 제목을 보내기위해 제목의 value를 불러와서 할당합니다.
    const title = document.querySelector('input[name="community-title"]').value
    // 비동기방식을 이용하여 view로 범주를 보내기 위해 선택된 범주의 value를 가져옵니다.
    const radio_active = document.querySelector('.radio-icon.active').parentElement;
    const inputValue = radio_active.querySelector('input').value;
    // post 방식으로 보낼 때 필요한 csrf_token을 가져오는 함수를 이용합니다.
    const csrfToken = getCSRFToken();
    // 비동기 방식을 이용하여 가져온 내용을 저장할 div를 가져옵니다.
    const result_boxes = document.querySelectorAll('#result1')

    // console.log(title)
    // console.log(inputValue)

    // 내용을 가져오는 동안 화면상에서 로딩 중임을 표시하기 위해 loading의 display를 block으로 표시합니다.
    loading.style.display = 'block'
    box.style.display = 'none'
    // response라는 변수에 await 로 ai/similar 라는 경로를 통해 view로 비동기통신을 합니다.
    const response = await fetch("/ai/similar/", {
        // post 방식을 이용하여 csrftoken을 포함하여 앞서 설정한 제목과 범주 값을 JSON형태로 body에 담아 전송합니다.
        method: 'POST',
        headers: {
            "Content-Type": "application/json;charset=utf-8",
            "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify({
            title: title,
            radio_active: inputValue

        })
    });
    //  비동기 통신으로 view에서 값을 받아오기 전 로딩되는 화면을 다시 display none으로 바꿔줍니다.
    loading.style.display = 'none';
    // 내용을 받아와서 표시해주기 위해, 미리 만들어둔 div의 display를 block으로 바꿔줍니다.
    box.style.display = 'block';
    // response로 view를 통해 받아온 내용을 results에 담아줍니다.
    const results = await response.json();
    console.log(results);

    result_boxes.forEach((result_box, index)=>{
        // div에 각각 index로 가져온 유사도가 높은 내용을 담아줍니다.
        result_box.innerHTML = results.similar_communities[index];
        // 추천된 내용을 누르게 되면 addEventListener의 click 이벤트를 통해 내용 작성하는 곳에 추천된 내용을 담아줍니다.
        result_box.parentElement.addEventListener('click', (e)=>{
            const textarea = document.querySelector('.textarea-input textarea');

            textarea.value = results.similar_communities[index];
            // 추천된 내용이 옮겨 졌기 때문에, 기존의 추천을 받은 내용의 div는 display를 none으로 바꿔줍니다.
            box.style.display = 'none'
            // 추천된 내용을 그대로 저장하는 것을 방지하기 위해 저장 버튼을 비활성화해줍니다.
            save_btn.classList.add('disabled-button')
            save_btn.style.backgroundColor = '#808080'
            // 현재 추천된 내용을 temp에 저장합니다.
            temp = results.similar_communities[index];
        })
    })

});

// 내용을 수정하지 않고 저장을 누르게되면 경고문구를 표기하기 위해 해당되는 내용을 불러와서 warning에 할당합니다.
const warning = document.querySelector('.warning')
// 내용의 수정을 감지하기 위해 EventListener의 keyup을 이용합니다.
textarea.addEventListener('keyup', function() {
    // keyup이 감지될때 내용이 수정되어야 저장버튼을 활성화합니다.
    if (textarea.value !== temp) {
        save_btn.classList.remove('disabled-button')
        save_btn.style.backgroundColor = '#008243'
        // 경고 문구의 display를 none으로 바꿔줍니다.
        warning.style.display = 'none'
    } else {
        // textarea의 내용이 temp와 동일하면 저장버튼을 비활성화합니다.
        save_btn.classList.add('disabled-button')
        save_btn.style.backgroundColor = '#808080'
    }



})

// 저장 버튼을 눌렀을 때 submit을 해주기 위해 form 태그를 불러와서 할당합나디.
const form = document.getElementById('submit-form')

save_btn.addEventListener('click', (e)=> {
    // console.log('클릭')
    // 저장 버튼이 눌렸을 때, 비활성화되어 있다면, submit을 막고 경고문구를 활성화합니다.
    if (save_btn.classList.contains('disabled-button')) {
        e.preventDefault()
        warning.style.display = 'block'
    } else {
        // 저장 버튼이 활성화되어 있다면 form 태그를 submit합니다.
        form.submit();
    }
})

