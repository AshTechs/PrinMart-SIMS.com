document.addEventListener('DOMContentLoaded', function () {
    const otpInputs = document.querySelectorAll('.otp-digit');
    const resendBtn = document.getElementById('resend-btn');
    const errorMessageDiv = document.getElementById('error-message');
    const timerDiv = document.getElementById('timer');
    const csrfToken = document.querySelector('input[name="csrf_token"]').value;

    let countdown;
    let remainingTime = 60;  // Countdown timer

    // Function to update the timer display
    function updateTimer() {
        if (remainingTime > 0) {
            timerDiv.textContent = `${remainingTime} seconds.`;
            remainingTime--;
        } else {
            clearInterval(countdown);
            resendBtn.disabled = false;  // Enable resend button after timer ends
            timerDiv.textContent = '.';
        }
    }

    // Start the countdown timer
    countdown = setInterval(updateTimer, 1000);

    // Reset input borders to default
    function resetInputBorders() {
        otpInputs.forEach(input => {
            input.style.border = '1px solid #ccc';  // Default border color
        });
    }

    // Focus next input automatically on each key entry
    otpInputs.forEach((input, index) => {
        input.addEventListener('input', function () {
            if (input.value.length === 1 && index < otpInputs.length - 1) {
                otpInputs[index + 1].focus();
            }
            if (index === otpInputs.length - 1) {
                // Automatically verify code when the last input is filled
                verifyOtp();
            }
        });

        input.addEventListener('keydown', function (event) {
            if (event.key === 'Backspace' && input.value === '' && index > 0) {
                otpInputs[index - 1].focus();
            }
        });
    });

    // Handle pasting of the OTP
    let otpCode = '';
otpInputs.forEach(input => {
    otpCode += input.value.trim();  // Use trim() to remove whitespace
});

    otpInputs.forEach((input, index) => {
        input.addEventListener('paste', function (event) {
            event.preventDefault();
            const pastedData = event.clipboardData.getData('text').trim();
            const digits = pastedData.split('');

            if (digits.length === 6) {
                otpInputs.forEach((otpInput, i) => {
                    otpInput.value = digits[i] || '';  // Populate each input field
                });
                otpInputs[5].focus();  // Focus on the last input after pasting
                verifyOtp(); // Automatically verify when pasted
            }
        });
    });

    // Function to verify OTP
    async function verifyOtp() {
        let otpCode = '';
        otpInputs.forEach(input => {
            otpCode += input.value;
        });

        resetInputBorders();
        errorMessageDiv.style.display = 'none';

        if (otpCode.length !== 6) {
            errorMessageDiv.textContent = 'Please fill out all the digits.';
            errorMessageDiv.style.display = 'block';
            return;
        }

        try {
            const response = await fetch('/verify_code', {
                method: 'POST',
                body: JSON.stringify({ verification_code: otpCode }),
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                }
            });

            const result = await response.json();

            if (response.ok && result.success) {
                otpInputs.forEach(input => {
                    input.style.border = '1px solid green';  // Highlight in green for success
                });
                window.location.href = '/login';
            } else {
                errorMessageDiv.textContent = 'Invalid verification code. Please try again.';
                errorMessageDiv.style.display = 'block';
                otpInputs.forEach(input => {
                    input.style.border = '1px solid red';  // Highlight in red for error
                });
            }
        } catch (error) {
            errorMessageDiv.textContent = 'An error occurred. Please try again later.';
            errorMessageDiv.style.display = 'block';
        }
    }

    // Handle resend button click
    resendBtn.addEventListener('click', async function (event) {
        event.preventDefault();
        resendBtn.disabled = true;  // Disable the button until a new code is requested

        try {
            const response = await fetch('/resend_code', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken
                }
            });

            const result = await response.json();
            if (response.ok) {
                errorMessageDiv.textContent = 'New verification code sent.';
                errorMessageDiv.style.display = 'block';
                remainingTime = 60;  // Reset the timer
                countdown = setInterval(updateTimer, 1000);  // Restart the countdown
            } else {
                errorMessageDiv.textContent = result.error || 'Error sending code. Please try again.';
                errorMessageDiv.style.display = 'block';
            }
        } catch (error) {
            errorMessageDiv.textContent = 'An error occurred. Please try again later.';
            errorMessageDiv.style.display = 'block';
        }
    });
});
