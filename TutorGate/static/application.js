document.addEventListener("DOMContentLoaded", function () {
    const applicationForm = document.getElementById("applicationForm");

    applicationForm.addEventListener("submit", function (event) {
        event.preventDefault();

        // Get values from the form
        const universityName = document.querySelector("#applicationForm input[name='universityName']").value;
        const previousUniversityName = document.querySelector("#applicationForm input[name='previousUniversityName']").value;
        const completedQualifications = document.querySelector("#applicationForm input[name='completedQualifications']").value;
        const studentEmail = document.querySelector("#applicationForm input[name='studentEmail']").value;
        const mobileNumber = document.querySelector("#applicationForm input[name='mobileNumber']").value;
        const currentYearOfStudy = document.querySelector("#applicationForm select[name='currentYearOfStudy']").value;

        // Save values to local storage
        localStorage.setItem("universityName", universityName);
        localStorage.setItem("previousUniversityName", previousUniversityName);
        localStorage.setItem("completedQualifications", completedQualifications);
        localStorage.setItem("studentEmail", studentEmail);
        localStorage.setItem("mobileNumber", mobileNumber);
        localStorage.setItem("currentYearOfStudy", currentYearOfStudy);

        // Redirect to dashboard.html
        window.location.href = "dashboard.html";
    });
});




