$(document).on('click', '.like', function () {
  var pk = $(this).attr('name');
  $.ajax({                                                          // .like 버튼을 클릭하면 <새로고침> 없이 ajax로 서버와 통신하겠다.
    type: "POST",                                                   // 데이터를 전송하는 방법을 지정
    url: "{% url 'docxmerge:like' %}",                              // 통신할 url을 지정
    data: { 'pk': pk, 'csrfmiddlewaretoken': '{{ csrf_token }}' },  // 서버로 데이터 전송시 옵션
    dataType: "json",                                               // 서버측에서 전송한 데이터를 어떤 형식의 데이터로서 해석할 것인가를 지정, 없으면 알아서 판단
                      
    // 서버측에서 전송한 Response 데이터 형식 (json)
    // {'likes_count': {docxmerge:like}, 'message': message }
    // 통신 성공시 - 좋아요 갯수 변경, 유저 목록 변경
    success: function (response) {
      alert(response.message);
      $("#count-" + pk).html("좋아요 " + response.like_count + "개");
      var users = $("#like-user-" + pk).text();
      if (users.indexOf(response.username) != -1) {
        if (response.like_count == 0) {
          $("#like-user-" + pk).text("");
        } else {
          $("#like-user-" + pk).text(users.replace(response.username, ""));
        }
        $("input.like[name=" + pk + "]").toggleClass('liked to-like');
      } else {
        $("#like-user-" + pk).text(response.username + users);
        $("input.like[name=" + pk + "]").toggleClass('to-like liked');
      }
    },
    error: function (request, status, error) {                      // 통신 실패시 - 로그인 페이지 리다이렉트
      alert("로그인이 필요합니다.");
      window.location.replace("/users/login/");
      //  alert("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
    },
  });
});