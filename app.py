import cv2
import mediapipe as mp
import numpy as np
import streamlit as st
import time
import threading
import pyttsx3

# Robust Threaded Text-to-Speech using Windows SAPI5 driver
def speak(text):
    def _speak(txt):
        try:
            engine = pyttsx3.init('sapi5')
            engine.setProperty('rate', 170)
            voices = engine.getProperty('voices')
            if voices:
                engine.setProperty('voice', voices[0].id)
            engine.say(txt)
            engine.runAndWait()
            engine.stop()
        except Exception as e:
            pass
    threading.Thread(target=_speak, args=(text,), daemon=True).start()

# Page Configuration
st.set_page_config(page_title="Pro Seated AI Fitness Trainer", page_icon="💪", layout="wide")

# Advanced Modern UI Theme Styling
st.markdown("""
    <style>
    /* Global App Background & Font */
    .stApp {
        background: linear-gradient(135deg, #090d16 0%, #151c2f 100%);
        color: #f8fafc;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }

    /* Fix Streamlit Top Padding so Header doesn't get cut */
    .block-container {
        padding-top: 3.5rem !important;
        padding-bottom: 2rem !important;
    }

    /* Fix Streamlit Top Header & Toolbar Background */
    header[data-testid="stHeader"] {
        background: rgba(15, 23, 42, 0.85) !important;
        backdrop-filter: blur(8px);
        border-bottom: 1px solid #1e293b;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #111827 0%, #090d16 100%);
        border-right: 1px solid #1f2937;
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] label {
        color: #e2e8f0 !important;
    }

    /* Highly Highlighted / Glowing Workout Start-Stop Toggle Button */
    [data-testid="stSidebar"] [data-testid="stCheckbox"] {
        background: linear-gradient(135deg, #dc2626 0%, #991b1b 100%);
        padding: 10px 14px;
        border-radius: 10px;
        border: 2px solid #f87171;
        box-shadow: 0 0 15px rgba(220, 38, 38, 0.6);
        margin-top: 8px;
        margin-bottom: 8px;
        transition: all 0.3s ease;
    }
    [data-testid="stSidebar"] [data-testid="stCheckbox"]:hover {
        box-shadow: 0 0 20px rgba(248, 113, 113, 0.9);
        transform: scale(1.02);
    }
    [data-testid="stSidebar"] [data-testid="stCheckbox"] span {
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 15px !important;
    }

    /* Custom Attractive Header Banner Styling - Emojis brought closer and text made bigger */
    .main-header-container {
        background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%);
        padding: 20px 24px;
        border-radius: 14px;
        border: 1px solid #6366f1;
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.3);
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 15px;
        width: 100%;
        box-sizing: border-box;
    }
    .main-header-title {
        font-size: 26px;
        font-weight: 800;
        background: linear-gradient(90deg, #38bdf8, #818cf8, #f472b6, #34d399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.3px;
        margin: 0;
        line-height: 1.3;
        text-align: center;
    }
    .emoji-icon {
        font-size: 30px;
    }

    /* Subheaders */
    h2, h3 {
        color: #cbd5e1 !important;
        font-weight: 600 !important;
        margin-top: 0px !important;
        margin-bottom: 8px !important;
    }

    /* Compact Dashboard Metric Cards Styling */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.85) 0%, rgba(15, 23, 42, 0.95) 100%);
        padding: 10px 14px;
        border-radius: 10px;
        border: 1px solid #38bdf840;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(8px);
        margin-bottom: 6px;
    }
    [data-testid="stMetric"] label {
        color: #38bdf8 !important;
        font-weight: 600 !important;
        font-size: 13px !important;
    }
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #f1f5f9 !important;
        font-weight: 800 !important;
        font-size: 22px !important;
    }

    /* Guide Cards Styling */
    .guide-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.95) 100%);
        border: 1px solid #334155;
        border-radius: 14px;
        padding: 22px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
        margin-bottom: 20px;
    }
    .guide-title {
        color: #38bdf8;
        font-size: 20px;
        font-weight: 700;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .guide-text {
        color: #cbd5e1;
        font-size: 14px;
        line-height: 1.6;
    }
    .tip-badge {
        display: inline-block;
        background: rgba(56, 189, 248, 0.15);
        color: #38bdf8;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 13px;
        font-weight: 600;
        margin-top: 8px;
        border: 1px solid rgba(56, 189, 248, 0.3);
    }

    /* Developer Profile Card Styling */
    .dev-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #6366f1;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        margin-top: 30px;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.2);
    }
    .dev-name {
        font-size: 16px;
        font-weight: 700;
        color: #f8fafc;
        margin-bottom: 2px;
    }
    .dev-role {
        font-size: 12px;
        color: #818cf8;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 12px;
    }
    .dev-links {
        display: flex;
        justify-content: center;
        gap: 10px;
        flex-wrap: wrap;
        margin-top: 10px;
    }
    .dev-btn {
        background: #312e81;
        color: #38bdf8;
        padding: 6px 12px;
        border-radius: 6px;
        font-size: 12px;
        text-decoration: none;
        font-weight: 600;
        border: 1px solid #4f46e5;
        transition: all 0.3s ease;
    }
    .dev-btn:hover {
        background: #4f46e5;
        color: #ffffff;
    }
    </style>
""", unsafe_allow_html=True)

