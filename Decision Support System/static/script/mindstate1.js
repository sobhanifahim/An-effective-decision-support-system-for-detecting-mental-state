
//document.getElementById("sidebar").style.width="0px";
//document.getElementById("menu").style.visibility="hidden"



function slide(){
    document.getElementById("sidebar").style.width="270px";
    document.getElementById("menu").style.visibility="visible"
    document.getElementById("close").style.visibility="visible"
}
function inside(){
    document.getElementById("sidebar").style.width="0px";
    document.getElementById("menu").style.visibility="hidden"
    document.getElementById("close").style.visibility="hidden"
}

function clk(){
    document.getElementById("Age").value=''
    document.getElementById("LowAlpha").value=''
    document.getElementById("HighAlpha").value=''
    document.getElementById("LowBeta").value=''
    document.getElementById("HighBeta").value=''
    document.getElementById("LowGamma").value=''
    document.getElementById("HighGamma").value=''
    /*const dict_values = {pname, age, gender,lowalpha,highalpha,lowbeta,highbeta,lowgamma,highgamma} 
        const s = JSON.stringify(dict_values); 
        console.log(s); // Prints the variables to console window, which are in the JSON format
        $.ajax({
            url:"http://127.0.0.1:4000/",
            type:"POST",
            Accept: "application/json",
            contentType: "application/json",
            data: JSON.stringify(s)
        });*/
    
}