import streamlit as st
import time
from swarm import Swarm, Agent

# Initialize the Swarm client
client = Swarm()

# Agent for financial advice
def transfer_to_fitness_agent():
    return fitness_agent

financial_agent = Agent(
    name="Financial Advisor",
    instructions="You are an expert in providing financial advice, including budgeting, investments, and savings tips.",
    functions=[transfer_to_fitness_agent],  # Can transfer conversation to the fitness agent
)

# Agent for fitness tips
fitness_agent = Agent(
    name="Fitness Coach",
    instructions="You are a fitness expert. Offer workout routines, health tips, and motivation for staying fit.",
)

# Streamlit app
st.set_page_config(page_title="AI Agent Swarm Interactive Demo", page_icon="🤖", layout="wide")

st.title("🤖 AI Agent Swarm Interactive Demo")
st.markdown("Watch our AI agents collaborate in real-time!")

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Chat input
user_input = st.text_input("Ask anything about finance or fitness:")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

# Display chat messages
for message in st.session_state.messages:
    if message["role"] == "user":
        st.text_area("You:", value=message["content"], height=50, disabled=True)
    else:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Process user input
if user_input:
    # Start with financial agent
    with st.spinner("Financial Advisor is analyzing your query..."):
        financial_response = client.run(
            agent=financial_agent,
            messages=[{"role": "user", "content": user_input}],
        )
        time.sleep(1)  # Simulate processing time
    
    st.session_state.messages.append({"role": "assistant", "content": f"💼 Financial Advisor: {financial_response.messages[-1]['content']}"})
    
    # Check if handoff to fitness agent is needed
    if "fitness" in financial_response.messages[-1]["content"].lower():
        with st.spinner("Handing off to Fitness Coach..."):
            time.sleep(1)  # Simulate handoff time
        st.info("🔀 The Financial Advisor is transferring your query to the Fitness Coach!")
        
        with st.spinner("Fitness Coach is preparing a response..."):
            fitness_response = client.run(
                agent=fitness_agent,
                messages=[{"role": "user", "content": user_input}],
            )
            time.sleep(1)  # Simulate processing time
        
        st.session_state.messages.append({"role": "assistant", "content": f"🏋️ Fitness Coach: {fitness_response.messages[-1]['content']}"})

# Agent interaction visualization
st.subheader("Agent Interaction Visualization")
col1, col2, col3 = st.columns(3)

with col1:
    st.image("https://img.icons8.com/color/96/000000/financial-advisor.png", width=100)
    st.markdown("💼 Financial Advisor")

with col2:
    st.image("https://img.icons8.com/color/96/000000/arrow.png", width=100)
    st.markdown("🔀 Dynamic Handoff")

with col3:
    st.image("https://img.icons8.com/color/96/000000/personal-trainer.png", width=100)
    st.markdown("🏋️ Fitness Coach")

# Agent state and metrics
st.subheader("Agent States and Metrics")
col1, col2 = st.columns(2)

with col1:
    st.metric(label="Financial Advisor Queries", value=len([m for m in st.session_state.messages if "Financial Advisor" in m.get("content", "")]))

with col2:
    st.metric(label="Fitness Coach Queries", value=len([m for m in st.session_state.messages if "Fitness Coach" in m.get("content", "")]))

# Explanation of the process
st.subheader("How It Works")
st.markdown("""
1. 🎬 Your query is initially sent to the Financial Advisor.
2. 💡 The Financial Advisor analyzes the query and provides a response.
3. 🔍 If the query contains fitness-related content, a handoff occurs.
4. 🔀 The Fitness Coach then receives the query and provides specialized advice.
5. 🔄 This process ensures you always get the most relevant expertise!
""")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit and OpenAI's Agent Swarm")