# Styled Attractive App Header with Muscle Emojis close to the title
st.markdown("""
    <div class="main-header-container">
        <span class="emoji-icon">💪</span>
        <span class="main-header-title">Pro Seated AI Fitness Trainer & Goal Tracker</span>
        <span class="emoji-icon" style="transform: scaleX(-1);">💪</span>
    </div>
""", unsafe_allow_html=True)

# MediaPipe Setup
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Sidebar Controls & Goals
st.sidebar.header("⚙️ Workout Settings")
seated_exercises = [
    "Seated Bicep Curl", 
    "Seated Shoulder Press", 
    "Seated Leg Extension", 
    "Seated Triceps Extension", 
    "Seated Lateral Raises", 
    "Seated Knee Raises (Marching)", 
    "Seated Upright Row",
    "Seated Hammer Curl"
]
exercise = st.sidebar.selectbox("Select Seated Exercise", seated_exercises)
tracking_side = st.sidebar.selectbox("Tracking Side", ["Right", "Left"])
target_reps = st.sidebar.number_input("Target Reps per Set", min_value=1, max_value=50, value=10, step=1)
target_sets = st.sidebar.number_input("Target Sets", min_value=1, max_value=5, value=3, step=1)
workout_timer_mins = st.sidebar.slider("Workout Duration Timer (Minutes)", min_value=1, max_value=30, value=5, step=1)
rest_time = st.sidebar.slider("Rest Time Between Sets (sec)", min_value=5, max_value=60, value=15, step=5)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🛑 Workout Control Panel")
run_webcam = st.sidebar.checkbox("🚀 START / STOP SESSION")
reset_btn = st.sidebar.button("🔄 Reset Workout")

# Developer Profile in Sidebar with Direct Gmail Link
st.sidebar.markdown("""
    <div class="dev-card">
        <div class="dev-name">Narayan Das</div>
        <div class="dev-role">Founder & Creator</div>
        <div class="dev-links">
            <a href="https://mail.google.com/mail/?view=cm&fs=1&to=ndas88617@gmail.com" class="dev-btn" target="_blank">📧 Email</a>
            <a href="https://www.instagram.com/jh_10_narayan__?stkn=NDR5aW1oYnRyMzk5" class="dev-btn" target="_blank">📸 Instagram</a>
            <a href="https://www.linkedin.com/in/narayan-das-3a0bb03ab?utm_source=share_via&utm_content=profile&utm_medium=member_android" class="dev-btn" target="_blank">💼 LinkedIn</a>
        </div>
    </div>
""", unsafe_allow_html=True)

