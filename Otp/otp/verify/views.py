# views.py
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.http import HttpResponse

import random

def generate_otp():
    return str(random.randint(100000, 999999))

def index(request):
    email_value = ''
    success_message = None
    error_message = None

    if request.method == 'POST':
        if 'email' in request.POST:
            email = request.POST['email']
            if 'resend' in request.POST:
                # Handle resend OTP request
                otp = generate_otp()  # Generate a new OTP
                message = f'Your new OTP is: {otp}'
                send_mail('Resend OTP', message, 'singhdabbu829@gmail.com', [email])
                email_value = email  # Preserve email value
                success_message = 'New OTP sent successfully!'
                # Store the OTP in the session
                request.session['otp'] = otp
            else:
                # Handle initial OTP request
                otp = generate_otp()  # Generate OTP
                message = f'Your OTP is: {otp}'
                send_mail('OTP Verification', message, 'singhdabbu829@gmail.com', [email])
                email_value = email  # Preserve email value
                # Store the OTP in the session
                request.session['otp'] = otp

        elif 'otp' in request.POST:
            entered_otp = request.POST['otp']
            stored_otp = request.session.get('otp', '')  # Retrieve the stored OTP
            if entered_otp == stored_otp:
                # Redirect to the main page on successful verification
                return redirect('mainpage')
            else:
                error_message = 'Incorrect OTP. Please try again.'

    return render(request, 'index.html', {'email_value': email_value, 'success_message': success_message, 'error_message': error_message})

def mainpage(request):
    return render(request, 'mainpage.html')
