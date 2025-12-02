import streamlit as st
import random
from auth import register_user, login_user, get_user_by_id, get_user_by_email
from database import (
    save_user_profile, get_user_profile, get_user_assignment,
    mark_assignment_revealed, get_random_question, get_username_by_id,
    get_all_usernames_except, get_all_users
)
from spinner import create_circular_spinner_wheel
from excel_reader import get_assignment_from_excel, get_all_assignments_from_excel, get_all_child_names_from_excel, get_santa_name_by_email

# Page configuration
st.set_page_config(
    page_title="🎅 Secret Santa",
    page_icon="🎄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for festive Christmas styling
st.markdown("""
<style>
    /* Christmas themed background - red and green */
    .main {
        background: linear-gradient(135deg, 
            #0d3b1f 0%,     /* Deep forest green */
            #1a5c35 25%,    /* Christmas green */
            #8b1538 50%,    /* Christmas red */
            #1a5c35 75%,    /* Christmas green */
            #0d3b1f 100%    /* Deep forest green */
        );
        position: relative;
    }
    
    /* Falling snow animation - more realistic */
    @keyframes snowfall1 {
        0% {
            transform: translateY(-10vh);
            opacity: 0;
        }
        10% {
            opacity: 1;
        }
        100% {
            transform: translateY(110vh);
            opacity: 0.9;
        }
    }
    
    @keyframes snowfall2 {
        0% {
            transform: translateY(-10vh);
            opacity: 0;
        }
        10% {
            opacity: 1;
        }
        100% {
            transform: translateY(110vh);
            opacity: 0.7;
        }
    }
    
    @keyframes snowfall3 {
        0% {
            transform: translateY(-10vh);
            opacity: 0;
        }
        10% {
            opacity: 1;
        }
        100% {
            transform: translateY(110vh);
            opacity: 0.8;
        }
    }
    
    /* Create snow with only small snowflakes */
    .stApp::before {
        content: "";
        pointer-events: none;
    }
    
    .stApp::after {
        content: "";
        pointer-events: none;
    }
    
    /* Third snow layer */
    .main::before {
        content: "* * * * * * * * * * * *";
        position: fixed;
        top: -10vh;
        left: 50px;
        width: 100%;
        font-size: 10px;
        color: rgba(255, 255, 255, 0.6);
        letter-spacing: 80px;
        animation: snowfall3 32s linear infinite;
        animation-delay: 5s;
        pointer-events: none;
        z-index: 9999;
        text-shadow: 0 0 3px rgba(255, 255, 255, 0.4);
    }
    
    /* Twinkling and floating stars */
    @keyframes starFloat {
        0% {
            transform: translateY(0px) translateX(0px);
            opacity: 0.5;
        }
        25% {
            transform: translateY(-20px) translateX(30px);
            opacity: 1;
        }
        50% {
            transform: translateY(-10px) translateX(-20px);
            opacity: 0.7;
        }
        75% {
            transform: translateY(-25px) translateX(15px);
            opacity: 1;
        }
        100% {
            transform: translateY(0px) translateX(0px);
            opacity: 0.5;
        }
    }
    
    .main::after {
        content: "⭐ ✨ ⭐ ✨ ⭐ ✨ ⭐ ✨ ⭐ ✨ ⭐ ✨ ⭐ ✨ ⭐ ✨ ⭐ ✨ ⭐ ✨ ⭐ ✨ ⭐";
        position: fixed;
        top: 60px;
        right: 0;
        width: 100%;
        font-size: 18px;
        letter-spacing: 40px;
        animation: starFloat 6s ease-in-out infinite;
        pointer-events: none;
        z-index: 1;
    }
    
    /* Simple festive buttons */
    .stButton>button {
        background: linear-gradient(135deg, #dc2626 0%, #16a34a 100%);
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
        box-shadow: 0 5px 15px rgba(220, 38, 38, 0.5);
    }
    
    /* Clean boxes */
    .success-box {
        background: rgba(16, 185, 129, 0.9);
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #10b981;
        margin: 20px 0;
        color: white;
    }
    
    .info-box {
        background: rgba(59, 130, 246, 0.9);
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #3b82f6;
        margin: 20px 0;
        color: white;
    }
    
    .warning-box {
        background: rgba(245, 158, 11, 0.9);
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #f59e0b;
        margin: 20px 0;
        color: white;
    }
    
    /* Golden headings */
    h1, h2, h3 {
        color: #ffd700 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    
    /* Clean white profile cards */
    .profile-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        margin: 20px 0;
    }
    
    /* Keep sidebar simple with Christmas colors */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d3b1f 0%, #8b1538 100%);
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
            username = st.text_input("Name", key="reg_username", placeholder="Enter your full name")
            email = st.text_input("Email", key="reg_email", placeholder="Your Deloitte email")
            password = st.text_input("Password (minimum 6 characters)", type="password", key="reg_password")
            submitted = st.form_submit_button("Register")
            
            if submitted:
                if username and email and password:
                    # Check if email ends with @deloitte.com
                    if not email.lower().strip().endswith('@deloitte.com'):
                        st.error("Email must be a Deloitte email address (@deloitte.com)")
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
        placeholder="Anything you would love to receive!",
        height=150
    )
    
    anti_wishlist = st.text_area(
        "🚫 Anti-Wishlist",
        placeholder="Things you'd rather NOT receive! (e.g., Another coffee mug, Keychains, Motivational posters, Scented candles, Anything that needs assembly...)",
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
    
    # Get current user's email
    current_email = st.session_state.user_data['email']
    
    # Check if this user has an assignment in Excel (using email only)
    assignment_result = get_assignment_from_excel(current_email)
    
    if not assignment_result:
        st.markdown("<div class='warning-box'>", unsafe_allow_html=True)
        st.markdown("**⚠️ Secret Santa assignment not found. Please contact the organizer.**")
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
    """Display Secret Santa assignment after correct answer - child email from Excel, details from DB"""
    
    # Get current user's email
    current_email = st.session_state.user_data['email']
    
    # Get child email and name from Excel file
    assignment_result = get_assignment_from_excel(current_email)
    
    if not assignment_result:
        st.error(f"Could not find assignment for {current_email} in Excel file")
        return
    
    child_email = assignment_result['child_email']
    child_name_from_excel = assignment_result['child_name']  # Get name from Excel
    
    # Now get the child's details from DATABASE using their email
    all_users = get_all_users()
    child_user = None
    for user in all_users:
        if user['email'].lower() == child_email.lower():
            child_user = user
            break
    
    # Use name from Excel (always available), regardless of registration status
    child_username = child_name_from_excel
    child_registered = child_user is not None
    
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
    
    # Get names from Excel for the wheel (not from database)
    # This ensures consistent display using official participant names
    excel_names = get_all_child_names_from_excel()
    
    # Get current user's info to exclude them
    current_username = st.session_state.user_data['username']
    current_email = st.session_state.user_data['email']
    
    # Get the Santa name from Excel based on email (in case they registered with different name)
    santa_name_from_excel = get_santa_name_by_email(current_email)
    
    # Build list of names to exclude (current user's variations)
    names_to_exclude = set()
    names_to_exclude.add(current_username.lower())
    if santa_name_from_excel:
        names_to_exclude.add(santa_name_from_excel.lower())
    
    # Filter out current user's name from Excel names
    all_usernames = []
    for name in excel_names:
        # Skip if name matches any variation of current user
        if name.lower() not in names_to_exclude:
            all_usernames.append(name)
    
    # Ensure child is in the list
    if child_username not in all_usernames:
        all_usernames.append(child_username)
    
    # Limit to 8 names including the child and randomize
    if len(all_usernames) > 8:
        # Keep child and get 7 random others
        other_names = [n for n in all_usernames if n.lower() != child_username.lower()]
        random_others = random.sample(other_names, min(7, len(other_names)))
        wheel_names = random_others + [child_username]
        # Shuffle so child isn't always at the end
        random.shuffle(wheel_names)
    else:
        # Use all available names and shuffle
        wheel_names = all_usernames.copy()
        random.shuffle(wheel_names)
    
    # Initialize wheel spin state
    if 'wheel_spun' not in st.session_state:
        st.session_state.wheel_spun = False
    
    if not st.session_state.wheel_spun:
        if st.button("🎰 Spin the Wheel to Reveal!", key="spin_wheel", type="primary", use_container_width=True):
            st.session_state.wheel_spun = True
            st.rerun()
    
    if st.session_state.wheel_spun:
        # Show the spinning animation with all DB usernames, landing on the child
        create_circular_spinner_wheel(wheel_names, child_username)
        
        st.markdown("---")
        
        # Display child details
        st.markdown("<div class='profile-card'>", unsafe_allow_html=True)
        st.markdown(f"## 🎁 Your Secret Santa Child: **{child_username}**")
        st.markdown(f"**Email:** {child_email}")
        
        if child_registered:
            # Get child's profile from DATABASE
            child_profile = get_user_profile(child_user['user_id'])
            
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
        else:
            # Child hasn't registered yet
            st.markdown("<div class='warning-box'>", unsafe_allow_html=True)
            st.markdown(f"**📧 This person hasn't registered yet.**")
            st.markdown(f"Contact them at: **{child_email}**")
            st.markdown("Ask them to register and complete their profile so you can see their wishlist!")
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
