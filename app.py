import streamlit as st
from PIL import Image

from ocr import extract_text
from medicine_ai import analyze_medicine


# --------------------------------------------------
# PAGE SETTINGS
# --------------------------------------------------

st.set_page_config(
    page_title="MediScan",
    page_icon="💊",
    layout="centered"
)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("💊 MediScan")
st.write("Scan. Understand. Remember.")

st.divider()


# --------------------------------------------------
# IMAGE INPUT
# --------------------------------------------------

st.subheader("📷 Scan Medicine")

option = st.radio(
    "Choose an option",
    ["📤 Upload Image", "📸 Take Photo"],
    horizontal=True
)

image = None


# --------------------------------------------------
# UPLOAD IMAGE
# --------------------------------------------------

if option == "📤 Upload Image":

    uploaded_file = st.file_uploader(
        "Upload your medicine strip",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file:
        image = Image.open(uploaded_file)


# --------------------------------------------------
# CAMERA
# --------------------------------------------------

else:

    camera_photo = st.camera_input(
        "Take a photo of your medicine strip"
    )

    if camera_photo:
        image = Image.open(camera_photo)


# --------------------------------------------------
# PROCESS IMAGE
# --------------------------------------------------

if image:

    st.image(
        image,
        caption="Medicine Image",
        use_container_width=True
    )

    if st.button("🔍 Scan Medicine", use_container_width=True):

        # -------------------------------
        # OCR
        # -------------------------------

        with st.spinner("Reading medicine information..."):

            text = extract_text(image)

        if text.strip():

            st.success("Medicine text detected!")

            # -------------------------------
            # AI ANALYSIS
            # -------------------------------

            with st.spinner("Understanding the medicine..."):

                medicine = analyze_medicine(text)

            st.divider()

            # -------------------------------
            # MEDICINE INFORMATION
            # -------------------------------

            st.subheader("💊 Medicine Information")

            st.write(
                f"**Medicine Name:** "
                f"{medicine.get('medicine_name', 'Not available')}"
            )

            st.write(
                f"**Ingredients:** "
                f"{medicine.get('ingredients', 'Not available')}"
            )

            st.write(
                f"**Strength:** "
                f"{medicine.get('strength', 'Not available')}"
            )


            # -------------------------------
            # USES
            # -------------------------------

            st.divider()

            st.subheader("🩺 What is it used for?")

            uses = medicine.get("uses", [])

            if uses:

                for use in uses:
                    st.write(f"• {use}")

            else:

                st.write("Information not available.")


            # -------------------------------
            # SIDE EFFECTS
            # -------------------------------

            st.divider()

            st.subheader("⚠️ Possible Side Effects")

            side_effects = medicine.get(
                "side_effects",
                []
            )

            if side_effects:

                for effect in side_effects:
                    st.write(f"• {effect}")

            else:

                st.write("Information not available.")


            # -------------------------------
            # PRECAUTIONS
            # -------------------------------

            st.divider()

            st.subheader("🚫 Important Precautions")

            precautions = medicine.get(
                "precautions",
                "Information not available."
            )

            st.warning(precautions)


            # -------------------------------
            # FOOD INFORMATION
            # -------------------------------

            st.divider()

            st.subheader("🍽️ Food Information")

            food_information = medicine.get(
                "food_information",
                "Check the medicine leaflet or ask a pharmacist."
            )

            st.info(food_information)


            # -------------------------------
            # HEALTH TIP
            # -------------------------------

            st.divider()

            st.subheader("💡 Health Tip")

            health_tip = medicine.get(
                "health_tip",
                "Always verify medicine information before taking it."
            )

            st.success(health_tip)


            # -------------------------------
            # SAFETY MESSAGE
            # -------------------------------

            st.divider()

            st.caption(
                "⚠️ This information is for educational purposes only. "
                "Always follow your doctor's prescription, medicine label, "
                "or pharmacist's advice."
            )


        else:

            st.warning(
                "No readable text found. "
                "Please upload a clearer medicine image."
            )
