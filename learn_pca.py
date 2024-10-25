import streamlit as st
import base64
import os
from typing import List, Dict, Any

class LearnPCASection:
    def __init__(self):
        # Initialize session states
        if 'progress' not in st.session_state:
            st.session_state.progress = 1
        if 'quiz_status' not in st.session_state:
            st.session_state.quiz_status = {}
        
        self.pdf_dir = "tutorial_pdfs"
        self.tutorials = self._get_tutorials()
        self.faq_items = self._get_faq_items()

    def _get_tutorials(self) -> List[Dict[str, Any]]:
        """Define tutorial content"""
        return [
            {
                "title": "Tutorial 1: Understanding Eigenvalues and Eigenvectors",
                "pdf_file": "tutorial1.pdf",
                "quiz": [
                    {
                        "question": "What happens when you multiply a matrix by a vector?",
                        "options": [
                            "The vector's direction always changes.",
                            "The vector may get rotated or scaled.",
                            "The vector remains unchanged."
                        ]
                    },
                    {
                        "question": "Which of the following is true about eigenvectors?",
                        "options": [
                            "Eigenvectors change direction when multiplied by a matrix.",
                            "Eigenvectors disappear when multiplied by a matrix.",
                            "Eigenvectors retain their direction but may be scaled."
                        ]
                    },
                    {
                        "question": "What does an eigenvalue represent in the context of matrix multiplication with an eigenvector?",
                        "options": [
                            "The rotation angle of the vector.",
                            "The factor by which the eigenvector is scaled.",
                            "The determinant of the matrix"
                        ]
                    }
                ],
                "correct_answers": [
                    "The vector may get rotated or scaled.",
                    "Eigenvectors retain their direction but may be scaled.",
                    "The factor by which the eigenvector is scaled."
                ]
            },
            {
                "title": "Tutorial 2: Mathematical Foundation",
                "pdf_file": "tutorial2.pdf",
                "quiz": [
                    {
                        "question": "What is Eigenvalue?",
                        "options": [
                            "A value associated with matrix",
                            "A statistical measure",
                            "A type of variable"
                        ]
                    },
                    {
                        "question": "PCA is based on which decomposition?",
                        "options": [
                            "SVD",
                            "QR Decomposition",
                            "Cholesky Decomposition"
                        ]
                    },
                    {
                        "question": "What is the output of PCA?",
                        "options": [
                            "Principal Components",
                            "Coefficients",
                            "Basis Vectors"
                        ]
                    }
                ],
                "correct_answers": [
                    "A value associated with matrix",
                    "SVD",
                    "Principal Components"
                ]
            },
            {
                "title": "Tutorial 3: PCA in Practice",
                "pdf_file": "tutorial3.pdf",
                "quiz": [
                    {
                        "question": "What is the main purpose of PCA?",
                        "options": [
                            "Data compression",
                            "Data classification",
                            "Dimensionality reduction"
                        ]
                    },
                    {
                        "question": "Which preprocessing step is important before applying PCA?",
                        "options": [
                            "Data normalization",
                            "Data encryption",
                            "Data augmentation"
                        ]
                    },
                    {
                        "question": "How do you choose the number of principal components?",
                        "options": [
                            "Based on explained variance ratio",
                            "Always choose half of original dimensions",
                            "Random selection"
                        ]
                    }
                ],
                "correct_answers": [
                    "Dimensionality reduction",
                    "Data normalization",
                    "Based on explained variance ratio"
                ]
            }
        ]

    def _get_faq_items(self) -> List[Dict[str, str]]:
        """Define FAQ items"""
        return [
            {
                "question": "What is PCA used for?",
                "answer": "PCA is used primarily for dimensionality reduction and data visualization, allowing us to reduce the number of variables in our data without losing much information."
            },
            {
                "question": "Can PCA be used for classification?",
                "answer": "PCA itself is not a classification technique, but it can be used as a preprocessing step to reduce the number of features before applying classification algorithms."
            },
            {
                "question": "Is PCA sensitive to data scaling?",
                "answer": "Yes, PCA is sensitive to the scale of the data. It is generally recommended to standardize or normalize the data before applying PCA."
            },
            {
                "question": "How many principal components should I retain?",
                "answer": "This depends on your specific needs. A common approach is to retain enough components to explain a certain percentage (e.g., 95%) of the variance in your data."
            },
            {
                "question": "What are the limitations of PCA?",
                "answer": "PCA assumes linear relationships between variables, is sensitive to outliers, and may not work well with non-linear data. It also requires standardized data for optimal results."
            },
            {
                "question": "What's the difference between PCA and factor analysis?",
                "answer": "While both reduce dimensionality, PCA focuses on explaining maximum variance, while factor analysis focuses on identifying underlying factors that explain correlations between variables."
            },
            {
                "question": "Can PCA handle categorical data?",
                "answer": "PCA is designed for continuous numerical data. Categorical data should be properly encoded (e.g., one-hot encoding) before applying PCA, though other techniques might be more appropriate."
            },
            {
                "question": "Is PCA computationally expensive?",
                "answer": "For small to medium datasets, PCA is relatively fast. However, for very large datasets, computational cost can increase significantly, especially when computing the covariance matrix."
            }
        ]
    
    def display_pdf(self, pdf_file: str) -> None:
        """Embed PDF viewer in Streamlit"""
        try:
            with open(pdf_file, "rb") as f:
                pdf_data = f.read()
            
            base64_pdf = base64.b64encode(pdf_data).decode('utf-8')
            pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
            
            st.markdown(pdf_display, unsafe_allow_html=True)
            st.download_button(
                label="Download Tutorial PDF",
                data=pdf_data,
                file_name=pdf_file,
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"Error loading PDF: {str(e)}")

    def display_quiz(self, questions: List[Dict], correct_answers: List[str], tutorial_num: int) -> None:
        """Display quiz questions and handle submission"""
        with st.form(key=f'quiz_form_{tutorial_num}'):
            user_answers = []
            all_answered = True

            for i, q in enumerate(questions):
                st.write(f"**Q{i + 1}:** {q['question']}")
                user_answer = st.selectbox(
                    f"Choose the correct option for Q{i + 1}",
                    options=["Select an option"] + q['options'],
                    key=f'q{tutorial_num}_{i}'
                )
                
                if user_answer == "Select an option":
                    all_answered = False
                user_answers.append(user_answer)

            submitted = st.form_submit_button("Submit Quiz")
            
            if submitted:
                self._handle_quiz_submission(user_answers, correct_answers, all_answered, tutorial_num)

    def _handle_quiz_submission(self, user_answers: List[str], correct_answers: List[str], 
                            all_answered: bool, tutorial_num: int) -> None:
        """Handle quiz submission and scoring"""
        if not all_answered:
            st.error("Please answer all questions before submitting.")
            return

        score = sum(1 for ua, ca in zip(user_answers, correct_answers) if ua == ca)
        
        if score == len(correct_answers):
            st.success("🎉 Congratulations! All answers are correct!")
            st.session_state.progress += 1
            st.session_state.quiz_status[tutorial_num] = 'passed'
            st.balloons()
        else:
            st.error(f"Score: {score}/{len(correct_answers)}. Try again!")

    def render_page(self) -> None:
        """Main method to render the Learn PCA page"""
        st.title("Learn PCA 📚")
        
        # Progress tracking
        progress = (st.session_state.progress - 1) / len(self.tutorials) * 100 
        
        st.write(f"**Progress: {progress:.2f}%**")
        
        # Display tutorials
        for idx, tutorial in enumerate(self.tutorials):
            tutorial_number = idx + 1
            
            if st.session_state.progress >= tutorial_number:
                st.header(f"{tutorial['title']}")
                
                # Display PDF
                pdf_path = os.path.join(self.pdf_dir, tutorial['pdf_file'])
                if os.path.exists(pdf_path):
                    self.display_pdf(pdf_path)
                else:
                    st.error(f"PDF for {tutorial['title']} not found!")
                
                # Display quiz
                if st.session_state.progress == tutorial_number and tutorial_number not in st.session_state.quiz_status:
                    st.write("### Ready to Test Yourself")
                    self.display_quiz(tutorial["quiz"], tutorial["correct_answers"], tutorial_number)
                    st.write("---")
            else:
                st.write(f"**Tutorial {tutorial_number} is locked. Complete the previous tutorial's quiz to unlock.**")
        
        # Display FAQ
        st.title("Frequently Asked Questions (FAQ)")
        for faq in self.faq_items:
            st.subheader(f"**{faq['question']}**")
            st.write(faq['answer'])