import os
import json
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- Configuration & Data ---
# Expanded Fake Database with 15 detailed records
ORDER_DB = {
    "DH101": {"status": "Delivered", "delivery": "20 March", "items": "Sandalwood Incense, Brass Diya", "total": "₹1,250", "customer": "Rahul Sharma"},
    "DH102": {"status": "Shipped", "delivery": "30 March", "items": "Copper Water Bottle", "total": "₹899", "customer": "Priya Patel"},
    "DH103": {"status": "Processing", "delivery": "2 April", "items": "Yoga Mat, Meditation Cushion", "total": "₹2,450", "customer": "Ananya Iyer"},
    "DH104": {"status": "Out for Delivery", "delivery": "Today", "items": "Ganesha Statue (Marble)", "total": "₹4,200", "customer": "Vikram Singh"},
    "DH105": {"status": "Delivered", "delivery": "15 March", "items": "Organic Honey, Tulsi Tea", "total": "₹550", "customer": "Sneha Reddy"},
    "DH106": {"status": "Shipped", "delivery": "31 March", "items": "Rudraksha Mala (108 beads)", "total": "₹1,100", "customer": "Amit Verma"},
    "DH107": {"status": "Processing", "delivery": "3 April", "items": "Ayurvedic Hair Oil", "total": "₹750", "customer": "Kavita Gupta"},
    "DH108": {"status": "Processing", "delivery": "4 April", "items": "Handcrafted Singing Bowl", "total": "₹3,100", "customer": "Sandeep Das"},
    "DH109": {"status": "Delivered", "delivery": "10 March", "items": "Panch Aarti Stand", "total": "₹1,800", "customer": "Neha Malhotra"},
    "DH110": {"status": "Out for Delivery", "delivery": "Today", "items": "Lord Shiva Canvas Art", "total": "₹1,550", "customer": "Arjun Rao"},
    "DH111": {"status": "Cancelled", "delivery": "N/A", "items": "Cotton Dhoti (Set of 2)", "total": "₹1,050", "customer": "Siddharth Jain"},
    "DH112": {"status": "Processing", "delivery": "5 April", "items": "Bells & Chimes (Wind)", "total": "₹650", "customer": "Pooja Hegde"},
    "DH113": {"status": "Shipped", "delivery": "1 April", "items": "Jasmine Essential Oil", "total": "₹400", "customer": "Rajesh Nair"},
    "DH114": {"status": "Delivered", "delivery": "25 March", "items": "Puja Thali Set", "total": "₹2,999", "customer": "Aditi Joshi"},
    "DH115": {"status": "Processing", "delivery": "6 April", "items": "Wooden Temple (Small)", "total": "₹5,400", "customer": "Manoj Kumar"}
}

DEFAULT_MODEL = "llama-3.1-8b-instant"

# --- WhatsAppUI Shell ---
st.set_page_config(page_title="Divine Hindu AI Assistant", page_icon="🟢", layout="centered")

