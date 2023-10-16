function togglemenu() {
    const menu = document.querySelector(".menu-links");
    const icon = document.querySelector(".ham-icon");
    menu.classList.toggle("open")
    icon.classList.toggle("open")
}

const optionMenu = document.querySelector(".select-menu");
const selectBtn = optionMenu.querySelector(".select-btn");
const options = optionMenu.querySelectorAll(".option");
const sBtn_text = optionMenu.querySelector(".sBtn-text");
const videoInput = document.getElementById("videoInput");
const urlInput = document.getElementById("urlInput");

selectBtn.addEventListener("click", () => optionMenu.classList.toggle("active"));

options.forEach(option => {
    option.addEventListener("click", () => {
        let selectedOption = option.querySelector(".option-text").innerText;
        sBtn_text.innerText = selectedOption;

        optionMenu.classList.remove("active");

        if (selectedOption === "Video") {
            videoInput.style.display = "block";
            urlInput.style.display = "none";
        } else if (selectedOption === "Youtube URL") {
            urlInput.style.display = "block";
            videoInput.style.display = "none";
        } else if (selectedOption === "Select your option") {
            videoInput.style.display = "none";
            urlInput.style.display = "none";
        }
    });
});



const langSelectMenu = document.querySelector(".lang-select-menu");
const langSelectBtn = langSelectMenu.querySelector(".lang-select-btn");
const langOptions = langSelectMenu.querySelector(".lang-options");
const lang_SBtn_text = langSelectMenu.querySelector(".lang-sBtn-text");

langSelectBtn.addEventListener("click", () => {
    langSelectMenu.classList.toggle("active");

    langOptions.forEach(lang_option => {
        lang_option.addEventListener("click"), () => {
            let seletedlang = lang_option.querySelector(".lang-option-text").innerText;
            lang_SBtn_text.innerText = seletedlang;

            langSelectMenu.classList.remove("active");
        }
    })
});

langOptions.addEventListener("click", (event) => {
    if (event.target.classList.contains("lang-option-text")) {
        const selectedOption = event.target.textContent;
        langSelectBtn.querySelector(".lang-sBtn-text").textContent = selectedOption;
        langSelectMenu.classList.remove("active");
    }
});