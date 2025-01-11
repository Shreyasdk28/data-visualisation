import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

# Define the stages of the policy lifecycle
policy_lifecycle = [
    {
        "stage": "Policy Issued", 
        "description": "The policy is issued to the policyholder after they purchase the insurance plan. The policy document outlines the terms, coverage details, exclusions, and the premium amount.",
        "customer_action": "Review policy document and ensure all details are correct.",
        "estimated_time": "1-3 days"
    },
    {
        "stage": "Premium Payments", 
        "description": "The policyholder starts paying premiums either monthly, quarterly, or annually as per the policy terms. Non-payment can lead to policy lapses.",
        "customer_action": "Make premium payments on time to keep the policy active.",
        "estimated_time": "Ongoing"
    },
    {
        "stage": "Policy Active", 
        "description": "The policy becomes active, and the insurance company provides coverage to the policyholder against specified risks or events covered under the policy.",
        "customer_action": "Keep your details up-to-date and ensure continued premium payments.",
        "estimated_time": "Varies (could last months or years)"
    },
    {
        "stage": "Claim Made", 
        "description": "The policyholder files a claim, usually after an event like a medical emergency, accident, or damage that is covered under the policy. The claim is submitted to the insurer for review.",
        "customer_action": "Submit the necessary documents and evidence for the claim.",
        "estimated_time": "1-2 weeks"
    },
    {
        "stage": "Claim Processed", 
        "description": "The insurance company reviews and processes the claim, assessing the validity of the claim and ensuring that all required documentation is provided.",
        "customer_action": "Respond to any queries from the insurance company.",
        "estimated_time": "2-6 weeks"
    },
    {
        "stage": "Claim Paid", 
        "description": "The insurance company settles the claim, either partially or fully, based on the terms of the policy. The payment is made to the policyholder or directly to a healthcare provider, repair shop, or other beneficiary.",
        "customer_action": "Receive payment or coverage for the claim. Review settlement details.",
        "estimated_time": "Varies (usually 1-2 weeks after claim approval)"
    },
    {
        "stage": "Policy Expired/Terminated", 
        "description": "The policy expires either at the end of its term or is terminated due to conditions such as non-payment of premiums or a claim denial. The policyholder may renew or cancel the policy.",
        "customer_action": "Renew or cancel the policy as needed. Review options for extending or changing coverage.",
        "estimated_time": "End of term (annual, bi-annual, etc.)"
    }
]

# Create a directed graph for the policy lifecycle
G = nx.DiGraph()

# Add nodes for each stage
for stage in policy_lifecycle:
    G.add_node(stage["stage"], description=stage["description"])

# Add edges between stages to show the flow
for i in range(len(policy_lifecycle) - 1):
    G.add_edge(policy_lifecycle[i]["stage"], policy_lifecycle[i+1]["stage"])

# Set up the plot
plt.figure(figsize=(12, 8))

# Generate a layout for the graph
pos = nx.spring_layout(G, seed=42)  # Layout for better positioning of nodes

# Draw the graph with custom styles
nx.draw(G, pos, with_labels=True, node_size=3000, node_color='skyblue', font_size=10, font_weight='bold', arrows=True, edge_color='gray', width=2)

# Draw edge labels with descriptions for each stage transition
edge_labels = {}
for (start, end) in G.edges():
    edge_labels[(start, end)] = f"Next Step: {end}"

nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8, font_color='black')

# Title and other plot settings
plt.title("Policy Lifecycle Flowchart", fontsize=14)
plt.axis('off')  # Turn off the axis

# Use Streamlit's st.pyplot to display the plot
st.pyplot(plt)

# Streamlit Interface
st.title("Policy Lifecycle Visualization")

# Show the lifecycle stages with detailed information
selected_stage = st.selectbox("Select a stage to learn more", [item['stage'] for item in policy_lifecycle])

for stage in policy_lifecycle:
    if stage['stage'] == selected_stage:
        st.write(f"### {selected_stage}")
        st.write(f"**Description:** {stage['description']}")
        st.write(f"**Customer Action:** {stage['customer_action']}")
        st.write(f"**Estimated Time:** {stage['estimated_time']}")