# CSS Overhaul
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@400;600&display=swap');
    
    html, body, [class*="st-"] { font-family: 'Segoe UI', sans-serif; }
    
    .stApp {
        background-color: #0b141a;
        background-image: url('https://user-images.githubusercontent.com/15075759/28719144-86dc0f70-73b1-11e7-911d-60d70fcded21.png');
        background-blend-mode: overlay;
    }

    /* Fixed Header */
    .whatsapp-header {
        position: fixed; top: 0; left: 0; right: 0; height: 60px;
        background-color: #202c33; display: flex; align-items: center;
        padding: 0 20px; z-index: 1000; border-bottom: 1px solid #303d45;
    }
    .header-content { display: flex; align-items: center; gap: 15px; }
    .avatar { width: 40px; height: 40px; background-color: #53bdeb; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; color: white; }
    .brand-name { color: #e9edef; font-weight: 600; font-size: 1.1rem; }
    .online-status { color: #8696a0; font-size: 0.8rem; }

    /* Chat Container */
    .chat-container { padding: 80px 10px 180px 10px; display: flex; flex-direction: column; gap: 8px; }
    .chat-bubble { padding: 10px 15px; font-size: 0.95rem; position: relative; max-width: 80%; box-shadow: 0 1px 1px rgba(0,0,0,0.4); margin-bottom: 2px; }
    .user-bubble { background-color: #005c4b; color: #e9edef; align-self: flex-end; border-radius: 10px 0 10px 10px; }
    .bot-bubble { background-color: #202c33; color: #e9edef; align-self: flex-start; border-radius: 0 10px 10px 10px; }
    .bubble-time { font-size: 0.65rem; color: rgba(233,237,239,0.5); text-align: right; margin-top: 5px; }

    /* Floating Bottom Container */
    .input-wrapper {
        position: fixed; bottom: 0; left: 0; right: 0;
        background-color: #111b21; padding: 10px 15px 30px 15px;
        z-index: 1000; border-top: 1px solid #222d34;
    }

    /* WhatsApp Style Input Bar */
    [data-testid="stForm"] { border: none !important; padding: 0 !important; }
    
    .stTextInput > div > div > input {
        border-radius: 25px !important;
        background-color: #2a3942 !important;
        color: #e9edef !important;
        border: none !important;
        padding: 15px 20px !important;
        font-size: 1rem !important;
        height: 55px !important;
    }
    
    .stButton > button[kind="primaryFormSubmit"] {
        background-color: #00a884 !important;
        border-radius: 50% !important;
        width: 55px !important;
        height: 55px !important;
        min-width: 55px !important;
        color: white !important;
        border: none !important;
        font-size: 1.6rem !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        margin-left: 10px !important;
    }
    

    /* === Input Bar Layout === */
    /* Target only the form's horizontal block (inside stForm) */
    [data-testid="stForm"] div[data-testid="stHorizontalBlock"] {
        flex-wrap: nowrap !important;
        align-items: center !important;
        gap: 8px !important;
    }
    /* Send button column: fixed narrow width */
    [data-testid="stForm"] div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:last-child {
        flex: 0 0 58px !important;
        min-width: 58px !important;
        max-width: 58px !important;
        padding: 0 !important;
    }
    /* Text input column: take remaining space */
    [data-testid="stForm"] div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:first-child {
        flex: 1 1 0 !important;
        min-width: 0 !important;
    }

    /* === Suggestion Chips === */
    /* The chip row: horizontally scrollable */
    .chip-scrollable > div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-wrap: nowrap !important;
        overflow-x: auto !important;
        gap: 6px !important;
        padding-bottom: 4px !important;
        scrollbar-width: none !important;
        -ms-overflow-style: none !important;
    }
    .chip-scrollable > div[data-testid="stHorizontalBlock"]::-webkit-scrollbar { display: none !important; }
    /* Each chip column: shrink to content */
    .chip-scrollable > div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
        flex: 0 0 auto !important;
        min-width: unset !important;
        width: auto !important;
        padding: 0 2px !important;
    }
    /* Chip button appearance */
    .chip-scrollable .stButton > button {
        border-radius: 15px !important;
        background-color: #202c33 !important;
        border: 1px solid #334049 !important;
        color: #e9edef !important;
        font-size: 0.78rem !important;
        padding: 5px 14px !important;
        white-space: nowrap !important;
        height: auto !important;
        min-height: 32px !important;
        width: auto !important;
        min-width: unset !important;
        transition: background 0.15s !important;
    }
    .chip-scrollable .stButton > button:hover {
        background-color: #2a3942 !important;
        border-color: #53bdeb !important;
    }

    @media (max-width: 768px) {
        .chat-bubble { max-width: 92%; }
    }

    header {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- Logic ---

def detect_intent(message):
    active_order = st.session_state.get("active_order_id", "None")
    valid_ids = ", ".join(list(ORDER_DB.keys()))
    prompt = f"""
    Engine: Divine Hindu. Valid IDs: {valid_ids}. Current: {active_order}.
    - Map typos or partials to valid IDs.
    - Intent: order_tracking, return, general.
    Return JSON: {{"intent": "...", "order_id": "..."}}
    Msg: "{message}"
    """
    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY") or st.session_state.get("groq_api_key"))
        resp = client.chat.completions.create(model=DEFAULT_MODEL, messages=[{"role":"user","content":prompt}], response_format={"type":"json_object"})
        data = json.loads(resp.choices[0].message.content)
        if data.get("order_id"):
            id_v = str(data["order_id"]).upper().replace(" ","")
            if id_v.isdigit(): id_v = f"DH{id_v}"
            st.session_state["active_order_id"] = id_v
            data["order_id"] = id_v
        return data
    except: return {"intent":"general","order_id":None}

def generate_reply(user_msg, intent_data):
    raw_id = intent_data.get("order_id") or st.session_state.get("active_order_id")
    order_id = str(raw_id).strip().upper().replace(" ","") if raw_id else None
    order_data = ORDER_DB.get(order_id)
    ctx = f"DB RECORD for {order_id}: {json.dumps(order_data)}" if order_data else "No order record found."
    
    sys_prompt = f"""
    You are 'Divine Hindu AI Assistant'. Data: {ctx}
    STRICT RULES:
    1. MAX 2 SENTENCES. No explanation of ability.
    2. If ID missing: "Namaste! 🙏 Please share your Order ID (DH101-DH115) so I can assist you."
    3. If ID found: Provide FULL SUMMARY (Name, Items, Total, Status, Delivery) using HTML <b> for bold.
    4. NEVER use Markdown stars (**) for bold. Use HTML tags <b> and </b>.
    5. Return Policy: 3 days. 
    6. Always start with 'Namaste! 🙏'.
    """
    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY") or st.session_state.get("groq_api_key"))
        resp = client.chat.completions.create(model=DEFAULT_MODEL, messages=[{"role":"system","content":sys_prompt},{"role":"user","content":user_msg}])
        return resp.choices[0].message.content
    except: return "Namaste! 🙏 Please check your connection or Order ID."

# --- UI Assembly ---

# Header
st.markdown(f'<div class="whatsapp-header"><div class="header-content"><div class="avatar">DH</div><div><div class="brand-name">Divine Hindu AI Assistant</div><div class="online-status">online</div></div></div></div>', unsafe_allow_html=True)

if "messages" not in st.session_state: st.session_state.messages = []

# Messages
chat_html = "<div class='chat-container'>"
for msg in st.session_state.messages:
    side = "user-bubble" if msg["role"] == "user" else "bot-bubble"
    formatted_content = msg["content"].replace("\n", "<br>")
    chat_html += f'<div class="chat-bubble {side}">{formatted_content}<div class="bubble-time">12:30</div></div>'
chat_html += "</div>"
st.markdown(chat_html, unsafe_allow_html=True)

# Fixed Bottom Footer
st.markdown('<div class="input-wrapper">', unsafe_allow_html=True)

# Chips — horizontally scrollable row (works on all screen sizes)
st.markdown("<div style='margin-bottom:6px; color:#8696a0; font-size:0.7rem; font-weight:600; text-transform:uppercase; letter-spacing:0.05em;'>💡 Suggestions</div>", unsafe_allow_html=True)
suggestions = ["Track My Order", "Return Policy", "Payment Issues", "Talk to Agent", "Shipping Info", "Order History"]
clicked_s = None
# Wrap chip columns in a div with class for scoped CSS
st.markdown("<div class='chip-scrollable'>", unsafe_allow_html=True)
_chip_cols = st.columns(len(suggestions))
for i, s in enumerate(suggestions):
    with _chip_cols[i]:
        if st.button(s, key=f"sugg_{i}", use_container_width=False): clicked_s = s
st.markdown("</div>", unsafe_allow_html=True)

# Form
with st.form(key='wa_form', clear_on_submit=True):
    sub_col1, sub_col2 = st.columns([0.88, 0.12])
    with sub_col1:
        u_input = st.text_input("", placeholder="Type a message", label_visibility="collapsed")
    with sub_col2:
        submit = st.form_submit_button("➤")
st.markdown('</div>', unsafe_allow_html=True)

# Side bar for key
with st.sidebar:
    st.title("Settings")
    if not os.getenv("GROQ_API_KEY"):
        key = st.text_input("Enter Groq API Key:", type="password")
        if key: st.session_state["groq_api_key"] = key

# Process
final = u_input if (submit and u_input) else clicked_s
if final:
    st.session_state.messages.append({"role": "user", "content": final})
    data = detect_intent(final)
    reply = generate_reply(final, data)
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()
