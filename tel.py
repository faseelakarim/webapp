import streamlit as st
import numpy as np
import joblib
from PIL import Image
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import urllib.parse
# Custom CSS


# Custom CSS
st.markdown("""
<style>
body {
    background-color: #000000;
    color: #2A2A2A;
}
h1 {
    color: #5e9ca0;
}
input {
    background-color: #eef5ef;
}
.left-column {
    background-color: #000000;
    border-radius: 10px;
    padding: 1rem;
}
.right-column {
    background-color: #F0F0F0;
    border-radius: 10px;
    padding: 1rem;
}
</style>
""", unsafe_allow_html=True)
# st.markdown("""
# <style>
# body {
#     margin: 2rem;
#     border: 1px solid #5e9ca0;
#     border-radius: 10px;
# }
# h1 {
#     color: #5e9ca0;
# }
# input {
#     background-color: #eef5ef;
# }
# .left-column {
#     background-color: #87ceeb;  /* sky blue */
#     border-radius: 10px;
#     padding: 1rem;
# }
# .right-column {
#     background-color: #b5c5bf;
#     border-radius: 10px;
#     padding: 1rem;
# }
# </style>
# """, unsafe_allow_html=True)


def create_gmail_link(to, subject, body):
    base_url = "https://mail.google.com/mail/?view=cm&fs=1&tf=1"
    params = {
        "to": to,
        "su": subject,
        "body": body
    }
    url_params = urllib.parse.urlencode(params)
    return f"{base_url}&{url_params}"


# Load the pretrained model
model = joblib.load('finalized_model.pkl')

# Create columns
left_column, _, right_column = st.columns([5, .5, 4])


# Display image in the right upper corner
image = Image.open("image.jpg")
right_column.image(image, width=200)

# Display heading in the right side
right_column.header("What We Can Offer")

# Title and Description
left_column.title("Telecom Customer Churn Prediction")
left_column.write("This application predicts if a customer is likely to churn based on their usage and account data. "
                  "Please enter the required information below and click the 'Predict Churn' button.")

# User Input Section
left_column.subheader("Customer Information")
id_ = left_column.number_input('CustomerID', min_value=0, step=1)
months = left_column.number_input('years on Network', min_value=0, step=1)
eqpdays = left_column.number_input('Number of days the customer using the equipment', min_value=0, step=1)
refurb_new = left_column.number_input('Refurbished/New Status (0 if Refurbished, 1 if New phone)', min_value=0, max_value=1, step=1)
hnd_price = left_column.number_input('Handset Price', min_value=0, step=1)
mou_mean = left_column.number_input('Mean Monthly Minutes of Use', min_value=0.0, step=0.1)
asl_flag = left_column.number_input('Account Spending Limit Flag (0 if this feature is off, or 1 if feature is on)', min_value=0, max_value=1, step=1)

# Prepare input array
input_data = np.array([months, eqpdays, refurb_new, hnd_price, mou_mean, asl_flag]).reshape(1, -1)

# Predict Button and Display Result
if left_column.button('Predict Churn'):
    prediction = model.predict(input_data)

    if prediction >= 0.5:
        left_column.success("The customer is likely to churn.")
        offer_message = "We have a special offer for you!"
        if eqpdays > 300:
            right_column.write("Provide financial incentives for purchasing new devices, either through discounts or easy installment plans, it can encourage customers to stay with the company.")
            offer_message=offer_message+"\n"+"We are providing financial incentives for purchasing new devices"
        if 0 < months <= 48:
            right_column.write("provide Promotions and limited-time offers.")
#             right_column.write("Roaming and international offers.")
            offer_message=offer_message+"\n"+"We have promotional offers for you ,valid until next month"
        if months > 48:
            right_column.write(" Provide Loyalty programs: Reward long-term customers with perks such as discounts, free upgrades, or exclusive access to new products and services.")
            offer_message=offer_message+"\n"+"We have long term reward for you"
        if refurb_new == 0:
#             right_column.write("Offer a new phone with a lower price than the market.")
            right_column.write("Provide financial incentives for purchasing new devices, either through discounts or easy installment plans, it can encourage customers to stay with the company.")
            offer_message=offer_message+"\n"+"We are providing financial incentives for purchasing new devices"
        if refurb_new == 1:
#             right_column.write("Offer a new phone with a lower price than the market.")
            
            right_column.write("Provide Bundle offers: Combine multiple services like voice, data, text, and other value-added services in a single package.")
            offer_message=offer_message+"\n"+"We are providing Bundle offers "
        if mou_mean > 600:
            right_column.write("Provide Personalized plans: Customize plans according to individual usage patterns and preferences.")
            offer_message=offer_message+"\n"+"We have some unlimited voice plans for you "
        if asl_flag == 0:
            right_column.write("Provide Customized instructions for turning on the account spending limit.")
            offer_message=offer_message+"\n"+"Add account spending limit and save your money"
    
        customer_email = f"{id_}@gmail.com"
        gmail_link = create_gmail_link(
        to=customer_email,
        subject="Telecom Customer Churn Prediction - Special Offer",
        body=offer_message
        )
        left_column.markdown(f'[Click here to send an email to {customer_email}]({gmail_link})', unsafe_allow_html=True)

    else:
        left_column.success("The customer is not likely to churn.")
