function togglemenu() {
    const menu = document.querySelector(".menu-links");
    const icon = document.querySelector(".ham-icon");
    menu.classList.toggle("open")
    icon.classList.toggle("open")
}


const optionMenu = document.querySelector(".select-menu"),
       selectBtn = optionMenu.querySelector(".select-btn"),
       options = optionMenu.querySelectorAll(".option"),
       sBtn_text = optionMenu.querySelector(".sBtn-text");
selectBtn.addEventListener("click", () => optionMenu.classList.toggle("active"));       
options.forEach(option =>{
    option.addEventListener("click", ()=>{
        let selectedOption = option.querySelector(".option-text").innerText;
        sBtn_text.innerText = selectedOption;
        optionMenu.classList.remove("active");
    });
});



function showInputFields() {
    var option = document.getElementById("option").value;
    var videoInput = document.getElementById("videoInput");
    var urlInput = document.getElementById("urlInput");

    videoInput.style.display = "none";
    urlInput.style.display = "none";

    if (option === "video") {
        videoInput.style.display = "block";
    } else if (option === "youtube") {
        urlInput.style.display = "block";
    }
}