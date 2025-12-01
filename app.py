import streamlit as st
import random
from auth import register_user, login_user, get_user_by_id, get_user_by_email
from database import (
    save_user_profile, get_user_profile, get_user_assignment,
    mark_assignment_revealed, get_random_question, get_username_by_id,
    get_all_usernames_except, get_all_users
)
from spinner import create_circular_spinner_wheel
from excel_reader import get_assignment_from_excel, get_all_assignments_from_excel

# Page configuration
st.set_page_config(
    page_title="🎅 Secret Santa",
    page_icon="🎄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for festive styling
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stButton>button {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        border: none;
        padding: 12px 30px;
        font-size: 16px;
        font-weight: 600;
        border-radius: 10px;
        cursor: pointer;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }
    .success-box {
        background: linear-gradient(135deg, #d4fc79 0%, #96e6a1 100%);
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #28a745;
        margin: 20px 0;
    }
    .info-box {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #17a2b8;
        margin: 20px 0;
    }
    .warning-box {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #ffc107;
        margin: 20px 0;
    }
    h1, h2, h3 {
        color: white;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .profile-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_data' not in st.session_state:
    st.session_state.user_data = None
if 'page' not in st.session_state:
    st.session_state.page = 'login'

def show_login_page():
    """Display login and registration page"""
    st.markdown("<h1 style='text-align: center;'>🎅 Secret Santa 🎄</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Spread the Holiday Joy!</h3>", unsafe_allow_html=True)
    
    # Check if user just registered
    if 'just_registered' not in st.session_state:
        st.session_state.just_registered = False
    
    # Default to login tab, or register tab based on state
    if st.session_state.just_registered:
        default_tab = 0  # Login tab
        st.session_state.just_registered = False
        st.success("✅ Registration successful! Please login with your credentials.")
    else:
        default_tab = 0  # Login tab by default
    
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])
    
    with tab1:
        st.markdown("<div class='profile-card'>", unsafe_allow_html=True)
        st.subheader("Welcome Back!")
        
        with st.form("login_form"):
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")
            submitted = st.form_submit_button("Login")
            
            if submitted:
                if email and password:
                    success, user_data, message = login_user(email, password)
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.user_data = user_data
                        st.session_state.page = 'dashboard'
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.warning("Please fill in all fields")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tab2:
        st.markdown("<div class='profile-card'>", unsafe_allow_html=True)
        st.subheader("Create Your Account")
        
        with st.form("register_form"):
            username = st.text_input("Username", key="reg_username")
            email = st.text_input("Email", key="reg_email")
            password = st.text_input("Password", type="password", key="reg_password")
            confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm")
            submitted = st.form_submit_button("Register")
            
            if submitted:
                if username and email and password and confirm_password:
                    if password != confirm_password:
                        st.error("Passwords do not match!")
                    elif len(password) < 6:
                        st.error("Password must be at least 6 characters long")
                    else:
                        success, message = register_user(username, email, password)
                        if success:
                            st.balloons()
                            st.session_state.just_registered = True
                            st.rerun()
                        else:
                            st.error(message)
                else:
                    st.warning("Please fill in all fields")
        
        st.markdown("</div>", unsafe_allow_html=True)

def show_profile_form():
    """Display profile completion form"""
    st.markdown("<h2 style='text-align: center;'>📝 Complete Your Profile</h2>", unsafe_allow_html=True)
    
    st.markdown("<div class='info-box'>", unsafe_allow_html=True)
    st.markdown("**Please fill in your details so your Secret Santa knows what to get you!**")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='profile-card'>", unsafe_allow_html=True)
    
    shipping_address = st.text_area(
        "📍 Shipping Address",
        placeholder="Enter your full shipping address...",
        height=100
    )
    
    wishlist = st.text_area(
        "🎁 Wishlist",
        placeholder="What would you like to receive? (Be specific!)",
        height=150
    )
    
    anti_wishlist = st.text_area(
        "🚫 Anti-Wishlist",
        placeholder="What would you NOT like to receive? (Allergies, dislikes, etc.)",
        height=100
    )
    
    if st.button("💾 Save Profile", key="save_profile"):
        if shipping_address and wishlist:
            save_user_profile(
                st.session_state.user_data['user_id'],
                shipping_address,
                wishlist,
                anti_wishlist
            )
            st.session_state.user_data['profile_completed'] = True
            st.success("✅ Profile saved successfully!")
            st.balloons()
            st.rerun()
        else:
            st.warning("Please fill in at least your shipping address and wishlist")
    
    st.markdown("</div>", unsafe_allow_html=True)

def show_quiz_page():
    """Display quiz to reveal Secret Santa assignment"""
    st.markdown("<h2 style='text-align: center;'>🎯 Answer to Reveal Your Secret Santa Child</h2>", unsafe_allow_html=True)
    
    # Get current username and email
    current_username = st.session_state.user_data['username']
    current_email = st.session_state.user_data['email']
    
    # Check if this user has an assignment in Excel (with email verification)
    assignment_result = get_assignment_from_excel(current_username, current_email)
    
    if not assignment_result:
        st.markdown("<div class='warning-box'>", unsafe_allow_html=True)
        st.markdown("**⚠️ Secret Santa assignment not found or email mismatch. Please contact the organizer.**")
        st.markdown("</div>", unsafe_allow_html=True)
        return
    
    # Check if user has already revealed their assignment (using session state)
    if 'assignment_revealed' not in st.session_state:
        st.session_state.assignment_revealed = False
    
    if st.session_state.assignment_revealed:
        # Create a dummy assignment object for the display function
        dummy_assignment = {'revealed': True}
        show_assignment_details(dummy_assignment)
        return
    
    # Initialize attempt counter
    if 'question_attempts' not in st.session_state:
        st.session_state.question_attempts = 0
    
    # Get random question
    if 'current_question' not in st.session_state:
        st.session_state.current_question = get_random_question()
    
    question_data = st.session_state.current_question
    
    st.markdown("<div class='profile-card'>", unsafe_allow_html=True)
    
    st.markdown(f"### {question_data['question']}")
    
    # Display options as buttons
    st.write("")
    cols = st.columns(2)
    
    for idx, option in enumerate(question_data['options']):
        col = cols[idx % 2]
        with col:
            if st.button(option, key=f"option_{idx}", use_container_width=True):
                if option == question_data['correct_answer']:
                    st.session_state.assignment_revealed = True
                    st.session_state.answered_correctly = True
                    st.session_state.question_attempts = 0
                    st.success("✅ Correct! Preparing to reveal your Secret Santa child...")
                    st.rerun()
                else:
                    st.session_state.question_attempts += 1
                    st.error("❌ Incorrect! Loading next question...")
                    st.session_state.current_question = get_random_question()
                    st.rerun()
    
    # Show attempt counter and skip button
    st.write("")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if st.button("🔄 Skip to Next Question", use_container_width=True):
            st.session_state.question_attempts += 1
            st.session_state.current_question = get_random_question()
            st.rerun()
    
    with col2:
        # After 5 attempts, allow user to reveal without answering
        if st.session_state.question_attempts >= 5:
            if st.button("🎁 Reveal Anyway", use_container_width=True, type="primary"):
                st.session_state.assignment_revealed = True
                st.session_state.answered_correctly = False
                st.session_state.question_attempts = 0
                st.rerun()
    
    # Show attempt counter
    if st.session_state.question_attempts > 0:
        st.info(f"💡 Attempts: {st.session_state.question_attempts} | After 5 attempts, you can reveal anyway!")
    
    st.markdown("</div>", unsafe_allow_html=True)

def show_assignment_details(assignment):
    """Display Secret Santa assignment after correct answer - child from Excel, details from DB"""
    
    # Get current user's username and email
    current_username = st.session_state.user_data['username']
    current_email = st.session_state.user_data['email']
    
    # Get child from Excel file (THIS IS THE KEY - Excel tells us WHO the child is)
    assignment_result = get_assignment_from_excel(current_username, current_email)
    
    if not assignment_result:
        st.error(f"Could not find assignment for {current_username} in Excel file or email mismatch")
        return
    
    child_username = assignment_result['child_username']
    
    # Show appropriate message based on how they revealed
    if 'answered_correctly' not in st.session_state:
        st.session_state.answered_correctly = False
    
    if st.session_state.answered_correctly:
        st.markdown("<div class='success-box'>", unsafe_allow_html=True)
        st.markdown("### ✅ Correct Answer!")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='info-box'>", unsafe_allow_html=True)
        st.markdown("### 🎁 Revealing Your Secret Santa Child")
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Show spinner wheel animation
    st.markdown("---")
    
    # Get all usernames from DATABASE (not Excel) for the wheel
    all_usernames = get_all_usernames_except(st.session_state.user_data['user_id'])
    
    # Ensure child is in the list
    if child_username not in all_usernames:
        all_usernames.append(child_username)
    
    # Limit to 8 names including the child
    wheel_names = all_usernames
    if len(wheel_names) > 8:
        # Keep child and random others
        other_names = [n for n in wheel_names if n.lower() != child_username.lower()]
        random_others = random.sample(other_names, min(7, len(other_names)))
        wheel_names = random_others + [child_username]
    elif len(wheel_names) < 8:
        # If less than 8, just use what we have
        wheel_names = all_usernames
    
    # Initialize wheel spin state
    if 'wheel_spun' not in st.session_state:
        st.session_state.wheel_spun = False
    
    if not st.session_state.wheel_spun:
        if st.button("🎰 Spin the Wheel to Reveal!", key="spin_wheel", type="primary", use_container_width=True):
            st.session_state.wheel_spun = True
            st.rerun()
    
    if st.session_state.wheel_spun:
        # Show the spinning animation with all DB usernames, landing on the Excel child
        create_circular_spinner_wheel(wheel_names, child_username)
        
        st.markdown("---")
        
        # NOW show the child details from DATABASE AFTER the wheel animation
        child_user = None
        # Find the child user in database by username
        all_users = get_all_users()
        for user in all_users:
            if user['username'].lower() == child_username.lower():
                child_user = user
                break
        
        # Get child's profile from DATABASE
        child_profile = None
        if child_user:
            child_profile = get_user_profile(child_user['user_id'])
        
        # Display child details from DATABASE
        st.markdown("<div class='profile-card'>", unsafe_allow_html=True)
        st.markdown(f"## 🎁 Your Secret Santa Child: **{child_username}**")
        
        if child_profile:
            st.markdown("### 📋 Their Details:")
            
            st.markdown("#### 📍 Shipping Address:")
            st.info(child_profile.get('shipping_address', 'Not provided'))
            
            st.markdown("#### 🎁 Wishlist:")
            st.success(child_profile.get('wishlist', 'Not provided'))
            
            st.markdown("#### 🚫 Anti-Wishlist:")
            st.warning(child_profile.get('anti_wishlist', 'Not provided'))
        else:
            st.markdown("<div class='warning-box'>", unsafe_allow_html=True)
            st.markdown(f"**{child_username} hasn't completed their profile yet.**")
            st.markdown("Please check back later for their details!")
            st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

def show_dashboard():
    """Display main dashboard"""
    user = st.session_state.user_data
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 👤 User Profile")
        st.markdown(f"**Username:** {user['username']}")
        st.markdown(f"**Email:** {user['email']}")
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user_data = None
            st.session_state.page = 'login'
            if 'current_question' in st.session_state:
                del st.session_state.current_question
            if 'answer_correct' in st.session_state:
                del st.session_state.answer_correct
            if 'assignment_revealed' in st.session_state:
                del st.session_state.assignment_revealed
            if 'wheel_spun' in st.session_state:
                del st.session_state.wheel_spun
            if 'question_attempts' in st.session_state:
                del st.session_state.question_attempts
            if 'answered_correctly' in st.session_state:
                del st.session_state.answered_correctly
            st.rerun()
    
    # Main content
    st.markdown(f"<h1 style='text-align: center;'>🎄 Welcome, {user['username']}! 🎅</h1>", unsafe_allow_html=True)
    
    # Check if profile is completed
    if not user.get('profile_completed', False):
        show_profile_form()
    else:
        # Show quiz/assignment page
        show_quiz_page()

def main():
    """Main application logic"""
    if not st.session_state.logged_in:
        show_login_page()
    else:
        show_dashboard()

if __name__ == "__main__":
    main()
