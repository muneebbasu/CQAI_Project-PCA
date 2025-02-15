import onnxruntime
import streamlit as st
from PIL import Image
from io import BytesIO
import requests
from streamlit_star_rating import st_star_rating
from database import FeedbackStorage
from learn_pca import LearnPCASection
from how_pca_works import how_pca_works_page
from comparison_analytics import comparison_page
from compress_image import upload_image
from background_remover import background_remover_page
# Function to load images from URLs
def load_image(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img

def load_image_from_path(image_path):
    img = Image.open(image_path)
    return img

# Set page config
st.set_page_config(
    page_title="PCA ImageXpert",
    page_icon="📸",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Streamlit navigation
def navigate_pages(pages):
    # Initialize the session state
    if 'page_index' not in st.session_state:
        st.session_state['page_index'] = 0

    # Set the radio button selection to the current page
    page = st.sidebar.radio("Select a page:", pages, index=st.session_state.page_index)

    # Return the current page
    return page

# Streamlit navigation
st.sidebar.header(" NAVIGATION", divider='rainbow')

pages = ["Home", "Compress Image", "How PCA Works", "Compare Images", "Learn PCA","Background Remover","Feedback"]

# Call the navigate_pages function and store the current page
current_page = navigate_pages(pages)

# Custom CSS for styling
st.markdown("""
    <style>
    .body {background-color: #f2c698;}
    .main {
            background-image: url("https://images.unsplash.com/photo-1528460033278-a6ba57020470?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTAyfHxtYWNoaW5lJTIwbGVhcm5pbmclMjBsaWdodCUyMGJhY2tncm91bmR8ZW58MHx8MHx8fDA%3D");
            background-size: cover;
#        background-color: #add8e0;
    }
    .appview-container .sidebar .sidebar-content {
            background-image: url("https://images.unsplash.com/photo-1528460033278-a6ba57020470?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTAyfHxtYWNoaW5lJTIwbGVhcm5pbmclMjBsaWdodCUyMGJhY2tncm91bmR8ZW58MHx8MHx8fDA%3D");
            background-size: cover;
#        background-color: #fff;
    }
    .sidebar .sidebar-header {
    }
    .stButton > button {
        background-color: #4CAFFE;
        color: aliceblue;
    }
    .stSlider > div {
        color: #4CAF50;
    }
    </style>
    """, unsafe_allow_html=True)

# Page functions
def home():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Merriweather:wght@700&display=swap'); /* Importing Merriweather from Google Fonts */

        .art-title {
            font-family: 'Merriweather', serif; /* Professional and beautiful font */
            text-align: center;
            color: #2c3e50; /* Dark blue color for the text */
            text-shadow: 3px 3px 5px rgba(0, 0, 0, 0.5), 6px 6px 10px rgba(0, 0, 0, 0.3); /* Enhanced shadows for 3D effect */
            font-size: 53px; /* Adjusted font size for professionalism */
            margin: 20px 0; /* Reduced margin */
            letter-spacing: 2px;
            line-height: 1.0;
        }
        body {
            background-color: #FFFFFF; /* White background */
            color: #000000; /* Black text color */
        }
    </style>
    <h1 class="art-title">
    📸 PCA ImageXpert 
    </h1>
    """, unsafe_allow_html=True)


    st.markdown("""
        <style>
        .big-paragraph {
            font-size: 20px;
            line-height: 1.5;
            margin-top: 20px;
            text-align: left;
            }
            .sub {
                font-family: 'Merriweather', serif; /* Professional and beautiful font */
                text-align: center;
                font-size: 23px;
                font-weight: bold; /* Making the text bold */
                margin: 2px 0; /* Adding margin */
                line-height: 1.5; /* Adjusting line height */
                letter-spacing: 1.3px; /* Adjusting letter spacing */
            }
            @keyframes moveLeft {
            0% { transform: translateX(0px); }
            50% { transform: translateX(-10px); }
            100% { transform: translateX(0px); }
            }

            .moving-emoji-container {
            display: flex;
            justify-content: center;
            }

            .moving-emoji {
            animation: moveLeft 1s infinite;
            font-size: 39px; /* Adjust the size as needed */
            }
        </style>
        <p class="sub">Welcome to PCA ImageXpert!</p>
        <p class="big-paragraph">
        Unlock the power of Principal Component Analysis (PCA) with PCA ImageXpert, your comprehensive, pedagogical platform designed to make learning and applying PCA accessible, engaging, and fun. Whether you’re a tech nerd diving deep into the logic and code, or a beginner exploring the basics, PCA ImageXpert is crafted to guide you through the fascinating world of unsupervised machine learning with ease.
        <p><strong style="font-size: 24px;">Navigate Your PCA Journey</strong>.</p>
        <!-- Example of including image using HTML in a single line with options for changing size and alignment -->
        <img src="https://www.designnominees.com/application/blog-images/website-easy-to-navigate.png" alt="Image" style="width: 600px; height: auto; margin: auto; display: block;">
        <br>
            <p style="font-size: 20px;">Our intuitive navigation bar helps you explore all the features PCA ImageXpert offers:</p>
            <p><strong style="font-size: 20px;">Home:</strong> <span style="font-size: 20px;">Return to the main page anytime to see the latest updates and featured content.</span></p>
            <p><strong style="font-size: 20px;">Compress Image:</strong> <span style="font-size: 20px;">Effortlessly upload your images in JPG, JPEG, or PNG format and experience the magic of PCA-powered image compression. Other formats are not supported to ensure the best quality and performance.</span></p>
            <p><strong style="font-size: 20px;">How PCA works:</strong> <span style="font-size: 20px;">Dive into the detailed workings of PCA. Understand the underlying logic, algorithms, and code implementations. Perfect for those who want to get into the technical nitty-gritty.</span></p>
            <p><strong style="font-size: 20px;">Learn PCA:</strong> <span style="font-size: 20px;">Start from scratch with our beginner-friendly tutorials. We break down complex concepts into easy-to-understand lessons, making PCA accessible even to a child.</span></p>
            <p><strong style="font-size: 20px;">Compare Images:</strong> <span style="font-size: 20px;">See the difference PCA makes. Upload an image, let our application compress it, and then compare the original and compressed versions side by side. Analyze various metrics and view histograms of the similarity index to understand the effectiveness of the compression.</span></p>
            <p><strong style="font-size: 20px;">Feedback:</strong> <span style="font-size: 20px;">Share your thoughts and see what others have to say. Your feedback helps us improve, and we value every suggestion.</span></p>
            <p><strong style="font-size: 20px;">View Feedback:</strong><span style="font-size: 20px;"> This feature allows users to see feedbacks and suggestions given by users.</span></p>
            <p><strong style="font-size: 24px;">Why PCA ImageXpert?</strong></p>
        <img src="https://plannersweb.com/wp-content/uploads/1993/01/why-word.jpg" alt="Image" style="width: 500px; height: auto; margin: auto; display: block;">
        <br>
            <p style="font-size: 20px;">PCA ImageXpert isn’t just another tech tool; it’s a learning companion. We believe in honesty, clarity, and making complex subjects approachable. Our features are designed to provide a seamless experience, whether you’re learning the basics or exploring advanced applications.</p>
            <p style="font-size: 20px;"><strong>Educational:</strong> Learn PCA in a structured, easy-to-follow way.</p>
            <p style="font-size: 20px;"><strong>Practical:</strong> Apply PCA to real-world tasks like image compression.</p>
            <p style="font-size: 20px;"><strong>Interactive:</strong> Compare and analyze results to deepen your understanding.</p>
            <p style="font-size: 20px;"><strong>Community-Driven:</strong> Engage with a community of learners and tech enthusiasts through feedback and shared experiences.</p>
            <p style="font-size: 20px;">Join us on PCA ImageXpert and transform your understanding of PCA from theory to practice. Let’s make data science not just understandable but also enjoyable for everyone.</p>
            <p style="font-size: 20px;">Welcome aboard, and happy learning!</p>
            <p style="font-size: 20px;">By using our application, you can see these principles in action and understand the impact of PCA on image processing. Start with the Compress Image feature to see how much space you can save without losing significant details.</p>
        </p>
        
        <div class="moving-emoji-container">
        <div class="moving-emoji">👈</div>
        </div>
    
    """, unsafe_allow_html=True)
    
    st.markdown("""
    For more information, visit our [documentation](https://example.com/documentation) or contact our [support team](https://example.com/support).
    """)

    st.markdown("""
        <footer style="position: fixed; bottom: 0; left: 0; width: 100%; margin: 0; text-align: center; font-size: 14px; color: black; border: 1px solid #333; color: #fff; background-color: black">
        @All rights reserved. Quantum Inno Vissionaries
        </footer>
                """, unsafe_allow_html=True)
    
    # Display the next button
    if st.button("**Compress Image ⇨**", key="next"):
        st.session_state.page_index = (st.session_state.page_index + 1) % len(pages)
        st.rerun()

        
def learn_pca_page():
    learn_pca = LearnPCASection()
    learn_pca.render_page()
    
    # Display the next button
    if st.button("**Background Remover ⇨**", key="next"):
        st.session_state.page_index = (st.session_state.page_index + 1) % len(pages)
        st.rerun()
        
def feedback():
    storage = FeedbackStorage()
    
    # Custom CSS for styling
    st.markdown("""
        <style>
        .big-font {
            font-size: 24px !important;
            font-weight: bold;
            color: #1E88E5;
        }
        .feedback-container {
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        .feedback-header {
            text-align: center;
            padding: 20px;
            background: linear-gradient(135deg, #1E88E5, #64B5F6);
            color: white;
            border-radius: 10px;
            margin-bottom: 30px;
        }
        .feedback-card {
            background-color: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            margin-bottom: 15px;
            border-left: 4px solid #1E88E5;
        }
        .rating-display {
            color: #FFC107;
            font-size: 18px;
        }
        .timestamp {
            color: #680;
            font-size: 14px;
            font-style: italic;
        }
        .divider {
            height: 2px;
            background: linear-gradient(to right, #1E88E5, transparent);
            margin: 20px 0;
        }
        </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown("<div class='feedback-header'><h1>🌟 Share Your Experience</h1></div>", unsafe_allow_html=True)

    # Main feedback container
    st.markdown("<div class='feedback-container'>", unsafe_allow_html=True)
    
    # Introduction text
    st.markdown("""
        <p style='font-size: 18px; text-align: center; color: #666;'>
            Your feedback helps us improve and serve you better. Please take a moment to share your thoughts!
        </p>
    """, unsafe_allow_html=True)

    # Rating and Comment section
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("<p class='big-font'>Rate your experience:</p>", unsafe_allow_html=True)
        rating = st_star_rating(
            label=" ",
            maxValue=5,
            defaultValue=0,
            key="rating",
            size=40,
            dark_theme = True,
            customCSS={
                ".stars": {"color": "#FFC107"},
                "button": {"background-color": "transparent", "border": "none"}
            }
        )
    with col2:
        st.markdown("<p class='big-font'>Tell us more:</p>", unsafe_allow_html=True)
        comment = st.text_area(
            "",
            height=70,
            placeholder="Share your thoughts, suggestions, or experiences...",
            key="feedback_comment"
        )

    # Submit button with custom styling
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        submit = st.button(
            "Submit Feedback",
            key="submit_feedback",
            help="Click to submit your feedback"
        )

    st.markdown("</div>", unsafe_allow_html=True)

    # Handle submission
    if submit:
        if rating and comment:
            storage.save_feedback("Anonymous", rating, comment)
            st.success("🎉 Thank you for your valuable feedback!")
            st.balloons()
        else:
            st.error("Please provide both a rating and comment before submitting.")

    # Display previous feedback
    st.markdown("<div class='feedback-header'><h1>📝 Previous Feedback</h1></div>", unsafe_allow_html=True)

    feedbacks = storage.get_all_feedback()
    for feedback in feedbacks:
        st.markdown("<div class='feedback-card'>", unsafe_allow_html=True)
        st.markdown(f"<p class='rating-display'>{feedback['rating']} stars</p>", unsafe_allow_html=True)
        st.markdown(f"<p>{feedback['comment']}</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='timestamp'>{feedback['timestamp']}</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # Display the next button
    if st.button("**Return to Home Page ⇨**", key="next"):
        st.session_state.page_index = (st.session_state.page_index + 1) % len(pages)
        st.rerun()
        
if current_page == "Home":
    home()
elif current_page == "Compress Image":
    upload_image()
elif current_page == "How PCA Works":
    how_pca_works_page()
elif current_page == "Compare Images":
    comparison_page()
elif current_page == "Learn PCA":
    learn_pca_page()
elif current_page == "Background Remover":
    background_remover_page()
elif current_page == "Feedback":
    feedback()


def generate_footer():
    return """
    <footer style="text-align: center; font-size: 14px; color: black;">
        This is the footer text. You can add any additional information or links here.
    </footer>
    """