# Angle Calculation Function
def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    
    if angle > 180.0:
        angle = 360.0 - angle
        
    return angle

# UI Layout: Camera wider [3.5], Dashboard compact [1.2]
col1, col2 = st.columns([3.5, 1.2])

with col1:
    st.subheader("📷 Live Camera Stream")
    stframe = st.empty()

with col2:
    st.subheader("📊 Live Dashboard")
    rep_placeholder = st.empty()
    set_placeholder = st.empty()
    stage_placeholder = st.empty()
    timer_placeholder = st.empty()
    calories_placeholder = st.empty()
    
    st.markdown("### 🎯 Progress")
    progress_bar = st.progress(0)
    
    st.markdown("### 💡 Form Tips")
    tip_box = st.empty()
    
    feedback_box = st.empty()
    feedback_box.success("Sit comfortably and align your side.")

# Main Workout Logic Loop
if run_webcam:
    cap = cv2.VideoCapture(0)
    counter = 0
    current_set = 1
    completed_sets = 0
    total_reps_all_sets = 0
    stage = "Down"
    
    start_time_epoch = time.time()
    workout_duration_sec = workout_timer_mins * 60
    
    calorie_multiplier = 0.15 if "Press" in exercise or "Extension" in exercise else 0.1
    
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while run_webcam and cap.isOpened():
            if reset_btn:
                counter = 0
                current_set = 1
                completed_sets = 0
                total_reps_all_sets = 0
                stage = "Down"
                start_time_epoch = time.time()
                
            elapsed_time = time.time() - start_time_epoch
            remaining_workout_time = max(0, int(workout_duration_sec - elapsed_time))
            
            if remaining_workout_time <= 0:
                speak("Workout time is up! Great job!")
                feedback_box.success("⏰ Workout Timer Finished! Awesome effort!")
                st.balloons()
                st.markdown("---")
                st.markdown("""
                    <div style="background: linear-gradient(135deg, #047857 0%, #065f46 100%); padding: 20px; border-radius: 12px; text-align: center; border: 1px solid #34d399; box-shadow: 0 8px 20px rgba(4, 120, 87, 0.3);">
                        <h2 style="color: #6ee7b7 !important; margin: 0;">🎈🎊 Workout Timer Completed! 🌟🔥</h2>
                        <p style="color: #d1fae5; font-size: 16px; margin-top: 5px;">You successfully completed your timed session!</p>
                    </div>
                """, unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                
                st.subheader("📋 Workout Summary Report Card")
                col_a, col_b, col_c = st.columns(3)
                col_a.metric("Total Exercises", exercise)
                col_b.metric("Total Repetitions", str(total_reps_all_sets))
                col_c.metric("Estimated Calories Burned", f"{int(total_reps_all_sets * calorie_multiplier)} kcal")
                break
                
            ret, frame = cap.read()
            if not ret:
                st.warning("Failed to grab camera frame.")
                break
                
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = pose.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            try:
                landmarks = results.pose_landmarks.landmark
                
                if tracking_side == "Right":
                    shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                    elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                    wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                    hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                    knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                    ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
                else:
                    shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                    elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                    wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                    hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                    knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                    ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

                if exercise in ["Seated Bicep Curl", "Seated Hammer Curl"]:
                    angle = calculate_angle(shoulder, elbow, wrist)
                    if angle > 140:
                        stage = "Down"
                        tip_box.info("ℹ️ Curl all the way up smoothly.")
                    elif angle < 50 and stage == "Down":
                        stage = "Up"
                        counter += 1
                        total_reps_all_sets += 1
                        speak(str(counter))
                        tip_box.success("✅ Good contraction! Lower down slowly.")
                        
                elif exercise == "Seated Shoulder Press":
                    angle = calculate_angle(shoulder, elbow, wrist)
                    if angle < 80:
                        stage = "Down"
                        tip_box.info("ℹ️ Press overhead fully.")
                    elif angle > 150 and stage == "Down":
                        stage = "Up"
                        counter += 1
                        total_reps_all_sets += 1
                        speak(str(counter))
                        tip_box.success("✅ Great extension! Lower carefully.")

                elif exercise == "Seated Leg Extension":
                    angle = calculate_angle(hip, knee, ankle)
                    if angle < 100:
                        stage = "Bent"
                        tip_box.info("ℹ️ Extend your leg straight out.")
                    elif angle > 160 and stage == "Bent":
                        stage = "Extended"
                        counter += 1
                        total_reps_all_sets += 1
                        speak(str(counter))
                        tip_box.success("✅ Excellent lockout! Bring it back.")

                elif exercise == "Seated Triceps Extension":
                    angle = calculate_angle(shoulder, elbow, wrist)
                    if angle > 140:
                        stage = "Extended"
                        tip_box.info("ℹ️ Bend your elbow backward/downward.")
                    elif angle < 80 and stage == "Extended":
                        stage = "Bent"
                        counter += 1
                        total_reps_all_sets += 1
                        speak(str(counter))
                        tip_box.success("✅ Perfect triceps squeeze!")

                elif exercise == "Seated Lateral Raises":
                    angle = calculate_angle(hip, shoulder, elbow)
                    if angle < 30:
                        stage = "Down"
                        tip_box.info("ℹ️ Raise your arms sideways up to shoulder height.")
                    elif angle > 75 and stage == "Down":
                        stage = "Up"
                        counter += 1
                        total_reps_all_sets += 1
                        speak(str(counter))
                        tip_box.success("✅ Good posture! Control the drop.")

                elif exercise == "Seated Knee Raises (Marching)":
                    angle = calculate_angle(shoulder, hip, knee)
                    if angle > 130:
                        stage = "Down"
                        tip_box.info("ℹ️ Lift your knee up towards your chest.")
                    elif angle < 90 and stage == "Down":
                        stage = "Raised"
                        counter += 1
                        total_reps_all_sets += 1
                        speak(str(counter))
                        tip_box.success("✅ Solid core engagement!")

                elif exercise == "Seated Upright Row":
                    angle = calculate_angle(shoulder, elbow, wrist)
                    if angle > 140:
                        stage = "Down"
                        tip_box.info("ℹ️ Pull elbows upward and outward.")
                    elif angle < 70 and stage == "Down":
                        stage = "Up"
                        counter += 1
                        total_reps_all_sets += 1
                        speak(str(counter))
                        tip_box.success("✅ Perfect pull alignment!")

                if counter >= target_reps:
                    completed_sets += 1
                    if completed_sets < target_sets:
                        current_set += 1
                        counter = 0
                        speak(f"Set {completed_sets} completed. Take a rest.")
                        feedback_box.warning(f"Set {completed_sets-1} completed! 🛑 Resting for {rest_time}s...")
                        
                        rest_placeholder = st.empty()
                        for remaining in range(rest_time, 0, -1):
                            rest_placeholder.metric("⏱️ Rest Countdown", f"{remaining}s")
                            time.sleep(1)
                        rest_placeholder.empty()
                        feedback_box.success("Get ready for the next set!")
                    else:
                        speak("Workout completed successfully. Awesome job!")
                        feedback_box.success("🎉 All sets completed successfully!")
                        
                        st.balloons()
                        st.markdown("---")
                        st.markdown("""
                            <div style="background: linear-gradient(135deg, #047857 0%, #065f46 100%); padding: 20px; border-radius: 12px; text-align: center; border: 1px solid #34d399; box-shadow: 0 8px 20px rgba(4, 120, 87, 0.3);">
                                <h2 style="color: #6ee7b7 !important; margin: 0;">🎈🎊 Workout Completed Successfully! 🌟🔥</h2>
                                <p style="color: #d1fae5; font-size: 16px; margin-top: 5px;">Amazing dedication! Here is your final se<p style="color: #d1fae5; font-size: 16px; margin-top: 5px;">Amazing dedication! Here is your final session breakdown.</p>
                            </div>
                        """, unsafe_allow_html=True)
                        st.markdown("<br>", unsafe_allow_html=True)
                        
                        st.subheader("📋 Workout Summary Report Card")
                        col_a, col_b, col_c = st.columns(3)
                        col_a.metric("Total Exercises", exercise)
                        col_b.metric("Total Repetitions", str(total_reps_all_sets))
                        col_c.metric("Estimated Calories Burned", f"{int(total_reps_all_sets * calorie_multiplier)} kcal")
                        break

                min_left = remaining_workout_time // 60
                sec_left = remaining_workout_time % 60
                timer_str = f"{min_left:02d}:{sec_left:02d}"

                rep_placeholder.metric("Current Reps", str(counter), delta=f"Target: {target_reps}")
                set_placeholder.metric("Current Set", f"{current_set} / {target_sets}")
                stage_placeholder.metric("Current Stage", stage)
                timer_placeholder.metric("Workout Time Left", timer_str)
                calories_placeholder.metric("Est. Calories Burned", f"{int(total_reps_all_sets * calorie_multiplier)} kcal")
                
                progress_percent = min(float(counter / target_reps), 1.0)
                progress_bar.progress(progress_percent)
                
            except Exception as e:
                pass
            
            mp_drawing.draw_landmarks(
                image, 
                results.pose_landmarks, 
                mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(56, 189, 248), thickness=2, circle_radius=3),
                mp_drawing.DrawingSpec(color=(192, 132, 252), thickness=2, circle_radius=2)
            )
            
            stframe.image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), channels="RGB")
            
    cap.release()

