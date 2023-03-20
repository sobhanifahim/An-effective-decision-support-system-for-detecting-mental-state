

function emptyfield(){
     var n=document.getElementById("name").value
     var g=document.getElementById("gen").value
     var a=document.getElementById("age").value
     var la=document.getElementById("la").value
     var ha=document.getElementById("ha").value
     var lb=document.getElementById("lb").value
     var hb=document.getElementById("hb").value
     var lg=document.getElementById("lg").value
     var hg=document.getElementById("hg").value
     var ms=document.getElementById("ms").value
     var ref=document.getElementById("rf").value
     var cmnt=document.getElementById("cmmnt").value
     var res=confirm("Are you sure want to submit?")
     if(res==false){
          event.preventDefault();
     }
     if(n==''||g==''||a==''||la==''||ha==''||lb==''||hb==''||lg==''||hg==''||ms==''||ref==''){
      alert(" input field cannot be empty")
     }
}
