import streamlit as st
import time
import random

def create_circular_spinner_wheel(names, winner_name):
    """Create an animated circular spinner wheel that lands on the winner"""
    
    # Ensure winner is in the list
    if winner_name not in names:
        names.append(winner_name)
    
    # Make sure we have exactly 8 names
    while len(names) < 8:
        names.append("---")
    names = names[:8]
    
    # Shuffle to randomize positions, but keep track of winner
    random.shuffle(names)
    winner_index = names.index(winner_name)
    
    # Create placeholder for animation
    wheel_placeholder = st.empty()
    
    # Animation parameters - simulate spinning wheel with arrow pointing down
    total_rotations = 3  # Number of full rotations
    total_steps = (total_rotations * 8) + winner_index  # Land on winner
    
    # Spinning animation
    for step in range(total_steps + 1):
        current_index = step % 8
        
        # Slow down as we approach the winner
        if step < total_steps - 10:
            delay = 0.1
        elif step < total_steps - 5:
            delay = 0.2
        else:
            delay = 0.4
        
        # Display wheel
        with wheel_placeholder.container():
            st.markdown("### 🎰 Spinning the Wheel...")
            st.markdown("<div style='text-align: center; font-size: 2em; color: red;'>⬇️</div>", unsafe_allow_html=True)
            
            # Create circular layout
            cols = st.columns(8)
            for i in range(8):
                with cols[i]:
                    # Highlight current position under the arrow
                    if i == current_index:
                        st.markdown(f"""
                        <div style='
                            background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
                            padding: 15px;
                            border-radius: 15px;
                            text-align: center;
                            color: black;
                            font-weight: bold;
                            font-size: 1.1em;
                            box-shadow: 0 8px 16px rgba(255,215,0,0.5);
                            transform: scale(1.15);
                            border: 4px solid gold;
                            min-height: 80px;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                        '>
                            {names[i]}
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div style='
                            background: #e0e0e0;
                            padding: 15px;
                            border-radius: 15px;
                            text-align: center;
                            color: #666;
                            font-size: 0.9em;
                            min-height: 80px;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                        '>
                            {names[i]}
                        </div>
                        """, unsafe_allow_html=True)
        
        time.sleep(delay)
    
    # Final result - show winner
    with wheel_placeholder.container():
        st.markdown("### 🎉 WINNER!")
        st.balloons()
        st.markdown("<div style='text-align: center; font-size: 2em; color: red;'>⬇️</div>", unsafe_allow_html=True)
        
        # Show final wheel with winner highlighted
        cols = st.columns(8)
        for i in range(8):
            with cols[i]:
                if i == winner_index:
                    st.markdown(f"""
                    <div style='
                        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
                        padding: 20px;
                        border-radius: 15px;
                        text-align: center;
                        font-weight: bold;
                        font-size: 1.5em;
                        box-shadow: 0 12px 24px rgba(255,215,0,0.6);
                        border: 5px solid gold;
                        min-height: 100px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                    '>
                        🎁 {names[i]} 🎁
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style='
                        background: #f0f0f0;
                        padding: 15px;
                        border-radius: 15px;
                        text-align: center;
                        color: #999;
                        font-size: 0.9em;
                        min-height: 80px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                    '>
                        {names[i]}
                    </div>
                    """, unsafe_allow_html=True)
    
    return winner_name

def create_spinner_wheel(names, winner_name):
    """Wrapper for backward compatibility"""
    return create_circular_spinner_wheel(names, winner_name)