# --- EXERCISE GUIDE & POSTURE INSTRUCTION SECTION ---
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("## 📖 Comprehensive Exercise Guide & Posture Instruction Manual")
st.markdown("Yeh guide aapko batati hai ki kis exercise mein kya posture rakhna hai, angles kaise maintain karne hain, aur common mistakes se kaise bachna hai.")

col_g1, col_g2 = st.columns(2)

with col_g1:
    st.markdown("""
        <div class="guide-card">
            <div class="guide-title">💪 1. Seated Bicep / Hammer Curl</div>
            <div class="guide-text">
                <b>Target Muscle:</b> Biceps Brachii & Brachioradialis<br>
                <b>How to Perform:</b><br>
                • Sit upright on a chair with feet flat on the floor.<br>
                • Keep your elbows locked close to your sides throughout the movement.<br>
                • Curl weights upward until your forearm touches your bicep.<br>
                <b>Angle Tracking:</b><br>
                • Start Position (Arm Extended): Angle > 140°<br>
                • Peak Contraction: Angle < 50°<br>
            </div>
            <div class="tip-badge">💡 Tip: Avoid swinging your upper body or moving your elbows forward.</div>
        </div>

        <div class="guide-card">
            <div class="guide-title">🏋️‍♂️ 2. Seated Shoulder Press</div>
            <div class="guide-text">
                <b>Target Muscle:</b> Deltoids & Triceps<br>
                <b>How to Perform:</b><br>
                • Sit straight with back supported against the chair backrest.<br>
                • Hold dumbbells at shoulder height with palms facing forward.<br>
                • Press weights overhead until arms are fully extended.<br>
                <b>Angle Tracking:</b><br>
                • Start Position (At Shoulders): Angle < 80°<br>
                • Overhead Lockout: Angle > 150°<br>
            </div>
            <div class="tip-badge">💡 Tip: Keep core tight and avoid arching your lower back.</div>
        </div>

        <div class="guide-card">
            <div class="guide-title">🦵 3. Seated Leg Extension</div>
            <div class="guide-text">
                <b>Target Muscle:</b> Quadriceps (Thighs)<br>
                <b>How to Perform:</b><br>
                • Sit firmly on a chair with hands resting on the seat sides.<br>
                • Extend one leg outward until fully straight parallel to the floor.<br>
                • Hold for a split second, then slowly lower back down.<br>
                <b>Angle Tracking:</b><br>
                • Start Position (Knee Bent): Angle < 100°<br>
                • Full Extension: Angle > 160°<br>
            </div>
            <div class="tip-badge">💡 Tip: Control the descent; do not let your leg drop suddenly.</div>
        </div>

        <div class="guide-card">
            <div class="guide-title">🦾 4. Seated Triceps Extension</div>
            <div class="guide-text">
                <b>Target Muscle:</b> Triceps Brachii<br>
                <b>How to Perform:</b><br>
                • Sit upright, holding a weight overhead with both hands.<br>
                • Keep elbows pointing upward and close to your ears.<br>
                • Lower weight behind your head, then extend arms back up.<br>
                <b>Angle Tracking:</b><br>
                • Extended Position: Angle > 140°<br>
                • Bent/Lowered Position: Angle < 80°<br>
            </div>
            <div class="tip-badge">💡 Tip: Ensure your upper arms remain stationary while bending elbows.</div>
        </div>
    """, unsafe_allow_html=True)

with col_g2:
    st.markdown("""
        <div class="guide-card">
            <div class="guide-title">🙆‍♂️ 5. Seated Lateral Raises</div>
            <div class="guide-text">
                <b>Target Muscle:</b> Side Deltoids (Shoulders)<br>
                <b>How to Perform:</b><br>
                • Sit upright with dumbbells at your sides.<br>
                • Raise arms out to the sides with a slight bend in the elbow.<br>
                • Lift until arms reach parallel with your shoulders.<br>
                <b>Angle Tracking:</b><br>
                • Start Position (Arms Down): Angle < 30°<br>
                • Raised Position: Angle > 75°<br>
            </div>
            <div class="tip-badge">💡 Tip: Do not use momentum or shrug your shoulders upward.</div>
        </div>

        <div class="guide-card">
            <div class="guide-title">🚶‍♂️ 6. Seated Knee Raises (Marching)</div>
            <div class="guide-text">
                <b>Target Muscle:</b> Hip Flexors & Core (Abs)<br>
                <b>How to Perform:</b><br>
                • Sit tall on the chair without leaning back.<br>
                • Lift one knee up toward your chest in a marching motion.<br>
                • Lower it gently and alternate with the other leg.<br>
                <b>Angle Tracking:</b><br>
                • Start Position (Foot Down): Angle > 130°<br>
                • Knee Raised: Angle < 90°<br>
            </div>
            <div class="tip-badge">💡 Tip: Maintain a straight torso and avoid slouching forward.</div>
        </div>

        <div class="guide-card">
            <div class="guide-title">🚣‍♂️ 7. Seated Upright Row</div>
            <div class="guide-text">
                <b>Target Muscle:</b> Trapezius & Shoulders<br>
                <b>How to Perform:</b><br>
                • Sit upright, holding weights in front of your thighs.<br>
                • Pull weights upward toward your chin, leading with your elbows.<br>
                • Keep elbows higher than your wrists throughout.<br>
                <b>Angle Tracking:</b><br>
                • Start Position (Arms Down): Angle > 140°<br>
                • Pulled Up Position: Angle < 70°<br>
            </div>
            <div class="tip-badge">💡 Tip: Keep weights close to your body as you pull up.</div>
        </div>

        <div class="guide-card">
            <div class="guide-title">🌟 General Safety & Best Practices</div>
            <div class="guide-text">
                <b>Camera Placement:</b><br>
                • Place your laptop or phone on a stable surface sideways (profile view).<br>
                • Ensure your full upper/lower body joints are visible to MediaPipe.<br><br>
                <b>Breathing Technique:</b><br>
                • Exhale when exerting effort (lifting/contracting).<br>
                • Inhale when returning to the starting position.
            </div>
            <div class="tip-badge">💡 Tip: Consistency and proper form matter much more than speed!</div>
        </div>
    """, unsafe_allow_html=True)